from django import forms
from .models import Product, Category


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(parent=None)

    def clean(self):
        cleaned_data = super().clean()
        special_price = cleaned_data.get('special_price')
        remaining_time = cleaned_data.get('remaining_time')
        category = cleaned_data.get('category')
        contains_reizan = category.filter(title='ریزان الکترونیک').exists()
        if remaining_time and not special_price:
            self.add_error('special_price', 'برای مدت زمان فروش ویژه قیمت فروش ويژه را تعیین نمایید')
        elif special_price and not remaining_time:
            self.add_error('remaining_time', 'برای فروش ویژه مدت زمان فروش ویژه را مشخص کنید')
        elif special_price and contains_reizan:
            self.add_error('special_price', 'برای محصولات دسته بندی ریزان الکترونیک نمیتوانید فروش ویژه تعیین کنید')
