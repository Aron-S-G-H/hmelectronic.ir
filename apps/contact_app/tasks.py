from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from celery import shared_task
from django.contrib.auth import get_user_model
from jalali_date import datetime2jalali


@shared_task
def send_confirm_email_admins(date):
    user_model = get_user_model()
    admins = user_model.objects.filter(is_superuser=True, email='aronesadegh@gmail.com')
    email = [admin.email for admin in admins]
    date_jalali = datetime2jalali(date).strftime('%Y/%m/%d - %H:%M')
    try:
        send_mail(
            subject='پیام جدید',
            message=f'{date_jalali}پیام جدیدی از طریق سایت ثبت شده است . بخش پیام ها را بررسی کنید . ',
            from_email=settings.EMAIL_HOST_USER, recipient_list=email
        )
        return 'Successfully Sent'
    except:
        return 'Email Failed'


@shared_task
def send_email_users(subject, message, file_url, read_file, user_email):
    try:
        if message and file_url and read_file:
            email = EmailMessage(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[user_email])
            email.attach(file_url, read_file)
            email.send()
        else:
            if message:
                email = EmailMessage(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[user_email])
            elif file_url and read_file:
                email = EmailMessage(subject=subject, body='فایل', from_email=settings.EMAIL_HOST_USER, to=[user_email])
                email.attach(file_url, read_file)
            else:
                return 'email failed'
            email.send()
        return 'email sent'
    except Exception as e:
        exception_name = type(e).__name__
        exception_message = e.args[0].decode()
        return f'{exception_name} : {exception_message}'
