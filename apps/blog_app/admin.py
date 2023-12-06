from django.contrib import admin
from apps.blog_app import models
from django.db import models as djmodels
from django import forms
from jalali_date import datetime2jalali


class CommentAdmin(admin.StackedInline):
    readonly_fields = ('date_time_format',)
    model = models.Comment
    extra = 0

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def date_time_format(self, obj):
        return obj.created_at.strftime("%Y/%m/%d - %H:%M")


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = (CommentAdmin,)
    readonly_fields = ('update_time_format', 'date_time_format')
    list_filter = ('status',)
    list_display = ('title', 'author', 'status', 'img_preview', 'date_time_format')
    list_editable = ('status',)
    search_fields = ('author', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        djmodels.CharField: {'widget': forms.TextInput(attrs={'size': '100'})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = models.CustomUser.objects.filter(is_staff=True)
        return super(BlogAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def date_time_format(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ به روزرسانی', ordering='update_at')
    def update_time_format(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time_format',)
    list_filter = ('blog',)
    list_display = ('user', 'blog', 'text_show', 'is_parent', 'date_time_format')
    search_fields = ('user', 'blog', 'text')

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def date_time_format(self, obj):
        return obj.created_at.strftime("%Y/%m/%d - %H:%M")
