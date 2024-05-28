from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes ,authentication_classes
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .serializers import RegisterSerializer , PostSerializer , LikeSerializer , CommentSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post , Like ,Comment
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from rest_framework.throttling import UserRateThrottle
# Create your views here.
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '150/day'

@api_view()
def Home(request):
    return Response({'message':'HelloWorld'},status=status.HTTP_200_OK)

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'message':'Deleted'},status=status.HTTP_200_OK)

class Registerview(APIView):
    permission_classes=[AllowAny]  
    throttle_classes=[OncePerDayUserThrottle]
    
    def post(self,request):        
        email= EmailMessage("Registration in Social Media App",
         f"Congrtulations {request.data.get('first_name')}, You have successfully registered in the Application ",
        settings.EMAIL_HOST_USER,
         [request.data.get('email')])
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email.send()
            # send_mail(subject,message,from_email,recipient_list)
            serializer.save()
            return Response({'username':serializer.data['username'],'email':serializer.data['email']},status=status.HTTP_201_CREATED)               

class Postview(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    throttle_classes=[OncePerDayUserThrottle]
    filterset_fields=['user']
    search_fields=['title','tag']

    def create(self ,request ,*args,**kwargs):
        user_id = Token.objects.get(key=request.auth.key).user_id
        if int(user_id)== int(request.data.get('user')):
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers=self.get_success_headers(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
        else:
            return Response("Not a Valid user Id")

class Commentview(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    filterset_fields=['user','post']

    def create(self ,request ,*args,**kwargs):
        user_id = Token.objects.get(key=request.auth.key).user_id
        if int(user_id)== int(request.data.get('user')):
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers=self.get_success_headers(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
        else:
            return Response("Not a Valid user Id")

class Likeview(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    filterset_fields=['user','post']


@api_view(['DELETE',])
def Remove_like(request):

    if request.method == 'DELETE':
        # serializer = LikeSerializer(data=request.data)
        user_id = Token.objects.get(key=request.auth.key).user_id
        if int(user_id)== int(request.data.get('user')):
            if Like.objects.filter(user=request.data.get('user'), post=request.data.get('post')).exists():
                Like.objects.filter(user=request.data.get('user'), post=request.data.get('post')).delete()
                return Response({'message':'Unlike'},status=status.HTTP_200_OK)
            else:
                return Response("Already didn't like the post")
        else:
            return Response("Not a Valid user Id")