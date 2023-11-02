from django import forms

from mailing.models import Settings, Client, Message


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SettingsForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)

        self.fields['client'].queryset = Client.objects.filter(owner=user)
        self.fields['mailing'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Settings
        fields = (
            'mailing_name', 'mailing_time_start', 'mailing_time_end', 'periodicity', 'preferred_weekday',
            'preferred_day_of_month', 'mailing', 'client',
        )

    def clean(self):
        cleaned_data = super().clean()
        mailing_time_start = cleaned_data.get('mailing_time_start')
        mailing_time_end = cleaned_data.get('mailing_time_end')

        if mailing_time_end < mailing_time_start:
            raise forms.ValidationError('Время окончания рассылки не может быть меньше времени начала рассылки')

        return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'last_name', 'first_name', 'surname', 'message',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    BANWORD = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Message
        exclude = ('owner',)

    def clean_mail_body(self):
        cleaned_data = self.cleaned_data.get('mail_body')

        if cleaned_data in MessageForm.BANWORD:
            raise forms.ValidationError('Присутствуют запрещенные слова в описании')

        return cleaned_data

    def clean_mail_subject(self):
        cleaned_data = self.cleaned_data.get('mail_subject')

        if cleaned_data in MessageForm.BANWORD:
            raise forms.ValidationError('Присутствуют запрещенные слова в описании')

        return cleaned_data
