from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from content.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number", "password1", "password2")


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ("avatar", "username", "tg_nickname", "phone_number", "email", "password")
