# Generated by Django 4.2.5 on 2023-10-23 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_alter_blog_update_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
    ]