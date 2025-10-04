import qrcode
import base64

from io import BytesIO

from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model


from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

from .forms import RegisterForm, LoginForm


def login_user(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("user_profile", "me")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                user_device = next(devices_for_user(user), None)
                if user_device and user_device.confirmed:
                    request.session["pre_otp_user_id"] = user.id
                    return redirect("verify_otp")
                else:
                    login(request, user)
                    return redirect("user_profile", "me")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
                return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def verify_otp(request: HttpRequest):
    user_id = request.session.get("pre_otp_user_id")
    if not user_id:
        return redirect("login")

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        del request.session["pre_otp_user_id"]
        return redirect("login")

    device = next(devices_for_user(user), None)

    if request.method == "POST":
        token = request.POST.get("otp_token", "")

        if device and device.verify_token(token):
            login(request, user)

            if "pre_otp_user_id" in request.session:
                del request.session["pre_otp_user_id"]

            return redirect("user_profile", "me")
        else:
            messages.error(request, "Неверный код 2FA.")
            return render(request, "verify_otp.html")

    return render(request, "verify_otp.html")


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("setup_2fa")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def logout_user(request: HttpRequest):
    logout(request)
    return render(request, "logout.html")


def setup_2fa(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("login_user")

    if next(devices_for_user(request.user, confirmed=True), None):
        return redirect("user_profile", "me")

    unconfirmed_device = next(devices_for_user(request.user, confirmed=False), None)

    if not unconfirmed_device:
        unconfirmed_device, created = TOTPDevice.objects.get_or_create(
            user=request.user,
            confirmed=False,
            defaults={"name": f"TOTP Device for {request.user.username}"},
        )

    if request.method == "POST":
        token = request.POST.get("otp_token", "")
        if unconfirmed_device.verify_token(token):
            unconfirmed_device.confirmed = True
            unconfirmed_device.save()

            messages.success(request, "2FA успешно настроена и подтверждена!")
            return redirect("user_profile", "me")
        else:
            messages.error(request, "Неверный код. Попробуйте снова.")

    qr_url = unconfirmed_device.config_url
    qr = qrcode.make(qr_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(
        request,
        "setup_2fa.html",
        {
            "qr_image_base64": qr_image_base64,
            "device": unconfirmed_device,
        },
    )
