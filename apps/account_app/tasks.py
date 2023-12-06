from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Otp


@shared_task
def send_email(random_code: int, user_email: str):
    try:
        send_mail(
            subject='کد ورود',
            message=f'کد ورود شما به اچ ام الکترونیک: {random_code}',
            from_email=settings.EMAIL_HOST_USER, recipient_list=[user_email]
        )
        return {'status': True, 'message': f'Forgot password email sent successfully to : {user_email}'}
    except Exception as e:
        exception_name = type(e).__name__
        exception_message = e.args[0].decode()
        return {'status': False, 'message': f'Forgot password email {exception_name} error : {exception_message}'}


@shared_task
def create_otp(data, random_code, token):
    try:
        response = Otp.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password'],
            code=random_code,
            token=token,
        )
        return f'OTP create successfully : {response}'
    except Exception as e:
        exception_name = type(e).__name__
        exception_message = e.args[0].decode()
        return f'OTP create {exception_name} error : {exception_message}'
