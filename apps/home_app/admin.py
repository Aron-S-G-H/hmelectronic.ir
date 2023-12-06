from django.contrib import admin
from . import models as app_model
from django import forms
from django.db import models
from .forms import UploadFileAdminForm
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import StackedInlineJalaliMixin


class CompanyNumberAdmin(admin.StackedInline):
    model = app_model.CompanyNumber
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '5'})},
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '12'})},
    }


class PhoneNumberAdmin(admin.StackedInline):
    model = app_model.PhoneNumber
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '20'})},
    }


class SocialMediaAdmin(StackedInlineJalaliMixin, admin.StackedInline):
    model = app_model.SocialMedia
    extra = 0
    readonly_fields = ('get_created_jalali',)

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.CommunicationWays)
class CommunicationWaysAdmin(admin.ModelAdmin):
    inlines = (PhoneNumberAdmin, CompanyNumberAdmin, SocialMediaAdmin)
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '100'})},
        models.EmailField: {'widget': forms.EmailInput(attrs={'size': '30'})},
    }
    list_display = ('id', 'email', 'short_address', 'get_created_jalali')
    readonly_fields = ('get_created_jalali', 'get_update_jalali')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ به روزرسانی', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.SliderBannerImage)
class SliderBannerImageAdmin(admin.ModelAdmin):
    readonly_fields = ('get_upload_jalali',)
    list_display = ('img_preview', 'url_address', 'sort_number', 'status', 'get_upload_jalali')
    list_editable = ('url_address', 'sort_number')
    formfield_overrides = {
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }

    @admin.display(description='تاریخ آپلود', ordering='upload_at')
    def get_upload_jalali(self, obj):
        return date2jalali(obj.upload_at).strftime('%Y/%m/%d')


@admin.register(app_model.BannerSectionTwo)
class BannerSectionTwoAdmin(admin.ModelAdmin):
    model = app_model.BannerSectionTwo
    readonly_fields = ('get_upload_jalali', 'get_update_jalali')
    list_display = ('id', 'img_preview', 'url_address', 'get_upload_jalali', 'get_update_jalali')
    list_editable = ('url_address',)
    formfield_overrides = {
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپلود', ordering='upload_at')
    def get_upload_jalali(self, obj):
        return date2jalali(obj.upload_at).strftime('%Y/%m/%d')


@admin.register(app_model.BannerSectionOne)
class BannerSectionOneAdmin(admin.ModelAdmin):
    readonly_fields = ('get_upload_jalali', 'get_update_jalali')
    list_display = ('id', 'img_preview', 'url_address', 'get_upload_jalali', 'get_update_jalali')
    list_editable = ('url_address',)
    formfield_overrides = {
        models.URLField: {'widget': forms.TextInput(attrs={'size': '80'})},
    }

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپلود', ordering='upload_at')
    def get_upload_jalali(self, obj):
        return datetime2jalali(obj.upload_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.SliderLogo)
class SliderLogoAdmin(admin.ModelAdmin):
    readonly_fields = ('get_upload_jalali',)
    list_display = ('id', 'img_preview', 'status', 'get_upload_jalali')
    list_filter = ('status', 'upload_at')

    @admin.display(description='تاریخ آپلود', ordering='upload_at')
    def get_upload_jalali(self, obj):
        return date2jalali(obj.upload_at).strftime('%Y/%m/%d')


@admin.register(app_model.FQuestions)
class FQAdmin(admin.ModelAdmin):
    readonly_fields = ('get_created_jalali', 'get_update_jalali')
    list_display = ('question', 'status', 'get_update_jalali', 'get_created_jalali')
    list_filter = ('created_at', 'update_at', 'status')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '90'})}
    }

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.Logo)
class LogoAdmin(admin.ModelAdmin):
    readonly_fields = ('get_upload_jalali',)
    list_display = ('img_preview', 'status', 'get_upload_jalali')
    list_filter = ('status',)

    @admin.display(description='تاریخ آپلود', ordering='upload_at')
    def get_upload_jalali(self, obj):
        return datetime2jalali(obj.upload_at).strftime('%Y/%m/%d - %H:%M')


class AboutUsFeatureAdmin(admin.StackedInline):
    model = app_model.AboutUsFeature
    extra = 0
    max_num = 4
    readonly_fields = ('get_update_jalali', 'get_created_jalali')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '50'})}
    }

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')


@admin.register(app_model.AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = (AboutUsFeatureAdmin,)
    readonly_fields = ('get_update_jalali', 'get_created_jalali')
    list_display = ('title', 'get_created_jalali', 'get_update_jalali')
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '90'})}
    }

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_update_jalali')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def get_update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.FixedBoxText)
class FixedBoxTextAdmin(admin.ModelAdmin):
    list_display = ('text', 'status', 'get_created_jalali')
    list_editable = ('status',)
    readonly_fields = ('get_created_jalali',)
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput(attrs={'size': '100'})}
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(app_model.UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    form = UploadFileAdminForm
    list_display = ('__str__', 'size', 'absolute_url')
    readonly_fields = ('size', 'absolute_url')
