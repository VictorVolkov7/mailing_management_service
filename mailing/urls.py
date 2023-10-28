from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (HomePageTemplateView, SettingsListView, SettingsDetailView, SettingsCreateView,
                           SettingsUpdateView, SettingsDeleteView, ClientListView, ClientCreateView, ClientUpdateView,
                           ClientDeleteView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
                           toggle_activity)

app_name = MailingConfig.name

urlpatterns = [
    path('', HomePageTemplateView.as_view(), name='home_page'),
]

mailing_urls = [
    path('mailing/', SettingsListView.as_view(), name='settings_list'),
    path('mailing/<int:pk>', SettingsDetailView.as_view(), name='settings_detail'),
    path('mailing/create/', SettingsCreateView.as_view(), name='settings_create'),
    path('mailing/update/<int:pk>', SettingsUpdateView.as_view(), name='settings_update'),
    path('mailing/delete/<int:pk>', SettingsDeleteView.as_view(), name='settings_delete'),
    path('activity/<int:pk>', toggle_activity, name='toggle_activity'),
]

client_urls = [
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
]

message_url = [
    path('mailing/message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('mailing/message/create/', MessageCreateView.as_view(), name='message_create'),
    path('mailing/message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('mailing/message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
]

urlpatterns += mailing_urls + client_urls + message_url
