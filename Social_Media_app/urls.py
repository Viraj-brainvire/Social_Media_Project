from django.urls import path , include
from . import views
from .views import Registerview ,loginview ,logout_view,remove_like
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from django.contrib import admin

router = DefaultRouter()
router.register(r'post',views.Postview,basename='Post')
router.register(r'comment',views.Commentview,basename='Comment')
router.register(r'like',views.Likeview,basename='Like')

urlpatterns = [
    path('',views.Home,name='Home'),
    path('home/',views.home,name='home1'),
    path('login/',loginview.as_view(),name='login'),
    path('register/',Registerview.as_view(),name='Register'),
    path('logout/',logout_view.as_view(),name='logout'),
    path('',include(router.urls)),
    path('Unlike/',remove_like.as_view(),name='Unlike'),
    # path(
    # "admin/password_reset/",
    # auth_views.PasswordResetView.as_view(
    #     extra_context={"site_header": admin.site.site_header}
    # ),
    # name="admin_password_reset",
    # ),
    # path(
    #     "admin/password_reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(
    #         extra_context={"site_header": admin.site.site_header}
    #     ),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(
    #         extra_context={"site_header": admin.site.site_header}
    #     ),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     auth_views.PasswordResetCompleteView.as_view(
    #         extra_context={"site_header": admin.site.site_header}
    #     ),
    #     name="password_reset_complete",
    # ),
]

