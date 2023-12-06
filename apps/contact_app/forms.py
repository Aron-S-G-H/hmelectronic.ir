from django import forms
from .models import ContactUs, SendEmail
from django.contrib.auth import get_user_model


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ('user', 'created_at')
        widgets = {
            'subject': forms.TextInput(attrs={
                'name': 'subject',
                'id': 'subject',
                'placeholder': 'موضوع:',
                'maxlength': '100',
            }),
            'message': forms.Textarea(attrs={
                'name': 'message',
                'id': 'message',
                'placeholder': 'متن پیام...',
                'rows': '8',
            }),
        }


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.pdf']
    if not ext.lower() in valid_extensions:
        return False
    return True


class SendEmailAdminForm(forms.ModelForm):
    class Meta:
        model = SendEmail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SendEmailAdminForm, self).__init__(*args, **kwargs)
        user_model = get_user_model()
        self.fields['user'].queryset = user_model.objects.filter(is_staff=False, email__isnull=False)

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user', None)
        if not user:
            self.add_error('user', 'برای ارسال ایمیل کاربر را مشخص کنید')
        subject = cleaned_data.get('subject', None)
        if not subject:
            self.add_error('subject', 'برای ارسال ایمیل موضوع (Subject) را بنوسید')
        message = cleaned_data.get('message', None)
        file = cleaned_data.get('file', None)
        if not message and not file:
            self.add_error('message', 'برای ارسال ایمیل یک پیام (Message) یا یک فایل انتخاب کنید ')
        if file:
            check_file = validate_file_extension(file)
            if not check_file:
                self.add_error('file', 'فایل های pdf و png و jpg مجاز هستند')
