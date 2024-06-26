# Generated by Django 4.2.5 on 2024-01-15 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0002_remove_aboutusfeature_about_us_and_more'),
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecategory',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='base_category', verbose_name='تصویر پس زمینه'),
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, help_text='130 × 130 px', null=True, upload_to='category', verbose_name='آیکون'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_brands', to='home_app.sliderlogo', verbose_name='اسم برند'),
        ),
        migrations.AddField(
            model_name='product',
            name='technical_specs',
            field=models.JSONField(blank=True, null=True, verbose_name='مشخصات فنی'),
        ),
        migrations.AlterField(
            model_name='basecategory',
            name='title',
            field=models.CharField(help_text='۳۰ کاراکتر', max_length=30, unique=True, verbose_name='عنوان دسته بندی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(db_index=True, help_text='۱۵۰ کاراکتر', max_length=150, verbose_name='اسم محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subtitle',
            field=models.CharField(blank=True, db_index=True, help_text='۱۵۰ کاراکتر', max_length=150, null=True, verbose_name='اسم محصول به انگلیسی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ آپدیت'),
        ),
    ]
