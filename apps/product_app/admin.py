from django.contrib import admin
from jalali_date import datetime2jalali
from . import models
from django import forms
from django.db import models as m
from.forms import ProductAdminForm


class CommentAdmin(admin.StackedInline):
    model = models.Comment
    readonly_fields = ('get_created_jalali',)
    extra = 0

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


class ProductImageAdmin(admin.StackedInline):
    model = models.ProductImage
    extra = 0


class TipAAdmin(admin.TabularInline):
    model = models.TipA
    extra = 0
    max_num = 1
    formfield_overrides = {
        m.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '25'})},
    }


class ProductCustomFilter(admin.SimpleListFilter):
    title = "دسته بندی"
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "category__id__exact"

    def lookups(self, request, model_admin):
        category = models.Category.objects.filter(parent__isnull=False)
        return [(obj.id, obj.title) for obj in category]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    readonly_fields = ('update_jalali', 'created_jalali')
    ordering = ('-created_at',)
    list_display = ('product_name', 'price', 'status', 'selected_product', 'update_jalali', 'created_jalali')
    list_filter = ('status', ProductCustomFilter)
    search_fields = ('product_name', 'slug')
    inlines = (ProductImageAdmin, TipAAdmin, CommentAdmin)
    prepopulated_fields = {'slug': ('product_name',)}
    filter_horizontal = ('category', 'tag')
    list_editable = ('price', 'status', 'selected_product')
    formfield_overrides = {
        m.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '25'})},
        m.PositiveSmallIntegerField: {'widget': forms.NumberInput(attrs={'size': '15'})},
        m.SlugField: {'widget': forms.TextInput(attrs={'size': 70})},
        m.CharField: {'widget': forms.TextInput(attrs={'size': 70})},
    }

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    @admin.display(description='تاریخ آپدیت', ordering='update_at')
    def update_jalali(self, obj):
        return datetime2jalali(obj.update_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time_format',)
    list_display = ('title', 'slug', 'date_time_format')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def date_time_format(self, obj):
        return obj.created_at.strftime("%Y/%m/%d")


class CategoryCustomFilter(admin.SimpleListFilter):
    title = "دسته بندی"
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "parent__id__exact"

    def lookups(self, request, model_admin):
        category = models.Category.objects.filter(parent=None)
        return [(obj.id, obj.title) for obj in category]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__id__exact=self.value())


@admin.register(models.BaseCategory)
class BaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time_format',)
    ordering = ('-created_at',)
    list_display = ('title', 'parent', 'base_category', 'slug', 'id', 'date_time_format')
    list_filter = ('base_category', CategoryCustomFilter)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = models.Category.objects.filter(parent__isnull=True)
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def date_time_format(self, obj):
        return obj.created_at.strftime("%Y/%m/%d - %H:%M")


class CommentReplyAdmin(admin.StackedInline):
    model = models.CommentReply
    extra = 0
    readonly_fields = ('responder', 'responder_name_persistent', 'get_created_jalali')
    ordering = ('-created_at',)

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = (CommentReplyAdmin,)
    readonly_fields = ('get_created_jalali',)
    list_display = ('user', 'product', 'get_created_jalali', 'has_response')
    list_filter = ('created_at',)
    search_fields = ('user', 'product')
    ordering = ('-created_at',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.responder = request.user
            instance.responder_name_persistent = f'{request.user.first_name} {request.user.last_name}'
            instance.save()
        formset.save_m2m()

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')
