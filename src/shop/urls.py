from django.urls import path
from .views import Index, ProductDetail, ProductList, admin_qrcode, scan_qr


app_name = 'shop'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:category_slug>', ProductList.as_view(),
         name='product_list'),
    path('<int:id>/<slug:product_slug>', ProductDetail.as_view(),
         name='product_detail'),
    path('admin/qr_code/<int:product_id>/', admin_qrcode, name='qrcode'),
    path('scanqr/', scan_qr, name='scan_qr'),

]