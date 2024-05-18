from django.conf import settings
from django.shortcuts import render
from apps.cart_app.models import UserOrder
from apps.cart_app.sms_module import send_verify_order_sms
import requests
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt
import logging
import datetime
import os
import pytz
import rsa
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

# requests pakckage
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


CallbackURL = 'https://hmelecteronic.ir/payment-gateway/verify/'


IRAN_KISH = {
    'get_token_url': 'https://ikc.shaparak.ir/api/v3/tokenization/make',
    'post_and_redirect_url': 'https://ikc.shaparak.ir/iuiv3/IPG/Index/',
    'confirmation_url': 'https://ikc.shaparak.ir/api/v3/confirmation/purchase',
    'call_back_url': CallbackURL,
    'terminal_id': 'your terminal ID',
    'acceptor_id': 'your acceptor ID',
    'pass_phrase': 'your pass phrase',
    'sha1_key': 'PUT YOUR SHA1_KEY  HERE',
    'rsa_public_key_file': settings.RSI_PUBLIC_KEY,
    'post_and_redirect_token_key': 'tokenIdentity'
}


# load the rsa public key
with open(IRAN_KISH['rsa_public_key_file'], mode='rb') as private_file:
    rsa_public_key_data = private_file.read()
rsa_public_key = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_public_key_data)


def get_token(amount: int, order_id: int):
    aes_key, aes_iv = os.urandom(16), os.urandom(16)
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    byte_array_data = bytearray(48)
    byte_array_data[0:16], byte_array_data[16:48] = aes_key, \
                                                    bytearray(
                                                        SHA256.new(
                                                            aes.encrypt(
                                                                pad(
                                                                    bytes(
                                                                        bytearray.fromhex(
                                                                            IRAN_KISH['terminal_id'] +
                                                                            IRAN_KISH['pass_phrase'] +
                                                                            str(amount).zfill(12) +
                                                                            '00'
                                                                        )
                                                                    ),
                                                                    16
                                                                )
                                                            )
                                                        ).digest()
                                                    )
    authentication_envelope = {
        'iv': aes_iv.hex(),
        'data': rsa.encrypt(byte_array_data, rsa_public_key).hex()
    }

    request_headers = {
        'transactionType': 'Purchase',
        'terminalId': IRAN_KISH['terminal_id'],
        'acceptorId': IRAN_KISH['acceptor_id'],
        'amount': amount,
        'revertUri': IRAN_KISH['call_back_url'],
        'requestId': str(order_id),
        'requestTimestamp': int(datetime.datetime.timestamp(datetime.datetime.now(tz=pytz.UTC)))
    }

    payload = {
        'authenticationEnvelope': authentication_envelope,
        'request': request_headers
    }

    r = requests.post(IRAN_KISH['get_token_url'], json=payload, verify=False)
    if r.ok:
        result = r.json()
        if result['responseCode'] == '00':
            logging.info(f'SUCCESSFULLY GOT THE TOKEN , ORDER-ID:{order_id}')
            return result['result']['token']
    logging.warning(f'GET TOKEN ERROR, RESULT: {r.json()}, ORDER-ID: {order_id}')
    return False


@csrf_exempt
def verify(request):
    response_code = request.POST.get('responseCode')
    reference_id = request.POST.get('systemTraceAuditNumber')
    if response_code == '00':
        user_order_id = request.session.get('user_order')
        try:
            user_order = UserOrder.objects.get(id=user_order_id)
        except UserOrder.DoesNotExist:
            logging.warning(f'Verify order Error - User Order does not exists - RefID: {reference_id}')
            user_order = None
        payload = {
            'terminalId': IRAN_KISH['terminal_id'],
            'retrievalReferenceNumber': request.POST.get('retrievalReferenceNumber'),
            'systemTraceAuditNumber': reference_id,
            'merchantId': request.POST.get('merchantID'),
            'acceptorId': request.POST.get('acceptorId'),
            'tokenIdentity': request.POST.get('token'),
        }
        r = requests.post(IRAN_KISH['confirmation_url'], json=payload, verify=False)
        if r.ok:
            result = r.json()
            if result['status']:
                context = {'RefID': reference_id}
                if user_order:
                    user_order.is_paid = True
                    user_order.reference_id = reference_id
                    send_verify_sms = send_verify_order_sms.apply_async(
                        (user_order.phone, reference_id),
                        retry=False,
                        ignore_result=False,
                        expires=20
                    )
                    sms_result = AsyncResult(send_verify_sms.task_id)
                    try:
                        get_sms_result = sms_result.get(timeout=30)
                        logging.warning(get_sms_result['message'])
                        if get_sms_result['status']:
                            user_order.is_sms_sent = True
                        else:
                            user_order.is_sms_sent = False
                    except TimeoutError as e:
                        logging.warning("Send Confirm SMS Task has not completed within the specified timeout")
                        sms_result.forget()
                        user_order.is_sms_sent = False
                    user_order.save()
                    context['date'] = user_order.created_at
                    context['order_id'] = user_order_id
                    context['total_price'] = user_order.total_price
                return render(request, 'zarinpal_app/success.html', context)
            else:
                logging.warning(f'Verify Order Confirmation Error, STATUS:{r.json()}, ORDER-ID:{user_order_id}')
                return render(request, 'zarinpal_app/fail.html', {'status': 'VOCE'})
        else:
            logging.warning(f'Verify Order Confirmation Error, Request-Result:{r.json()}, ORDER-ID:{user_order_id}')
            return render(request, 'zarinpal_app/fail.html', {'status': 'VOCE'})  # Verify Order Confirmation Error
    else:
        logging.warning(f'Verify Order Transaction Canceled, RESPONSE-CODE:{response_code}')
        return render(request, 'zarinpal_app/fail.html', {'status': 'CT'})  # Canceled Transaction
