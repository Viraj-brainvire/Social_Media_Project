from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False)

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(upload_to="./Social_Media_app/Images",null=True)
    tag=models.TextField()
    posted_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
        

class Comment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE ,related_name="post_comment")
    text=models.TextField()

class Like(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE ,related_name="post_like")

    class Meta:
        unique_together = ('user','post')
    