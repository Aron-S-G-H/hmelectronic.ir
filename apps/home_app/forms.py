from django import forms
from .models import UploadFile
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
