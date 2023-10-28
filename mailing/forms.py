from django import forms

from mailing.models import Settings, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = (
            'mailing_name', 'mailing_time_start', 'mailing_time_end', 'periodicity', 'preferred_weekday',
            'preferred_day_of_month', 'mailing', 'client',
        )


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'last_name', 'first_name', 'surname', 'message',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
