from django.contrib import admin
from .models import Category, Product
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.


def qr_detail(obj):
    url = reverse('shop:qrcode', args=[obj.id])
    return mark_safe(f'<a href="{url}">Qr-code</a>')

qr_detail.short_description = 'QR'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'color', 'price', 'create', 'updated', 'image', 'quality', qr_detail]
    list_editable = ['price', 'quality',]
    prepopulated_fields = {'slug': ('name',)}

