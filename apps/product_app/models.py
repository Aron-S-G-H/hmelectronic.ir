from django.db import models
from ckeditor.fields import RichTextField
from apps.account_app.models import CustomUser
from django.utils.html import mark_safe
from django.urls import reverse
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django_jalali.db.models import jDateTimeField, jDateField


class BaseCategory(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='عنوان دسته بندی',
        unique=True
    )
    slug = models.SlugField(
        allow_unicode=True,
        verbose_name='اسلاگ',
        help_text='این فیلد به صورت خودکار تکمیل می شود',
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی والد'
        verbose_name_plural = 'دسته بندی های والد'


class Category(models.Model):
    base_category = models.ForeignKey(
        BaseCategory,
        related_name='main_categories',
        verbose_name='عنوان وابسته',
        on_delete=models.CASCADE,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='والد',
        related_name='subs',
        null=True,
        blank=True,
        help_text='درصورتی که دسته بندی شما زیرمجموعه دسته بندی دیگری باشد. از این قسمت انتخاب کنید'
    )
    title = models.CharField(
        max_length=60,
        verbose_name='عنوان دسته بندی',
        help_text='۶۰ کاراکتر مجاز است',
        null=True
    )
    slug = models.SlugField(
        allow_unicode=True,
        blank=True,
        verbose_name='اسلاگ',
        help_text='این فیلد به صورت خودکار تکمیل می شود'
    )
    created_at = jDateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    category = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name='دسته بندی',
    )
    product_name = models.CharField(
        max_length=150,
        verbose_name='اسم محصول',
        help_text='۱۰۰کاراکتر مجاز است',
        db_index=True,
    )
    subtitle = models.CharField(
        max_length=150,
        verbose_name='اسم محصول به انگلیسی',
        db_index=True,
        null=True,
        blank=True,
        help_text='۱۵۰ کاراکتر مجاز است - optional'
    )
    description = RichTextField(verbose_name='توضیحات')
    property = RichTextField(
        verbose_name='ویژگی محصول',
        help_text='ویژگی هایی که محصول داره را در این قسمت بنویسید'
    )
    price = models.PositiveIntegerField(
        verbose_name='قیمت اصلی',
        help_text='قیمت را به تومان وارد کنید | برای محصولات ریزان الکتریک قیمت تیپ B را وارد کنید',
        db_index=True,
    )
    special_price = models.PositiveIntegerField(
        verbose_name='قیمت فروش ویژه',
        blank=True,
        null=True,
        help_text='قیمت را به تومان وارد کنید'
    )
    remaining_time = models.DateField(
        editable=True,
        null=True,
        blank=True,
        verbose_name='مدت زمان فروش ویژه',
    )
    selected_product = models.BooleanField(
        default=False,
        verbose_name='محصول برگزیده',
        help_text='در صورت فعال بودن گزینه،این محصول در بخش محصولات برگزیده نمایش داده می شود'
    )
    tag = models.ManyToManyField(
        'Tag',
        verbose_name='تگ ها',
        related_name='tag',
    )
    status = models.BooleanField(
        default=True,
        verbose_name='وضعیت محصول',
        help_text='درصورت موجود نبودن محصول غیرفعال کنید.',
    )
    slug = models.SlugField(
        max_length=150,
        allow_unicode=True,
        verbose_name='اسلاگ',
        help_text='این فیلد به صورت خودکار تکمیل می شود',
        db_index=True,
    )
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت محصول')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product:productDetail_page', kwargs={'pk': self.id, 'slug': self.slug})

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='محصول',
        related_name='images'
    )
    img = models.ImageField(
        upload_to='product',
        verbose_name='عکس محصول',
        help_text='حداقل سایز تصاویر 600x700 پیکسل باشد'
    )

    def __str__(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "80"/>')

    class Meta:
        verbose_name = 'عکس محصول'
        verbose_name_plural = 'عکس های محصول'


class Tag(models.Model):
    title = models.CharField(max_length=25, verbose_name='عنوان تگ', unique=True)
    slug = models.SlugField(
        allow_unicode=True,
        unique=True,
        blank=True,
        verbose_name='اسلاگ',
        help_text='این فیلد به صورت خودکار تکمیل می شود'
    )
    created_at = jDateField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'


class TipA(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='محصول',
        related_name='tipA'
    )
    price = models.PositiveIntegerField(
        verbose_name='قیمت تیپ A محصول',
        help_text='قیمت تیپ A محصول ریزان الکتریک را به تومان وارد کنید'
    )

    def __str__(self):
        return f'{self.price} تومان'

    class Meta:
        verbose_name = 'قیمت تیپ A محصول'
        verbose_name_plural = 'قیمت تیپ A محصولات'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    text = models.TextField(verbose_name='متن دیدگاه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return str(self.user)

    def has_response(self):
        if self.replies.exists():
            return mark_safe('<img src="/public/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/public/static/admin/img/icon-no.svg" alt="False">')
    has_response.short_description = 'Response'

    class Meta:
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظرات کاربران'
        ordering = ('-created_at',)


class CommentReply(models.Model):
    responder = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='comments_reply',
        null=True,
        blank=True,
    )
    responder_name_persistent = models.CharField(max_length=50, verbose_name='responder name')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name='کامنت')
    text = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f'{self.responder_name_persistent} - {self.text[:25]}'

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Comments Replies'
