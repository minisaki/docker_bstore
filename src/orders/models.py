from django.db import models
from shop.models import Product
# from decimal import Decimal, getcontext
from decimal import *
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Order(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    gender = models.BooleanField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    postal_code = models.CharField(max_length=10)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True,
                               blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(
                                                              100)])
    def __str__(self):
        return f'Orders {self.id}'

    def get_total_cost(self):
        # for item in self.items.all():
        #     print(item.get_cost())
        #     print('toi day')
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):

        if self.coupon:

            discount = (self.discount / Decimal(100) * Decimal(self.get_total_cost()))
            return discount
        return Decimal(0)

    def get_ship(self):
        if self.get_total_cost() >= 500:
            return 0
        return Decimal(30)

    def get_total_price_after_discount(self):
        print(self.get_discount())
        return self.get_total_cost() + self.get_ship() - self.get_discount()

    def convert_number_to_word(self):
        pass


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        # print('k toi day')
        # price = Decimal(self.price)
        # quantity = int(self.quantity)
        # kq = price * quantity
        # print(kq)
        return self.price*self.quantity