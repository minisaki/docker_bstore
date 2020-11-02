from django.contrib import admin
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_detail(obj):
    url = reverse('orders:invoice_oder_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


order_detail.short_description = 'Order View'


def order_pdf(obj):
    url = reverse('orders:invoice_oder_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'gender','address',
                    'phone', 'create', 'update', 'postal_code', 'paid', order_detail, order_pdf]
    list_filter = ['create', 'update', 'paid']
    inlines = [OrderItemInline]

