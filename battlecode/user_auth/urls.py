from django.urls import path

from .views import login_user, logout_user, register, verify_otp, setup_2fa

urlpatterns = [
    path("login/", login_user, name="login"),
    path("login/verify", verify_otp, name="verify_otp"),
    path("register/", register, name="register"),
    path("logout/", logout_user, name="logout"),
    path("setup-2fa/", setup_2fa, name="setup_2fa"),
]

