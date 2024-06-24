from rest_framework import serializers , validators
from .models import *
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.conf import settings
from Social_Media.celery import send_mail
# from .models import 

class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','password','password_confirmation','phone_number']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password_confirmation']

        if password != password2:
            raise serializers.ValidationError({'error':'password and password2 are not same'})
        
        if CustomUser.objects.filter(email =self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email Already Exist'})
        
        # email= EmailMessage("Registration in Social Media App",f"Congrtulations {self.validated_data['first_name']}, You have successfully registered in the Application ",
        # settings.EMAIL_HOST_USER,[self.validated_data['email']])
        # email.send()
        send_mail.delay(self.validated_data['first_name'],self.validated_data['email'])
        account = CustomUser(username = self.validated_data['username'],email=self.validated_data['email'],first_name=self.validated_data['first_name'],last_name=self.validated_data['last_name'],phone_number=self.validated_data['phone_number'])
        account.set_password(password)
        account.save()

        return account
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        exclude=['password','is_superuser','is_staff','date_joined','phone_number','groups','user_permissions']
class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model= Post
        fields=['id','title','content','image','tag','posted_at','updated_at','user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        print(validated_data)
        return super().create(validated_data)
    
class PostCreateSerializer2(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    content=serializers.CharField()
    image=serializers.ImageField(required=False)
    tag=serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self,validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.content = validated_data.get('content',instance.content)
        instance.image = validated_data.get('image',instance.image)
        instance.tag = validated_data.get('tag',instance.tag)
        instance.user = validated_data.get('user',instance.user)
        instance.save()
        return instance

class PostListingSerializer(serializers.ModelSerializer):

    likescount = serializers.SerializerMethodField()
    commentscount=serializers.SerializerMethodField()
    user=UserSerializer()
    class Meta:
        model= Post
        fields=['id','title','content','image','tag','posted_at','updated_at','likescount','commentscount','user']

    def get_likescount(self, obj):
        return obj.post_like.count()
    
    def get_commentscount(self,obj):
        return obj.post_comment.count()
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model= Comment
        fields='__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        print(validated_data)
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model= Like
        fields='__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user','post'),
                message=('Already liked')
            )
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        print(validated_data)
        return super().create(validated_data)
    # def to_internal_value(self, data):
    #     user = Token.objects.get(key=self.context["request"].auth.key).user
    #     mutable_data=data.copy()
    #     mutable_data['user'] = user.id
    #     return super().to_internal_value(mutable_data)
    
        