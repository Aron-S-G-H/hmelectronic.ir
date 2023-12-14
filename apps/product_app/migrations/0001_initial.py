# Generated by Django 4.2.5 on 2023-12-14 09:59

import apps.product_app.mixins
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(allow_unicode=True, help_text='این فیلد به صورت خودکار تکمیل می شود', null=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'دسته بندی والد',
                'verbose_name_plural': 'دسته بندی های والد',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='۶۰ کاراکتر مجاز است', max_length=60, null=True, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, help_text='این فیلد به صورت خودکار تکمیل می شود', verbose_name='اسلاگ')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('base_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_categories', to='product_app.basecategory', verbose_name='عنوان وابسته')),
                ('parent', models.ForeignKey(blank=True, help_text='درصورتی که دسته بندی شما زیرمجموعه دسته بندی دیگری باشد. از این قسمت انتخاب کنید', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='product_app.category', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن دیدگاه')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'نظر کاربر',
                'verbose_name_plural': 'نظرات کاربران',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(db_index=True, help_text='۱۰۰کاراکتر مجاز است', max_length=150, verbose_name='اسم محصول')),
                ('subtitle', models.CharField(blank=True, db_index=True, help_text='۱۵۰ کاراکتر مجاز است - optional', max_length=150, null=True, verbose_name='اسم محصول به انگلیسی')),
                ('description', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('property', ckeditor.fields.RichTextField(help_text='ویژگی هایی که محصول داره را در این قسمت بنویسید', verbose_name='ویژگی محصول')),
                ('price', models.PositiveIntegerField(db_index=True, help_text='قیمت را به تومان وارد کنید | برای محصولات ریزان الکتریک قیمت تیپ B را وارد کنید', verbose_name='قیمت اصلی')),
                ('special_price', models.PositiveIntegerField(blank=True, help_text='قیمت را به تومان وارد کنید', null=True, verbose_name='قیمت فروش ویژه')),
                ('remaining_time', models.DateField(blank=True, null=True, verbose_name='مدت زمان فروش ویژه')),
                ('selected_product', models.BooleanField(default=False, help_text='در صورت فعال بودن گزینه،این محصول در بخش محصولات برگزیده نمایش داده می شود', verbose_name='محصول برگزیده')),
                ('status', models.BooleanField(default=True, help_text='درصورت موجود نبودن محصول غیرفعال کنید.', verbose_name='وضعیت محصول')),
                ('slug', models.SlugField(allow_unicode=True, help_text='این فیلد به صورت خودکار تکمیل می شود', max_length=150, verbose_name='اسلاگ')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت محصول')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('category', models.ManyToManyField(related_name='products', to='product_app.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ('-created_at',),
            },
            bases=(apps.product_app.mixins.MetaDescriptionMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, unique=True, verbose_name='عنوان تگ')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, help_text='این فیلد به صورت خودکار تکمیل می شود', unique=True, verbose_name='اسلاگ')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
            },
        ),
        migrations.CreateModel(
            name='TipA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(help_text='قیمت تیپ A محصول ریزان الکتریک را به تومان وارد کنید', verbose_name='قیمت تیپ A محصول')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipA', to='product_app.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'قیمت تیپ A محصول',
                'verbose_name_plural': 'قیمت تیپ A محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(help_text='حداقل سایز تصاویر 600x700 پیکسل باشد', upload_to='product', verbose_name='عکس محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product_app.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'عکس محصول',
                'verbose_name_plural': 'عکس های محصول',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(related_name='tag', to='product_app.tag', verbose_name='تگ ها'),
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responder_name_persistent', models.CharField(max_length=50, verbose_name='responder name')),
                ('text', models.TextField(verbose_name='متن')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='product_app.comment', verbose_name='کامنت')),
                ('responder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments_reply', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reply',
                'verbose_name_plural': 'Comments Replies',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product_app.product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
