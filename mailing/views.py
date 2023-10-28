from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import SettingsForm, ClientForm, MessageForm
from mailing.models import Settings, Client, Message, Logs


class HomePageTemplateView(TemplateView):
    template_name = 'mailing/home_page.html'
    extra_context = {'title': 'Главная'}


class SettingsListView(ListView):
    model = Settings
    extra_context = {'title': 'Рассылки'}

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        Logs.objects.all()

        mailing_list = Settings.objects.all()
        context_data['mailing_list'] = mailing_list

        message_list = Message.objects.all()
        context_data['message_list'] = message_list

        return context_data


class SettingsDetailView(DetailView):
    model = Settings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Рассылка {self.object.mailing_name}'
        return context_data


class SettingsCreateView(CreateView):
    model = Settings
    form_class = SettingsForm
    extra_context = {'title': 'Добавление рассылки'}
    success_url = reverse_lazy('mailing:settings_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.periodicity == 'daily':
            self.object.preferred_weekday = None
            self.object.preferred_day_of_month = None
        elif self.object.periodicity == 'weekly':
            self.object.preferred_day_of_month = None
        else:
            self.object.preferred_weekday = None
        self.object.save()
        return super().form_valid(form)


class SettingsUpdateView(UpdateView):
    model = Settings
    form_class = SettingsForm
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'{self.object.mailing_name} редактирование'
        return context_data

    def get_success_url(self):
        return reverse('mailing:settings_detail', args=[self.kwargs.get('pk')])


class SettingsDeleteView(DeleteView):
    model = Settings
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление {self.object.mailing_name} '
        return context_data


class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Клиенты'}


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {'title': 'Добавление клиента'}


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {'title': 'Редактирование клиента'}


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {'title': 'Удаление клиента'}


class MessageDetailView(DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Сообщение {self.object.mail_subject}'
        return context_data


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:settings_list')
    extra_context = {'title': 'Создание сообщения'}


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'{self.object.mail_subject} редактирование'
        return context_data


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:settings_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление {self.object.mail_subject}'
        return context_data


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
