from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import UserCreateView, NewPasswordView, ProfileView, redirect_to_payment

app_name = UsersConfig.name
urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path('new_password/', NewPasswordView.as_view(), name='new_password'),
    path("paymentstripe/", redirect_to_payment, name="paymentstripe"),
    path('profile/', ProfileView.as_view(), name='profile'),
]
