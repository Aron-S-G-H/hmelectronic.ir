from django.contrib import admin
from . import models
from django.urls import reverse
from django.utils.safestring import mark_safe
import csv
from django.http import HttpResponse
from jalali_date import datetime2jalali
from django import forms
from django.db import models as djmodels


def user_invoice_pdf(order):
    url = reverse('cart:admin_invoice_page', args=[order.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


user_invoice_pdf.short_description = 'Export to PDF'


class ProductOrderAdmin(admin.StackedInline):
    model = models.ProductOrder
    extra = 0

    formfield_overrides = {
        djmodels.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '20'})},
        djmodels.CharField: {'widget': forms.TextInput(attrs={'size': '70'})},
    }


@admin.register(models.UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    inlines = (ProductOrderAdmin,)
    list_filter = ('is_paid', 'created_at', 'city')
    list_display = ('user', 'phone', 'total_price', 'city', 'is_paid', 'get_created_jalali', user_invoice_pdf)
    readonly_fields = ('get_created_jalali',)
    search_fields = ('email', 'postal_code', 'phone', 'id')
    actions = ['export_as_csv']
    formfield_overrides = {
        djmodels.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '20'})},
    }

    @admin.display(description='تاریخ ثبت سفارش', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d - %H:%M')

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta.verbose_name)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export as CSV"
