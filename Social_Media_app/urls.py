from django.urls import path , include
from . import views
from .views import Registerview ,loginview ,logout_view,remove_like
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post',views.Postview,basename='Post')
router.register(r'comment',views.Commentview,basename='Comment')
router.register(r'like',views.Likeview,basename='Like')

urlpatterns = [
    path('',views.Home,name='Home'),
    path('login/',loginview.as_view(),name='login'),
    path('register/',Registerview.as_view(),name='Register'),
    path('logout/',logout_view.as_view(),name='logout'),
    path('',include(router.urls)),
    path('Unlike/',remove_like.as_view(),name='Unlike'),
]
