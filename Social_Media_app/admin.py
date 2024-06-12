from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Like ,Comment,Post,CustomUser
from .forms import PostForm

# Register your models here.


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(ImportExportActionModelAdmin):
    list_display = ['id','user','title','image']
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
    @admin.action(description='Superuser Change')
    def superuser_change(self,queryset):
        return queryset.update(is_superuser = True)

    list_max_show_all = 6

@admin.register(CustomUser)
class UserAdmin(ImportExportActionModelAdmin):
    list_display=['id','username','email','postCount']

    @admin.display(description='Post Count', empty_value= '0')
    def postCount(self, obj):
        return obj.user_post.count()

admin.site.register(Comment)
admin.site.register(Like)
# admin.site.register(CustomUser)
