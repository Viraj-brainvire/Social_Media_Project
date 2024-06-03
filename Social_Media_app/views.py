from rest_framework.decorators import api_view , permission_classes ,authentication_classes,action
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView 
from .serializers import *
from rest_framework import status , generics
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth import authenticate

from rest_framework.throttling import UserRateThrottle
# Create your views here.
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '150/day'

@api_view()
def Home(request):
    return Response({'message':'HelloWorld'},status=status.HTTP_200_OK)

class loginview(APIView):
    permission_classes=[AllowAny]
    def post(self , request):       
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            token ,created = Token.objects.get_or_create(user=user)
            return Response({"token":token.key},status=status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
    



# @api_view(['POST',])
class logout_view(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({'message':'Deleted'},status=status.HTTP_200_OK)

        
class Registerview(generics.CreateAPIView):
    permission_classes=[AllowAny]  
    throttle_classes=[OncePerDayUserThrottle]
    queryset=CustomUser.objects.all()
    serializer_class=RegisterSerializer
              

class Postview(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostCreateSerializer
    throttle_classes=[OncePerDayUserThrottle]
    filterset_fields=['user']
    search_fields=['title','tag']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user':user})
        return context
    
    def get_serializer_class(self):
        if self.action in ['listing_Post']:
            return PostListingSerializer
        return PostCreateSerializer
    
    @action(detail=False, methods=['get'])
    def listing_Post(self,request):
        queryset= Post.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

        



class Commentview(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    filterset_fields=['user','post']


    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user':user})
        return context

class Likeview(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    filterset_fields=['user','post']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user':user})
        return context

class remove_like(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        user_id = Token.objects.get(key=request.auth.key).user_id
        if int(user_id)== int(request.data.get('user')):
            if Like.objects.filter(user=request.data.get('user'), post=request.data.get('post')).exists():
                Like.objects.filter(user=request.data.get('user'), post=request.data.get('post')).delete()
                return Response({'message':'Unlike'},status=status.HTTP_200_OK)
            else:
                return Response("Already didn't like the post")
        else:
            return Response("Not a Valid user Id")


        