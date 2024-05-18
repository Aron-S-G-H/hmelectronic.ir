from django.db import models


class MetaDescriptionMixin(models.Model):
    meta_description = models.CharField(max_length=150, null=True, help_text='150 کاراکتر')

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ آپدیت')

    class Meta:
        abstract = True
