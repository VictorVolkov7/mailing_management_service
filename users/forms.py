from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from mailing.forms import StyleFormMixin
from users.models import User
from django import forms


class LoginForm(StyleFormMixin, AuthenticationForm):

    class Meta:
        model = User


class ProfileForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class RegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
