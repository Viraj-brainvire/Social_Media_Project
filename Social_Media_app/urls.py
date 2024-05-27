from django.urls import path , include
from . import views
from .views import Registerview , Postview ,Commentview
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post',views.Postview,basename='Post')
router.register(r'comment',views.Commentview,basename='Comment')
router.register(r'like',views.Likeview,basename='Like')

urlpatterns = [
    path('',views.Home,name='Home'),
    path('login/',obtain_auth_token,name='login'),
    path('register/',Registerview.as_view(),name='Register'),
    path('logout/',views.logout_view,name='logout'),
    path('',include(router.urls)),
    # path('Post/',Postview.as_view(),name="Post"),
    # path('Comment/',Commentview.as_view(),name="Comment"),
]
