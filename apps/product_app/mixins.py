from django.db import models


class MetaDescriptionMixin(models.Model):
    meta_description = models.CharField(max_length=120, null=True, help_text='۱۲۰ کاراکتر')

    class Meta:
        abstract = True
