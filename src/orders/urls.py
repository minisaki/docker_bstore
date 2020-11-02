from django.urls import path
from .views import OrderCreate
from . import views


app_name = 'orders'
urlpatterns = [
    path('', OrderCreate.as_view(), name='order_create'),
    path('admin/invoice/<int:order_id>/', views.admin_order_detail, name='invoice_oder_detail'),
    path('admin/invoice/<int:order_id>/pdf/', views.admin_order_pdf, name='invoice_oder_pdf'),

]