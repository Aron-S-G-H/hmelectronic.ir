from kavenegar import *
from django.conf import settings
from celery import shared_task


# send OTP sms (needs template)
@shared_task
def send_otp_sms(phone_number: str, code: int):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': settings.KAVENEGAR_OTP_TEMPLATENAME,
            'token': code,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params=params)
        return {'status': True, 'message': f'OTP sms sent successfully to {response[0]["receptor"]}'}
    except APIException as AE:
        exception_name = type(AE).__name__
        exception_message = AE.args[0].decode()
        return {'status': False, 'message': f'OTP {exception_name} error : {exception_message}'}
    except HTTPException as HE:
        exception_name = type(HE).__name__
        exception_message = HE.args[0].decode()
        return {'status': False, 'message': f'OTP {exception_name} error : {exception_message}'}
    

@shared_task
def send_verify_order_sms(phone_number, ref_id):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': settings.KAVENEGAR_VERIFYORDER_TEMPLATENAME,
            'token': ref_id,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params=params)
        return {'status': True, 'message': f'Verify order sms sent successfully to {response[0]["receptor"]}'}
    except APIException as AE:
        exception_name = type(AE).__name__
        exception_message = AE.args[0].decode()
        return {'status': False, 'message': f'Verify order sms {exception_name} error : {exception_message}'}
    except HTTPException as HE:
        exception_name = type(HE).__name__
        exception_message = HE.args[0].decode()
        return {'status': False, 'message': f'Verify order sms {exception_name} error : {exception_message}'}
