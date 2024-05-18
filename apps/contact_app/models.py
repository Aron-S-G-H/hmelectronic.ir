from django.db import models
from apps.account_app.models import CustomUser
from .tasks import send_email_users
import logging


class ContactUs(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='messages', null=True)
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(verbose_name='تاریخ دریافت پیام', auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'


class SendEmail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='emails', null=True)
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام', blank=True, null=True)
    file = models.FileField(
        verbose_name='فایل',
        blank=True,
        null=True,
        upload_to='messages_file',
        help_text='فایل های pdf و png و jpg مجاز هستند'
    )
    send_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    submit_status = models.BooleanField(verbose_name='وضعیت ارسال پیام', default=False)

    def __str__(self):
        return f'{self.user} - {self.subject}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user_email = self.user.email
        try:
            read_file = self.file.read() if self.file else None
            file_url = self.file.url if self.file else None
            send_email_users.apply_async(
                (self.subject, self.message, file_url, read_file, user_email),
                retry=False,
                ignore_result=True,
                expires=10,
            )
            self.submit_status = True
            super(SendEmail, self).save()
        except Exception as e:
            logging.warning(e)
            self.submit_status = False
            super(SendEmail, self).save()

    class Meta:
        verbose_name = 'ارسال ایمیل به کاربر'
        verbose_name_plural = 'ارسال ایمیل به کاربران'
