from smtplib import SMTPException as smtpException

import django.utils.timezone

from mailing.models import Settings, Logs
from mailing.services import send_email


def send_mailing() -> None:
    """
    Cron функция, для проверки рассылки (запущена и попадание рассылки в нужный диапазон времени)
    и отправки это рассылки пользователям с выбранной ими периодичностью, с последующим созданием логов.
    """
    now = django.utils.timezone.datetime.now()
    # ищем все рассылки, имеющие статус 'running'
    for mailing_settings in Settings.objects.filter(mailing_status__in=['running', 'mailing']):
        # проверяем попадает ли в диапазон времени
        if (mailing_settings.mailing_time_start <= now.time() <= mailing_settings.mailing_time_end and
                mailing_settings.mailing_status == 'running'):
            # собираем все данные для передачи в send_mail()
            clients: list = [client.email for client in mailing_settings.client.all()]
            subject: str = mailing_settings.mailing.mail_subject
            message: str = mailing_settings.mailing.mail_body

            # блок для проверки выбранной периодичности и отправки рассылки
            try:
                if mailing_settings.periodicity == 'daily':
                    send_email(subject, message, clients)
                elif mailing_settings.periodicity == 'weekly' and mailing_settings.preferred_weekday is not None:
                    if now.weekday() == int(mailing_settings.preferred_weekday):
                        send_email(subject, message, clients)
                elif mailing_settings.periodicity == 'monthly' and mailing_settings.preferred_day_of_month is not None:
                    if now.day == mailing_settings.preferred_day_of_month:
                        send_email(subject, message, clients)

                # создание и сохранение логов
                log = Logs.objects.create(
                    mailing_status='excellent',
                    mail_server_response='Успех',
                    mailing=mailing_settings,
                )
                log.save()

            except smtpException as error:
                log = Logs.objects.create(
                    mailing_status='failed',
                    mail_server_response=f'Ошибка почтового сервера: {str(error)}',
                    mailing=mailing_settings,
                )
                log.save()

            # меняем статус на 'mailing' после отправки
            mailing_settings.mailing_status = 'mailing'
            mailing_settings.save()

        # меняем статус на 'running' после времени окончания рассылки
        elif now.time() > mailing_settings.mailing_time_end and mailing_settings.mailing_status == 'mailing':
            mailing_settings.mailing_status = 'running'
            mailing_settings.save()
