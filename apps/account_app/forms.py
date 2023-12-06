from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.core import validators


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = CustomUser
        fields = '__all__'


_persian_to_english = {
    "۰": '0',
    "۱": '1',
    "۲": '2',
    "۳": '3',
    "۴": '4',
    "۵": '5',
    "۶": '6',
    "۷": '7',
    "۸": '8',
    "۹": '9'
}

invalid_chars = (
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-',
    '+', '=', '|', '{', '}', '[', ']', '/', '?', '>', '<', ':',
    ';', ',', '.', '~', '`',
)

farsi_digits = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')


def persian_to_english(number):
    print(number)
    changed_number = str()
    for i in number:
        item = _persian_to_english.get(i)
        if item:
            changed_number += item
        else:
            changed_number += i
    print(changed_number)
    return changed_number


def fullname_validator(value):
    for char in invalid_chars:
        if char in value:
            raise forms.ValidationError('لطفا از کاراکتر های غبر مجاز استفاده نکنید !')
    for item in range(0, 10):
        if str(item) in value:
            raise forms.ValidationError('لطفا نام معتبر وارد کنید !')


class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'name': 'phone', 'placeholder': 'شماره موبایل خود را وارد کنید ...'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'name': 'password', 'placeholder': 'رمز خود را وارد کنید ...'}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if '+' in phone:
            raise forms.ValidationError('شماره همراه معتبر نیست . شماره همراه خود را بدون ۹۸+ وارد کنید')
        elif len(phone) != 11:
            raise forms.ValidationError('شماره همراه باید ۱۱ عدد باشد')
        else:
            try:
                int(phone)
            except ValueError:
                raise forms.ValidationError('شماره همراه معتبر نمی باشد')
        return phone


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'name': 'email', 'placeholder': 'ایمیل خود را وارد کنید ...'}))


class RegisterForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'name': 'firstname', 'placeholder': 'نام'}),
        validators=[fullname_validator]
    )
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'name': 'lastname', 'placeholder': 'نام خانوادگی'}),
        validators=[fullname_validator]
    )
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'name': 'email', 'placeholder': 'آدرس ایمیل ( اختیاری )'}),
        validators=[validators.EmailValidator()]
    )
    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'name': 'phone', 'placeholder': 'شماره موبایل'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'password': 'password', 'placeholder': 'رمز'}),
        validators=[validators.MinLengthValidator(5)]
    )
    confirm_pass = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'name': 'confirmPassword', 'placeholder': 'تکرار رمز عبور'})
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if '+' in phone:
            raise forms.ValidationError('شماره همراه معتبر نیست . شماره همراه خود را بدون ۹۸+ وارد کنید')
        elif len(phone) != 11:
            raise forms.ValidationError('شماره همراه باید ۱۱ عدد باشد')
        else:
            try:
                int(phone)
                for digit in farsi_digits:
                    if digit in phone:
                        phone = persian_to_english(phone)
                        break
            except ValueError:
                raise forms.ValidationError('شماره همراه معتبر نمی باشد')
        return phone


