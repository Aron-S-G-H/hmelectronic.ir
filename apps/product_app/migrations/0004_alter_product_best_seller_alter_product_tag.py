# Generated by Django 4.2.5 on 2023-10-10 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_alter_product_price_alter_product_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='best_seller',
            field=models.BooleanField(default=False, help_text='در صورت فعال بودن گزینه،این محصول در بخش محصولات برگزیده نمایش داده می شود', verbose_name='محصول برگزیده'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(null=True, related_name='tag', to='product_app.tag', verbose_name='تگ ها'),
        ),
    ]