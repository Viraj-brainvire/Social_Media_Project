from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post,Like,Comment
# from .models import 

class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','password_confirmation']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password_confirmation']

        if password != password2:
            raise serializers.ValidationError({'error':'password and password2 are not same'})
        
        if User.objects.filter(email =self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email Already Exist'})
        
        account = User(username = self.validated_data['username'],email=self.validated_data['email'])
        account.set_password(password)
        account.save()

        return account
        
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model= Post
        fields='__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model= Like
        fields='__all__'

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model= Comment
        fields='__all__'

       