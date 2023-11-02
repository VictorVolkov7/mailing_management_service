from django.contrib import admin

from mailing.models import Client, Settings, Message, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'surname', 'message', 'owner')


@admin.register(Settings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'mailing_name', 'mailing_time_start', 'mailing_time_end', 'periodicity', 'mailing_status', 'mailing', 'owner',
    )


@admin.register(Message)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('mail_subject', 'mail_body', 'owner',)


@admin.register(Logs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'mailing_status', 'mail_server_response', 'mailing',)
