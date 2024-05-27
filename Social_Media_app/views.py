from django.shortcuts import render 
# from django.http import HttpResponse
from rest_framework.decorators import api_view , permission_classes ,authentication_classes
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

# Create your views here.


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
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'username':serializer.data['username'],'email':serializer.data['email']},status=status.HTTP_201_CREATED)
        
    
