from django.db import models
from apps.account_app.models import CustomUser
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from django.urls import reverse
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django_jalali.db.models import jDateTimeField
from apps.product_app.mixins import MetaDescriptionMixin, TimeStampMixin


class Blog(TimeStampMixin, MetaDescriptionMixin, models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='نویسنده', related_name='blogs')
    title = models.CharField(max_length=250, verbose_name='عنوان', unique=True, help_text='250 کاراکتر')
    description = RichTextField(verbose_name='متن')
    img = models.ImageField(upload_to='blog_image', verbose_name='تصویر', help_text='اندازه تصویر : 522 × 822', blank=True, null=True)
    status = models.BooleanField(default=True, help_text='درصورت غیرفعال بودن در سایت انتشار نمی یابد')
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, verbose_name='اسلاگ', help_text='این فیلد به صورت خودکار تکمیل می شود')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def img_preview(self):
        if self.img:
            return mark_safe(f'<a href="{self.img.url}"><img src="{self.img.url}" width="80"/></a>')
        else:
            return mark_safe('<span style="color: red">No Image</span>')
    img_preview.short_description = 'تصویر'

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-created_at',)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', verbose_name='جواب کامنت', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='blog_comments')
    text = models.TextField(verbose_name='متن کامنت')
    created_at = jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def text_show(self):
        return self.text[:20]
    text_show.short_description = 'متن پیام'

    def is_parent(self):
        if self.parent:
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')
    is_parent.short_description = 'Reply'

    def __str__(self):
        return f'{self.user} - {self.text[:50]}'

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ('-created_at',)
