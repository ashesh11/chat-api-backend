from django.urls import path

from account.views.account import *
from account.views.token import RefreshTokenView

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name='user-logout'),
    path("refresh/", RefreshTokenView.as_view(), name='refresh-token'),
]