from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="آدرس ایمیل", unique=True, null=True, blank=True)
    phone = models.PositiveBigIntegerField(verbose_name='شماره موبایل', unique=True)
    one_time_password = models.SmallIntegerField(verbose_name='رمز یک بار مصرف', null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# OTP = ONE TIME PASSWORD
class Otp(models.Model):
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=60)
    code = models.SmallIntegerField()
    token = models.CharField(max_length=125)

    class Meta:
        verbose_name = 'رمز یک بار مصرف'
        verbose_name_plural = 'رمزهای یک بار مصرف'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
