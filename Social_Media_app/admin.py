from django.contrib import admin
from .models import Like ,Comment,Post,CustomUser

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CustomUser)