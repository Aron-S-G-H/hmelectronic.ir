from django.conf import settings
from django.shortcuts import render, redirect
from apps.cart_app.models import UserOrder
from django.shortcuts import get_object_or_404
from apps.cart_app.sms_module import send_verify_order_sms
import requests
import json
from celery.result import AsyncResult
import logging

ZP_API_REQUEST = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش "  # Required
CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/'


def send_request(request):
    user_order_id = request.session.get('user_order')
    user_order = get_object_or_404(UserOrder, id=user_order_id)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": user_order.total_price + 0,
        "Description": description,
        "Phone": user_order.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    request_headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'content-length': str(len(data))
    }
    try:
        response = requests.post(url=ZP_API_REQUEST, data=data, headers=request_headers, timeout=20)
        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                logging.info(f'Successfully Redirected to Zarinpal, OrderID:{user_order_id}')
                return redirect(ZP_API_STARTPAY + authority)
            elif response_json['Status'] == -1:
                logging.warning(f'Zarinpal Send Request Response Error, OrderID:{user_order_id}')
                context = {
                    'stage': 'send_request',
                    'status': 'SRRE'  # Send Request Response Error
                }
                return render(request, 'zarinpal_app/response.html', context)
        else:
            logging.warning(f'Zarinpal Send Request Response Status Error, OrderID:{user_order_id}')
            context = {
                'stage': 'send_request',
                'status': 'SRSE'  # Send Request Status Error
            }
            return render(request, 'zarinpal_app/response.html', context)
    except requests.exceptions.Timeout:
        logging.warning(f'Zarinpal Send Request Timeout Error, OrderID:{user_order_id}')
        context = {
            'stage': 'send_request',
            'status': 'TE'  # Timeout Error
        }
        return render(request, 'zarinpal_app/response.html', context)
    except requests.exceptions.ConnectionError:
        logging.warning(f'Zarinpal Send Request Connection Error, OrderID:{user_order_id}')
        context = {
            'stage': 'send_request',
            'status': 'CE'  # Connection Error
        }
        return render(request, 'zarinpal_app/response.html', context)


def verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    user_order_id = request.session.get('user_order')
    user_order = get_object_or_404(UserOrder, id=user_order_id)
    if status == 'OK' and authority:
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": user_order.total_price + 0,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(url=ZP_API_VERIFY, data=data, headers=headers, timeout=20)
        if response.status_code == 200:
            response_json = response.json()
            try:
                reference_id = response_json['RefID']
                if response_json['Status'] == 100:
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
                        logging.warning("Send OTP SMS Task has not completed within the specified timeout")
                        sms_result.forget()
                        user_order.is_sms_sent = False
                    user_order.save()
                    context = {
                        'stage': 'verify',
                        'status': 'SF',  # Successful
                        'RefID': reference_id
                    }
                    return render(request, 'zarinpal_app/response.html', context)
                else:
                    logging.warning(f'Verify Order Transaction Error, Status:{response_json["Status"]}, OrderID:{user_order_id}')
                    context = {
                        'stage': 'verify',
                        'status': 'TSE'  # Transaction Status Error
                    }
                    return render(request, 'zarinpal_app/response.html', context)
            except requests.exceptions.Timeout:
                logging.warning(f'Verify Order Response TimeOut Error, OrderID:{user_order_id}')
                context = {
                    'stage': 'verify',
                    'status': 'TE'  # Timeout Error
                }
                return render(request, 'zarinpal_app/response.html', context)
            except requests.exceptions.ConnectionError:
                logging.warning(f'Verify Order Response Connection Error, OrderID:{user_order_id}')
                context = {
                    'stage': 'verify',
                    'status': 'CE'  # Connection Error
                }
                return render(request, 'zarinpal_app/response.html', context)
        else:
            logging.warning(f'Verify Order Response Error, Response Status:{response.status_code}, OrderID:{user_order_id}')
            context = {
                'stage': 'verify',
                'status': 'RSE',  # Response Status Error
            }
            return render(request, 'zarinpal_app/response.html', context)
    else:
        logging.warning(f'Verify Order Transaction canceled, Status:{status}, OrderID:{user_order_id}')
        context = {
            'stage': 'verify',
            'status': 'CT'  # Canceled Transaction
        }
        return render(request, 'zarinpal_app/response.html', context)
