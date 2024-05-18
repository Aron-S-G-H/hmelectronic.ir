from django.contrib import admin
from . import models as app_model
from django import forms
from django.db import models
from .forms import UploadFileAdminForm, CommunicationWaysForm
from jalali_date import datetime2jalali


@admin.register(app_model.SliderBannerImage)
class SliderBannerImageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at_jalali', 'update_at_jalali')
    list_display = ('img_preview', 'url_address', 'sort_number', 'status', 'created_at_jalali')
    list_editable = ('url_address', 'sort_number')
    formfield_overrides = {
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.BannerSectionOne)
class BannerSectionOneAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at_jalali', 'update_at_jalali')
    list_display = ('id', 'img_preview', 'url_address', 'created_at_jalali', 'update_at_jalali')
    list_editable = ('url_address',)
    formfield_overrides = {
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.SliderLogo)
class SliderLogoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at_jalali', 'update_at_jalali')
    list_display = ('brand_name', 'img_preview', 'url_address', 'created_at_jalali', 'update_at_jalali')
    list_editable = ('url_address',)
    formfield_overrides = {
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


class CompanyNumberAdmin(admin.StackedInline):
    model = app_model.CompanyNumber
    extra = 0
    max_num = 2
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '5'})},
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '12'})},
    }


@admin.register(app_model.CommunicationWays)
class CommunicationWaysAdmin(admin.ModelAdmin):
    inlines = (CompanyNumberAdmin,)
    form = CommunicationWaysForm
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '100'})},
        models.EmailField: {'widget': forms.EmailInput(attrs={'size': '30'})},
    }
    list_display = ('short_address', 'email', 'phone_number', 'telegram_id', 'update_at_jalali')
    readonly_fields = ('created_at_jalali', 'update_at_jalali')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('img_preview', 'status')


@admin.register(app_model.AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at_jalali', 'update_at_jalali')
    list_display = ('title', 'created_at_jalali', 'update_at_jalali')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '90'})}
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.FixedBoxText)
class FixedBoxTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'status', 'created_at_jalali', 'update_at_jalali')
    list_editable = ('status',)
    readonly_fields = ('created_at_jalali', 'update_at_jalali')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '80'})},
        models.URLField: {'widget': forms.URLInput(attrs={'size': '120'})}
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_at_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    form = UploadFileAdminForm
    list_display = ('__str__', 'size', 'absolute_url')
    readonly_fields = ('size', 'absolute_url')
