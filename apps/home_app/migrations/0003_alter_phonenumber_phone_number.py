# Generated by Django 4.2.5 on 2023-09-17 13:58

import apps.home_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0002_remove_sliderbannerimage_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='phone_number',
            field=models.CharField(help_text='مثال:۰۹۱۲۲۳۴۵۶۸۹', max_length=11, validators=[apps.home_app.models.phone_number_validator], verbose_name='شماره همراه'),
        ),
    ]