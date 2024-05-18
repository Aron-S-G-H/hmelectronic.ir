from django.contrib import admin
from .models import ContactUs, SendEmail
from jalali_date import datetime2jalali
from django.db import models
from django import forms
from .forms import SendEmailAdminForm


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'message', 'created_at_jalali')
    list_display = ('user', 'message', 'created_at_jalali')
    ordering = ('-created_at',)

    @admin.display(description='تاریخ دریافت پیام', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(SendEmail)
class SendEmailAdmin(admin.ModelAdmin):
    form = SendEmailAdminForm
    readonly_fields = ('send_at_jalali', 'submit_status')
    list_display = ('user', 'subject', 'send_at_jalali', 'submit_status')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '100'})},
    }
    ordering = ('-send_at',)

    @admin.display(description='زمان ارسال', ordering='send_at')
    def send_at_jalali(self, obj):
        return datetime2jalali(obj.send_at).strftime('%Y/%m/%d - %H:%M')
