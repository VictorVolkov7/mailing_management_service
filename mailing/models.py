from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    surname = models.CharField(max_length=50, **NULLABLE, verbose_name='отчество')
    message = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    mail_subject = models.CharField(max_length=150, verbose_name='тема письма')
    mail_body = models.TextField(verbose_name='тело письма', **NULLABLE)

    def __str__(self):
        return f'{self.mail_subject}'

    class Meta:
        verbose_name = 'сообщение рассылки'
        verbose_name_plural = 'сообщения рассылки'


class Settings(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('mailing', 'Идет отправка'),
        ('completed', 'Завершена'),
    )
    WEEKDAY = (
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье'),
    )

    mailing_name = models.CharField(max_length=20, verbose_name='название рассылки', **NULLABLE)
    mailing_time_start = models.TimeField(verbose_name='время начала рассылки')
    mailing_time_end = models.TimeField(verbose_name='время окончания рассылки')
    preferred_weekday = models.CharField(max_length=11, choices=WEEKDAY, verbose_name='день недели', **NULLABLE)
    preferred_day_of_month = models.IntegerField(choices=[(day, day) for day in range(1, 32)],
                                                 verbose_name='день месяца', **NULLABLE)
    periodicity = models.CharField(max_length=150, choices=FREQUENCY_CHOICES, verbose_name='периодичность рассылки')
    mailing_status = models.CharField(max_length=150, choices=STATUS_CHOICES, default='created',
                                      verbose_name='статус рассылки')

    mailing = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тема и тело рассылки')
    client = models.ManyToManyField(Client, related_name='mailings', verbose_name='клиенты')

    def __str__(self):
        return f'{self.mailing_name}'

    class Meta:
        verbose_name = 'рассылка/настройка'
        verbose_name_plural = 'рассылки/настройка'


class Logs(models.Model):
    MAILING_STATUS = (
        ('failed', 'не отправлено'),
        ('excellent', 'отправлено'),
    )

    mailing_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    mailing_status = models.CharField(max_length=50, choices=MAILING_STATUS, verbose_name='статус попытки')
    mail_server_response = models.CharField(max_length=150, **NULLABLE, verbose_name='ответ почтового сервера')

    mailing = models.ForeignKey(Settings, on_delete=models.CASCADE, verbose_name='настройка рассылки')

    def __str__(self):
        return f'{self.mailing_status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
