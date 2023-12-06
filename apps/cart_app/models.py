from django.db import models
from apps.account_app.models import CustomUser
from apps.product_app.models import Product


class UserOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    first_name = models.CharField(max_length=40, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)
    phone = models.CharField(verbose_name='شماره همراه', max_length=11)
    state = models.CharField(verbose_name='استان', max_length=40)
    city = models.CharField(verbose_name='شهر', max_length=40)
    postal_code = models.CharField(max_length=12, verbose_name='کد پستی')
    national_code = models.CharField(verbose_name='کد ملی', max_length=20)
    address = models.TextField(verbose_name='آدرس')
    note = models.TextField(verbose_name='یادداشت کاربر', null=True, blank=True)
    total_price = models.PositiveIntegerField(verbose_name='هزینه کل')
    is_paid = models.BooleanField(verbose_name='وضعیت پرداخت', default=False)
    created_at = models.DateTimeField(verbose_name='تاریخ ثبت سفارش', auto_now_add=True)
    reference_id = models.CharField(max_length=15, verbose_name='کد پیگیری سفارش', null=True, blank=True)
    is_sms_sent = models.BooleanField(verbose_name='اس ام اس ارسال شده', null=True, blank=True, default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class ProductOrder(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name='محصول')
    product_uniqueID = models.CharField(verbose_name='product unique id', max_length=110)
    product_price = models.PositiveIntegerField(verbose_name='قیمت محصول', default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name='تعداد')
    item_total = models.PositiveIntegerField(verbose_name='مجموع قیمت')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'سفارش محصول'
        verbose_name_plural = 'سفارش محصولات'
