from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import SettingsForm, ClientForm, MessageForm
from mailing.models import Settings, Client, Message
from mailing.services import get_cached_blogs


class PermissionMixin:
    def __init__(self):
        self.object = None

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class HomePageTemplateView(TemplateView):
    template_name = 'mailing/home_page.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        blog_list = get_cached_blogs()

        context_data['blogs'] = blog_list

        return context_data


class SettingsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Settings
    extra_context = {'title': 'Рассылки'}
    permission_required = 'mailing.view_settings'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['mailing_list'] = self.get_queryset()
        context_data['active_mailing'] = Settings.objects.filter(mailing_status__in=['running', 'mailing'],
                                                                 owner=self.request.user)

        context_data['unique_users'] = Client.objects.filter(owner=self.request.user)

        context_data['message_list'] = Message.objects.filter(owner=self.request.user)

        return context_data


class SettingsDetailView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, DetailView):
    model = Settings
    permission_required = 'mailing.view_settings'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Рассылка {self.object.mailing_name}'
        return context_data


class SettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Settings
    form_class = SettingsForm
    permission_required = 'mailing.add_settings'
    extra_context = {'title': 'Добавление рассылки'}
    success_url = reverse_lazy('mailing:settings_list')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def form_valid(self, form):
        form.instance.owner = self.request.user

        self.object = form.save(commit=False)
        if self.object.periodicity == 'daily':
            self.object.preferred_weekday = None
            self.object.preferred_day_of_month = None
        elif self.object.periodicity == 'weekly':
            self.object.preferred_day_of_month = None
        else:
            self.object.preferred_weekday = None

        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class SettingsUpdateView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Settings
    form_class = SettingsForm
    permission_required = 'mailing.change_settings'
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'{self.object.mailing_name} редактирование'
        return context_data

    def get_success_url(self):
        return reverse('mailing:settings_detail', args=[self.kwargs.get('pk')])


class SettingsDeleteView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Settings
    permission_required = 'mailing.delete_settings'
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление {self.object.mailing_name} '
        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    extra_context = {'title': 'Клиенты'}
    permission_required = 'mailing.view_client'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.add_client'
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {'title': 'Добавление клиента'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.change_client'
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {'title': 'Редактирование клиента'}


class ClientDeleteView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'mailing.delete_client'
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {'title': 'Удаление клиента'}


class MessageDetailView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, DetailView):
    model = Message
    permission_required = 'mailing.view_message'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Сообщение {self.object.mail_subject}'
        return context_data


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.add_message'
    success_url = reverse_lazy('mailing:settings_list')
    extra_context = {'title': 'Создание сообщения'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.change_message'
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'{self.object.mail_subject} редактирование'
        return context_data


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'mailing.delete_message'
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление {self.object.mail_subject}'
        return context_data


@login_required
def toggle_activity(request, pk):
    mailing_settings = get_object_or_404(Settings, pk=pk)

    if mailing_settings.mailing_status == 'created':
        mailing_settings.mailing_status = 'running'
    elif mailing_settings.mailing_status == 'running':
        mailing_settings.mailing_status = 'completed'
    elif mailing_settings.mailing_status == 'completed':
        mailing_settings.mailing_status = 'running'

    mailing_settings.save()

    return redirect('mailing:settings_list')
