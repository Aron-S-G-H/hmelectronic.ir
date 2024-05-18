import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Otp
from .forms import LoginForm, ForgotPasswordForm, RegisterForm
from apps.cart_app.sms_module import send_otp_sms
from .tasks import send_email, create_otp
from random import randint
from uuid import uuid4
from celery.result import AsyncResult


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        login_form = LoginForm()
        forgot_password_form = ForgotPasswordForm()
        context = {'loginForm': login_form, 'forgot_password': forgot_password_form}
        return render(request, 'account_app/login.html', context=context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(username=data['phone'], password=data['password'])
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 200, 'firstName': user.first_name, 'lastName': user.last_name})
            return JsonResponse({'status': 401})
        errors = {field: error for field, errors in login_form.errors.items() for error in errors}
        field = list(errors.keys())[0]
        error_message = list(errors.values())[0]
        logging.warning(f'login error:{request.POST["phone"]}, field: {field}, message: {error_message}')
        return JsonResponse({'status': 400, 'error_message': error_message})


class ForgotPasswordView(View):
    def get(self, request):
        code = request.GET.get('code')
        if code and code.isdigit():
            try:
                user = CustomUser.objects.get(one_time_password=code)
            except Exception as e:
                return JsonResponse({'status': 401, 'err': 'کد وارد شده نادرست است !'})
            login(request, user)
            user.one_time_password = 0
            user.save()
            return JsonResponse({'status': 200, 'firstName': user.first_name, 'lastName': user.last_name})
        else:
            return JsonResponse({'status': 400, 'err': 'کد نامعتبر است!'})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=user_email)
            except Exception as e:
                logging.warning(e)
                return JsonResponse({'status': 401})

            random_code = randint(10000, 30000)
            user.one_time_password = random_code
            user.save()
            email = send_email.delay(random_code, user_email)
            email_result = AsyncResult(email.task_id)
            try:
                get_email_result = email_result.get(timeout=15)
                logging.info(get_email_result['message'])
                if not get_email_result['status']:
                    return JsonResponse({'status': 400, 'err': 'خطا در ارسال ایمیل !'})
            except TimeoutError as e:
                logging.warning(f'Send forgot password email {user_email} has not completed within the specified timeout')
                email_result.forget()
                return JsonResponse({'status': 400, 'err': 'خطا در ارسال ایمیل !'})
            return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 400, 'err': 'فرم معتبر نمی باشد !'})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = RegisterForm()
        return render(request, 'account_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] != data['confirm_pass']:
                form.add_error('password', 'گذرواٰژه های یکسان نیستند')
            elif CustomUser.objects.filter(phone=data['phone']).exists():
                form.add_error(None, 'کاربری با این مشخصات ثبت شده است !')
            else:
                random_code = randint(10000, 30000)
                token = str(uuid4())
                sms_send = send_otp_sms.apply_async(
                    (data['phone'], random_code),
                    retry=False,
                    ignore_result=False,
                    expires=20
                )
                sms_result = AsyncResult(sms_send.task_id)
                try:
                    get_sms_result = sms_result.get(timeout=30)
                    logging.warning(get_sms_result['message'])
                    if not get_sms_result['status']:
                        form.add_error(None, 'سرویس OTP با خطا مواجه شد . شماره تلفن خود را با اعداد انگلیسی وارد کنید و دوباره تلاش کنید . درصورت برطرف نشدن مشکل با پشتیبانی تماس بگیرید .')
                        return render(request, 'account_app/register.html', {'form': form})
                except TimeoutError as e:
                    logging.warning("Send OTP SMS Task has not completed within the specified timeout")
                    sms_result.forget()
                otp = create_otp.apply_async(
                    (data, random_code, token),
                    retry=False,
                    ignore_result=False,
                    expires=10,
                )
                create_otp_result = AsyncResult(otp.task_id)
                try:
                    logging.warning(create_otp_result.get(timeout=30))
                except TimeoutError as e:
                    logging.warning("Create OTP Task has not completed within the specified timeout")
                    create_otp_result.forget()
                return redirect(reverse('account:checkOtp_page') + f'?token={token}')
        return render(request, 'account_app/register.html', {'form': form})


class CheckOtp(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        token = request.GET.get('token', None)
        if token is None:
            return redirect('account:Login_page')
        return render(request, 'account_app/check_otp.html')

    def post(self, request):
        token = request.POST.get('token')
        code = request.POST.get('code')
        if token and code:
            try:
                new_user = Otp.objects.get(token=token, code=code)
                user = CustomUser.objects.create_user(
                    first_name=new_user.first_name,
                    last_name=new_user.last_name,
                    email=new_user.email if new_user.email else None,
                    phone=int(new_user.phone),
                    password=new_user.password
                )
                login(request, user)
                new_user.delete()
                return JsonResponse({'status': 200, 'fName': user.first_name, 'lName': user.last_name})
            except Exception as e:
                logging.warning(e)
                return JsonResponse({'status': 400, 'errMessage': 'کد یا توکن نامعتبر است !'})
        else:
            return JsonResponse({'status': 400, 'errMessage': 'فرم نامعتبر است !'})
