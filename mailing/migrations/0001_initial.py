# Generated by Django 4.2.6 on 2023-10-26 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('first_name', models.CharField(max_length=50, verbose_name='имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='фамилия')),
                ('surname', models.CharField(blank=True, max_length=50, null=True, verbose_name='отчество')),
                ('message', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_subject', models.CharField(max_length=150, verbose_name='тема письма')),
                ('mail_body', models.TextField(blank=True, null=True, verbose_name='тело письма')),
            ],
            options={
                'verbose_name': 'сообщение рассылки',
                'verbose_name_plural': 'сообщения рассылки',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='название рассылки')),
                ('mailing_time_start', models.TimeField(verbose_name='время начала рассылки')),
                ('mailing_time_end', models.TimeField(verbose_name='время окончания рассылки')),
                ('preferred_weekday', models.CharField(blank=True, choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')], max_length=11, null=True, verbose_name='день недели')),
                ('preferred_day_of_month', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], null=True, verbose_name='день месяца')),
                ('periodicity', models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=150, verbose_name='периодичность рассылки')),
                ('mailing_status', models.CharField(choices=[('created', 'Создана'), ('running', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=150, verbose_name='статус рассылки')),
                ('client', models.ManyToManyField(related_name='mailings', to='mailing.client', verbose_name='клиенты')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='тема и тело рассылки')),
            ],
            options={
                'verbose_name': 'рассылка/настройка',
                'verbose_name_plural': 'рассылки/настройка',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('mailing_status', models.CharField(choices=[('failed', 'ошибка отправки'), ('excellent', 'успешная отправка')], max_length=50, verbose_name='статус попытки')),
                ('mail_server_response', models.CharField(blank=True, max_length=150, null=True, verbose_name='ответ почтового сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.settings', verbose_name='настройка рассылки')),
            ],
            options={
                'verbose_name': 'Лог рассылки',
                'verbose_name_plural': 'Логи рассылки',
            },
        ),
    ]
