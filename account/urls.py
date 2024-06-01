from django.urls import path

from account.views import *

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("refresh/", RefreshTokenView.as_view(), name='refresh-token')
]