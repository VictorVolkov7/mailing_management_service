from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, CreateView, TemplateView

from users.forms import LoginForm, ProfileForm, RegisterForm
from users.models import User
from users.services import send_email


class LoginView(BaseLoginView):
    model = User
    form_class = LoginForm
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class UserUpdateView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:verify_email', kwargs={'uidb64': uid, 'token': token})

        send_email(activation_url, user.email)

        return redirect('users:verified')


class VerifiedSentView(TemplateView):
    template_name = 'users/verify_sent.html'


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        group = Group.objects.get(name='group_user')
        request.user.groups.add(group)

        return redirect('mailing:home_page')
    else:
        return redirect('users:login')
