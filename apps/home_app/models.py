from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import truncatewords
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from django.utils.html import mark_safe
from django.conf import settings


class SliderBannerImage(models.Model):
    img = models.ImageField(
        upload_to='home_slider',
        verbose_name='عکس بنر',
        help_text='حداقل ارتفاع تصویر 675px باشد'
    )
    url_address = models.URLField(verbose_name='آدرس URL', blank=True, null=True)
    sort_number = models.PositiveSmallIntegerField(verbose_name='اولویت نمایش', unique=True, null=True)
    status = models.BooleanField(
        verbose_name='وضعیت نمایش در سایت',
        default=True,
        help_text='در صورت غیرفعال کردن در وبسایت نمایش داده نمی شود'
    )
    upload_at = models.DateField(
        verbose_name='تاریخ آپلود',
        auto_now_add=True
    )

    def __str__(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "120"/>')

    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "120"/>')
    img_preview.short_description = 'عکس بنر'

    class Meta:
        verbose_name = 'بنر اسلایدر'
        verbose_name_plural = 'بنرهای اسلایدر'


class BannerSectionOne(models.Model):
    img = models.ImageField(
        upload_to='banners',
        verbose_name='عکس بنر',
        help_text='اندازه تصاویر 450x450 پیکسل باشد',
    )
    url_address = models.URLField(verbose_name='آدرس URL', blank=True, null=True)
    upload_at = models.DateTimeField(
        verbose_name='تاریخ آپلود',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        verbose_name='تاریخ آپدیت',
        auto_now=True
    )

    def __str__(self):
        return f'بنر {self.id} از بنرهای بخش اول '

    def img_preview(self):
        if self.img:
            return mark_safe(f'<a href="{self.img.url}"><img src = "{self.img.url}" width = "80"/></a>')
        else:
            return mark_safe(f'<span style="color:red">No Banner</span>')
    img_preview.short_description = 'بنر'

    class Meta:
        verbose_name = 'بنر بخش اول'
        verbose_name_plural = 'بنرهای بخش اول'
        ordering = ('-upload_at',)


class BannerSectionTwo(models.Model):
    img = models.ImageField(
        upload_to='banners',
        verbose_name='عکس بنر',
        help_text='حداقل عرض 2000px و حداقل ارتفاع 800px'
    )
    url_address = models.URLField(verbose_name='آدرس URL', blank=True, null=True)
    upload_at = models.DateField(
        verbose_name='تاریخ آپلود',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        verbose_name='تاریخ آپدیت',
        auto_now=True
    )

    def __str__(self):
        return f'بنر {self.id} از بنرهای بخش دوم '

    def img_preview(self):
        if self.img:
            return mark_safe(f'<a href="{self.img.url}"><img src = "{self.img.url}" width = "80"/></a>')
        else:
            return mark_safe(f'<span style="color:red">No Banner</span>')
    img_preview.short_description = 'عکس بنر'

    class Meta:
        verbose_name = 'بنر بخش دوم'
        verbose_name_plural = 'بنرهای بخش دوم'
        ordering = ('-upload_at',)


class SliderLogo(models.Model):
    img = models.ImageField(
        upload_to='logo_slider',
        verbose_name='تصویر لوگو',
        help_text='حداقل اندازه تصویر 1280x452px یاشد'
    )
    status = models.BooleanField(
        verbose_name='وضعیت نمایش در سایت',
        default=True,
        help_text='در صورت غیرفعال کردن در وبسایت نمایش داده نمی شود'
    )
    upload_at = models.DateField(
        verbose_name='تاریخ آپلود',
        auto_now_add=True
    )

    def __str__(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "100" style="background-color: white"/>')

    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "100" style="background-color: white"/>')
    img_preview.short_description = 'لوگو'

    class Meta:
        verbose_name = 'لوگو شرکت'
        verbose_name_plural = 'لوگو شرکت ها'


class CommunicationWays(models.Model):
    address = models.CharField(
        max_length=150,
        verbose_name='آدرس',
        null=True,
        blank=True,
        help_text='۱۵۰ کاراکتر مجاز است - optional'
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        null=True,
        blank=True,
        help_text='optional',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    update_at = models.DateTimeField(
        verbose_name='تاریخ به روزرسانی',
        auto_now=True
    )

    def __str__(self):
        return f'اطلاعات و راه های ارتباطی'

    def short_address(self):
        return truncatewords(self.address, 20)
    short_address.short_description = 'آدرس'

    class Meta:
        verbose_name = 'راه ارتباطی'
        verbose_name_plural = 'راه های ارتباطی'


def phone_number_validator(number):
    try:
        int(number)
    except:
        raise ValidationError('شماره تلفن معتبر نمی باشد')
    if len(number) < 11 or len(number) > 11:
        raise ValidationError('شماره همراه باید ۱۱ عدد باشد')


class PhoneNumber(models.Model):
    communication_ways = models.ForeignKey(
        CommunicationWays,
        on_delete=models.CASCADE,
        verbose_name='راه ارتباطی',
        related_name='phone_n',
        null=True
    )
    title = models.CharField(
        max_length=30,
        verbose_name='عنوان بخش',
        help_text='مثال: بخش فنی و تعمیرات'
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name='شماره همراه',
        help_text='مثال:۰۹۱۲۲۳۴۵۶۸۹',
        validators=[phone_number_validator]
    )

    def __str__(self):
        return f'{self.title} - {self.phone_number}'

    class Meta:
        verbose_name = 'شماره همراه'
        verbose_name_plural = 'شمارهای همراه'


def company_number_validator(value):
    number = str(value)
    if len(number) > 8:
        raise ValidationError('شماره شرکت باید حداکثر ۸ عدد باشد')


class CompanyNumber(models.Model):
    communication_ways = models.ForeignKey(
        CommunicationWays,
        on_delete=models.CASCADE,
        verbose_name='راه ارتباطی',
        related_name='company_n',
        null=True
    )
    province_code = models.CharField(
        max_length=3,
        verbose_name='کد استان',
        help_text='مثال: ۰۲۱'
    )
    number = models.PositiveIntegerField(
        verbose_name='شماره ثابت',
        help_text='مثال: ۶۶۶۷۸۹۰۸',
        null=True,
        blank=True,
        validators=[company_number_validator]
    )

    def __str__(self):
        return f'{self.number}-{self.province_code}'

    class Meta:
        verbose_name = 'شماره ثابت'
        verbose_name_plural = 'شماره های ثابت'


SOCIALMEDIAS = [
    ('instagram', 'اینستاگرام'),
    ('facebook', 'فیسبوک'),
    ('linkedin', 'لینکدین'),
    ('twitter', 'توییتر'),
    ('telegram', 'تلگرام'),
]


class SocialMedia(models.Model):
    communication_ways = models.ForeignKey(
        CommunicationWays,
        on_delete=models.CASCADE,
        verbose_name='راه ارتباطی',
        related_name='medias',
        null=True
    )
    title = models.CharField(
        max_length=50,
        verbose_name='عنوان',
        choices=SOCIALMEDIAS
    )
    icon = models.ImageField(
        upload_to='social-icon',
        null=True,
        verbose_name='ایکون',
        help_text='ایکون مدنظر را در فرمت svg با png و بدون پس زمینه در حداقل سابز 50x50 آپلود کنید '
    )
    link = models.URLField(verbose_name='لینک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return mark_safe(f'<span>{self.title}<img src = "{self.icon.url}" width = "30" style="margin-right:5px"/><span>')

    class Meta:
        verbose_name = 'شبکه مجازی'
        verbose_name_plural = 'شبکه های مجازی'


# Frequently Asked Questions
class FQuestions(models.Model):
    question = models.CharField(max_length=150, verbose_name='عنوان سوال', help_text='۱۵۰ کاراکتر مجاز است', unique=True)
    answer = RichTextField(verbose_name='پاسخ')
    status = models.BooleanField(verbose_name='وضعیت انتشار در وبسایت', default=True)
    update_at = models.DateTimeField(verbose_name='تاریخ به آپدیت', auto_now=True)
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'


class Logo(models.Model):
    img = models.ImageField(verbose_name='تصویر لوگو', upload_to='logo', null=True, blank=True)
    status = models.BooleanField(verbose_name='وضعیت نمایش در سایت', default=True,
                                 help_text='در صورت غیرفعال کردن در وبسایت نمایش داده نمی شود')
    upload_at = models.DateTimeField(verbose_name='تاریخ آپلود', auto_now_add=True)

    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "60"/>')
    img_preview.short_description = 'لوگو'

    def __str__(self):
        return f' لوگو {self.id} '

    class Meta:
        verbose_name = 'لوگو'
        verbose_name_plural = 'لوگو'


class AboutUs(models.Model):
    title = models.CharField(max_length=60, verbose_name='عنوان', null=True, blank=True)
    description = RichTextField(verbose_name='توضیحات', null=True)
    update_at = models.DateTimeField(verbose_name='تاریخ به روزرسانی', auto_now=True)
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'


class AboutUsFeature(models.Model):
    about_us = models.ForeignKey(
        AboutUs,
        on_delete=models.CASCADE,
        verbose_name='درباره ما',
        related_name='features',
        null=True
    )
    title = models.CharField(
        max_length=25,
        verbose_name='عنوان',
        help_text='۲۵ کاراکتر',
        unique=True
    )
    description = models.CharField(
        max_length=30,
        verbose_name='توضیح',
        help_text='۳۰ کاراکتر'
    )
    icon = models.ImageField(
        upload_to='aboutUs_icon',
        verbose_name='ایکون',
        help_text='ایکون مدنظر را در فرمت svg یا png و بدون پس زمینه در حداقل سابز 50x50 آپلود کنید '
    )
    update_at = models.DateTimeField(verbose_name='تاریخ آپدیت', auto_now=True)
    created_at = models.DateField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    def __str__(self):
        return mark_safe(f'<span style="margin-right:5px">{self.title}<img src = "{self.icon.url}" width = "30" style="margin-right:10px"/><span>')

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'


class ShippingMethod(models.Model):
    title = models.CharField(max_length=40, verbose_name='عنوان', help_text='۴۰ کاراکتر مجاز است', unique=True)
    text = models.TextField(verbose_name='متن')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'روش ارسال'
        verbose_name_plural = 'روش های ارسال'


class FixedBoxText(models.Model):
    text = models.TextField(verbose_name='متن', help_text='از نوشتن متن طولانی خودداری کنید')
    url = models.URLField(help_text='optional - بک لینک متن', null=True, blank=True)
    background_color = ColorField(default='#0e1953', format='hex')
    text_color = ColorField(default='#f8f9fa', format='hex')
    border_color = ColorField(default='#d90000', format='hex')
    status = models.BooleanField(default=True, verbose_name='وضعیت نمایش', help_text='درصورت غیرفعال کردن در سایت نمایش داده نمیشود')
    created_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد')

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
        self.absolute_url = f'https://{domain_name}/{self.file.url}'
        self.size = self.file.size / 1000
        super(UploadFile, self).save()

