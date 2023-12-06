from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Otp
from django.db import models
from django import forms
from apps.cart_app.models import UserOrder
from jalali_date import datetime2jalali


class UserOrderAdmin(admin.StackedInline):
    model = UserOrder
    extra = 0
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '20'})},
    }


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = (UserOrderAdmin,)
    list_display = ("first_name", 'last_name', 'phone', 'email', 'last_login_jalali', 'date_joined_jalali', "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser", "date_joined", "last_login")
    readonly_fields = ('last_login_jalali', 'date_joined_jalali')
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '15'})},
    }

    fieldsets = (
        (None, {"fields": ("password",)}),
        ('اطلاعات شخصی', {"fields": ('first_name', 'last_name', 'phone', 'email', 'last_login_jalali', 'date_joined_jalali')}),
        ("مجوزها", {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "phone", "password1", "password2", "is_superuser", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email", "phone", "first_name", "last_name")
    ordering = ("-date_joined",)

    @admin.display(description='آخرین ورود', ordering='last_login')
    def last_login_jalali(self, obj):
        if obj.last_login:
            return datetime2jalali(obj.last_login).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ پیوستن', ordering='date_joined')
    def date_joined_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%Y/%m/%d - %H:%M')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Otp)
