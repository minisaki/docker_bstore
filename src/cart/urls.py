from django.urls import path
from .views import CartAdd, CartRemove, CartDetail, CartUpdate


app_name = 'cart'
urlpatterns = [
    path('cart/', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:product_id>', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>', CartRemove.as_view(), name='cart_remove'),
    path('update/<int:product_id>', CartUpdate.as_view(), name='cart_update'),
]