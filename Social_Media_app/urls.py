from django.urls import path
from . import views
from .views import Registerview
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',views.Home,name='Home'),
    path('login/',obtain_auth_token,name='login'),
    path('register/',Registerview.as_view(),name='Register'),
    path('logout/',views.logout_view,name='logout')

]
