from django import forms
from .models import UploadFile, CommunicationWays
from apps.contact_app.forms import validate_file_extension


class UploadFileAdminForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file', None)
        if file:
            check_file = validate_file_extension(file)
            if not check_file:
                self.add_error('file', 'فایل های pdf و png و jpg مجاز هستند')


class CommunicationWaysForm(forms.ModelForm):
    class Meta:
        model = CommunicationWays
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number', None)
        if phone_number:
            len_phone_number = len(phone_number)
            if len_phone_number != 11:
                self.add_error('phone_number', f'شماره همراه باید 11 عدد باشد. برای شما {len_phone_number} است')
            elif '+' in phone_number:
                raise self.add_error('phone_number', 'شماره همراه خود را بدون ۹۸+ وارد کنید')
            else:
                try:
                    int(phone_number)
                except ValueError:
                    self.add_error('phone_number', 'شماره همراه معتبر نمیباشد')
