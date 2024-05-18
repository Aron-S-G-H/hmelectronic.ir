from django import forms
from .models import UserOrder


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = UserOrder
        exclude = ('user', 'total_price', 'is_paid', 'created_at')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'نام خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'name',
                'id': 'first_name',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'نام خانوادگی',
                'class': 'form-control rounded-3',
                'name': 'lastname',
                'id': 'last_name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'آدرس ایمیل خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'email',
                'id': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'شماره تلفن همراه خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'phone',
                'id': 'phone',
            }),
            'state': forms.TextInput(attrs={
                'placeholder': 'نام استان خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'state',
                'id': 'state',
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'نام شهر خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'city',
                'id': 'city',
            }),
            'postal_code': forms.TextInput(attrs={
                'placeholder': 'کد پستی خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'postal_code',
                'id': 'postal_code',
            }),
            'national_code': forms.TextInput(attrs={
                'placeholder': 'کد ملی خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'national_code',
                'id': 'national_code',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'آدرس خود را وارد کنید',
                'class': 'form-control rounded-3',
                'name': 'address',
                'id': 'address',
            }),
            'note': forms.Textarea(attrs={
                'placeholder': 'نکاتی درباره سفارش را که لازم است یادداشت کنید',
                'class': 'form-control rounded-3',
                'name': 'message',
                'id': 'note',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
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

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        try:
            int(national_code)
        except ValueError:
            raise forms.ValidationError('کد ملی معتبر نمی باشد')
        return national_code

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        try:
            int(postal_code)
        except ValueError:
            raise forms.ValidationError('کد پستی معتبر نمی باشد')
        return postal_code

