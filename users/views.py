from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from content.models import Content
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.services import create_stripe_price, create_stripe_session


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")


class NewPasswordView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "users/new_password.html"
    success_url = reverse_lazy("users:login")


class ProfileView(CreateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')


@login_required
def redirect_to_payment(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    price = create_stripe_price(content)
    session_id, payment_link = create_stripe_session(price)
    user = request.user
    user.payment_id = session_id
    user.save()
    return redirect(payment_link)
