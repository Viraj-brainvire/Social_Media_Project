from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from os.path import splitext

def validate_brainvire_mail(value):
    if "@brainvire.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of brainvire only")

def validate_image(value):
    check = splitext(value.name)[1]
    alloewd_extentions = [".jpeg",".pdf"]
    if check.lower() not in alloewd_extentions:
        raise ValidationError("Check the Extentions or Select another image")

    # img_size = value.size
    # if img_size > 3*1024*1024 :
    #     raise ValidationError("this file size is very big")

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(("email address"), blank=True,validators =[validate_brainvire_mail])
    phone_number = PhoneNumberField(null=False, blank=False)

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(upload_to="./Social_Media_app/Images",null=True,validators =[validate_image])
    tag=models.TextField()
    posted_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_post', related_query_name='user_post',null=True,blank=True)
        

class Comment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE ,related_name="post_comment")
    text=models.TextField()

class Like(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE ,related_name="post_like",related_query_name='post_like')

    class Meta:
        unique_together = ('user','post')
    