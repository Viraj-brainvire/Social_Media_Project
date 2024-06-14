from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Like ,Comment,Post,CustomUser
from .forms import PostForm
from django.urls import reverse
from django.utils.html import format_html
from import_export import fields, resources
from import_export.resources import Field
# Register your models here.

class classification(resources.ModelResource):
    user = Field(attribute="user__username" ,column_name="user")
    class Meta:
        model = Post 
        fields = ['id','user','title','posted_at','updated_at','tag']
class PostInline(admin.TabularInline):
    model = Post
    fields = ['user','title','posted_at']
    readonly_fields = ['posted_at']

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(ImportExportActionModelAdmin):
    list_display = ['id','user','title','likeCount','posted_at','updated_at','tag']    
    list_display_links = ['user']
    # fields = ['user',('title','image')]
    search_fields = ['user']
    list_filter = ['posted_at']
    list_per_page = 5
    empty_value_display = "-empty-"
    empty_value_display = "unknown"
    list_select_related = ['user']
    actions = ["superuser_change"]
    form = PostForm
    save_as = True
    resource_class = classification
    @admin.action(description='Superuser Change')
    def superuser_change(self,queryset):
        return queryset.update(is_superuser = True)
    @admin.display(description='Like Count', empty_value= '0')
    def likeCount(self, obj):
        return obj.post_like.count()

    list_max_show_all = 6

@admin.register(CustomUser)
class UserAdmin(ImportExportActionModelAdmin):
    list_display=['id','username','email','postCount']
    inlines=[PostInline]
    @admin.display(description='Post Count', empty_value= '0')
    def postCount(self, obj):
        return obj.user_post.count()
    
@admin.register(Like)
class LikeAdmin(ImportExportActionModelAdmin):
    list_display=['id','user','display_post']
    list_display_links = ['post']
    list_display_links = ['display_post']
    def display_post(self,obj):
        link = reverse("admin:Social_Media_app_post_change",args=[obj.post.id])
        return format_html('<a href="{}">{}</a>',link, obj.post)

    display_post.short_description='Post'

@admin.register(Comment)
class CommentAdmin(ImportExportActionModelAdmin):
    list_display=['id','user','display_post','text']
    list_select_related = ["post"]
    list_display_links = ['display_post']

    def display_post(self,obj):
        link = reverse("admin:Social_Media_app_post_change",args=[obj.post.id])
        return format_html('<a href="{}">{}</a>',link, obj.post)

    display_post.short_description='Post'

# admin.site.register(Comment)
# admin.site.register(Like)
# admin.site.register(CustomUser)

