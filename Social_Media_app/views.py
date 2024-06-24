from rest_framework.decorators import api_view , permission_classes ,authentication_classes,action
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView 
from .serializers import *
from rest_framework import status , generics ,serializers
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters
from .pagination import CustomPagination
from django.http import HttpResponse
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


class logout_view(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({'message':'Deleted'},status=status.HTTP_200_OK)
      
class Registerview(generics.CreateAPIView):
    permission_classes=[AllowAny]  
    throttle_classes=[OncePerDayUserThrottle]
    queryset=CustomUser.objects.all()
    serializer_class=RegisterSerializer

class has_imagefilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        has_image = request.query_params.get('has_image')
        if has_image is not None:
            if has_image.lower() == 'true':
                queryset = queryset.exclude(image__isnull=True).exclude(image='')
            elif has_image.lower() == 'false':
                queryset = queryset.filter(image='')
            else:
                raise serializers.ValidationError('expected True or false')
        return queryset
class Postview(viewsets.ModelViewSet):
    # permission_classes=[AllowAny]
    queryset=Post.objects.prefetch_related('post_like','post_comment').all()
    throttle_classes=[OncePerDayUserThrottle]
    filterset_fields=['user']
    search_fields=['title','tag']
    filter_backends=[has_imagefilter,DjangoFilterBackend,filters.SearchFilter]
    pagination_class=CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user':user})
        return context
    
    def get_serializer_class(self):
        if self.action in ['listing_Post','list','retrieve']:
            return PostListingSerializer
        return PostCreateSerializer2
    
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
        if Like.objects.filter(user=user_id, post=request.data.get('post')).exists():
            Like.objects.filter(user=user_id, post=request.data.get('post')).delete()
            return Response({'message':'Unlike'},status=status.HTTP_200_OK)
        else:
            return Response("Already didn't like the post")
        

def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip))
        