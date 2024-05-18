from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import truncatewords
from colorfield.fields import ColorField
from django.utils.html import mark_safe
from django.conf import settings
from apps.product_app.mixins import TimeStampMixin


class SliderBannerImage(TimeStampMixin, models.Model):
    img = models.ImageField(upload_to='home_slider', verbose_name='عکس بنر', help_text='اندازه تصویر : 378 × 1079')
    url_address = models.URLField(verbose_name='Url Address', blank=True, null=True)
    sort_number = models.PositiveSmallIntegerField(verbose_name='اولویت نمایش', unique=True, default=1)
    status = models.BooleanField(default=True, help_text='در صورت غیرفعال کردن در وبسایت نمایش داده نمی شود')

    def __str__(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "120"/>')

    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "120"/>')
    img_preview.short_description = 'Banner View'

    class Meta:
        verbose_name = 'Slider Banner'
        verbose_name_plural = 'Slider Banners'


class BannerSectionOne(TimeStampMixin, models.Model):
    img = models.ImageField(upload_to='banners', verbose_name='عکس بنر', help_text='اندازه تصویر : 262 × 350')
    url_address = models.URLField(verbose_name='Url Address', blank=True, null=True)

    def __str__(self):
        return self.img.url

    def img_preview(self):
        return mark_safe(f'<a href="{self.img.url}"><img src="{self.img.url}" width="80"/></a>')
    img_preview.short_description = 'Banner View'

    class Meta:
        verbose_name = 'Small Banner'
        verbose_name_plural = 'Small Banners'
        ordering = ('-created_at',)


class SliderLogo(TimeStampMixin, models.Model):
    brand_name = models.CharField(verbose_name='اسم برند', max_length=25, null=True, help_text='۲۵ کاراکتر')
    img = models.ImageField(upload_to='logo_slider', verbose_name='تصویر لوگو', help_text='اندازه تصویر : 284 × 600')
    url_address = models.URLField(verbose_name='Url Address', blank=True, null=True)

    def __str__(self):
        return self.brand_name if self.brand_name else self.img.url

    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "100" style="background-color: white"/>')
    img_preview.short_description = 'لوگو'

    class Meta:
        verbose_name = 'لوگو شرکت'
        verbose_name_plural = 'لوگو شرکت ها'


class CommunicationWays(TimeStampMixin, models.Model):
    address = models.CharField(max_length=150, verbose_name='آدرس', null=True, blank=True, help_text='150 کاراکتر')
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='شماره همراه', null=True, blank=True)
    telegram_id = models.CharField(verbose_name='Telegram ID', max_length=30, null=True, blank=True, help_text='30 کاراکتر')

    def __str__(self):
        return truncatewords(self.address, 10)

    def short_address(self):
        return truncatewords(self.address, 20)
    short_address.short_description = 'آدرس'

    class Meta:
        verbose_name = 'راه ارتباطی'
        verbose_name_plural = 'راه های ارتباطی'


class CompanyNumber(models.Model):
    communication_ways = models.ForeignKey(CommunicationWays, on_delete=models.CASCADE, related_name='company_n', null=True)
    province_code = models.CharField(max_length=3, verbose_name='کد استان', help_text='مثال: 021')
    number = models.PositiveIntegerField(verbose_name='شماره ثابت', null=True, blank=True)

    def __str__(self):
        return f'{self.number}-{self.province_code}'

    class Meta:
        verbose_name = 'شماره ثابت'
        verbose_name_plural = 'شماره های ثابت'


class Logo(models.Model):
    img = models.ImageField(verbose_name='لوگو', upload_to='logo', null=True, blank=True)
    status = models.BooleanField(default=True, help_text='در صورت غیرفعال کردن در وبسایت نمایش داده نمی شود')

    def __str__(self):
        return self.img.url

    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "60"/>')
    img_preview.short_description = 'لوگو'

    class Meta:
        verbose_name = 'لوگو'
        verbose_name_plural = 'لوگو'


class AboutUs(TimeStampMixin, models.Model):
    title = models.CharField(max_length=60, verbose_name='عنوان', null=True, blank=True)
    description = RichTextField(verbose_name='توضیحات', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'


class FixedBoxText(TimeStampMixin, models.Model):
    title = models.CharField(max_length=25, verbose_name='عنوان', help_text='۲۵ کاراکتر', null=True, blank=True)
    text = models.TextField(verbose_name='متن', help_text='از نوشتن متن طولانی خودداری کنید')
    url = models.URLField(help_text='optional - بک لینک متن', null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name='وضعیت نمایش', help_text='درصورت غیرفعال کردن در سایت نمایش داده نمیشود')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'متن ثابت'
        verbose_name_plural = 'متن های ثابت'


class UploadFile(models.Model):
    file = models.FileField(upload_to='uploaded_file', help_text='فایل های pdf و png و jpg مجاز هستند')
    size = models.FloatField(default=0, help_text='برحسب کیلوبایت (KB) است')
    absolute_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.file.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        domain_name = settings.ALLOWED_HOSTS[0]
        self.absolute_url = f'https://{domain_name}public/media/{self.file.name}'
        self.size = self.file.size / 1000
        super(UploadFile, self).save()
