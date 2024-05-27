from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework.decorators import api_view , permission_classes ,authentication_classes
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status , generics , viewsets
from rest_framework.views import APIView
from .serializers import RegisterSerializer , PostSerializer , LikeSerializer , CommentSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import Post , Like ,Comment
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

# def send_email_to_client(request):
    



@api_view()
def Home(request):
    return Response({'message':'HelloWorld'},status=status.HTTP_200_OK)

@api_view(['POST',])
# @authentication_classes([TokenAuthentication])
# @permission_classes([])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'message':'Deleted'},status=status.HTTP_200_OK)


class Registerview(APIView):
    permission_classes=[AllowAny]
    
    
    def post(self,request):
        data = request.data
        subject = "Registration in Social Media App"
        message = "Congrtulations You have successfully registered in the Application "
        from_email=settings.EMAIL_HOST_USER
        emaila = data.get('email')
        recipient_list = [emaila]
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_mail(subject,message,from_email,recipient_list)
            serializer.save()
            return Response({'username':serializer.data['username'],'email':serializer.data['email']},status=status.HTTP_201_CREATED)
        
    
class Postview(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    filter_backends = [SearchFilter] 
    search_fields=['^title']

class Commentview(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

class Likeview(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    # filterset_fields=['user','post']

    # def create(self, request):
    #     user = request.user
    #     post = request.data.get('post')
    #     if Like.objects.filter(user=user,post_id=post).exists():
    #         return Response("Already Liked",status=status.HTTP_400_BAD_REQUEST)
    #     return super().create(request)
