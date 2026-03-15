from django.urls import path

from .views import (SignUpView,LoginView,LogoutView,ProfileView,ProfileUpdateView,AvatarUploadView,ChangePasswordView)

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/avatar/", AvatarUploadView.as_view(), name="avatar_upload"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

]