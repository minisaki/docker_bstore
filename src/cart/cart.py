from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity, size, color):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(
                product.price), 'size': size, 'color': color}
        elif product_id in self.cart:
            quantity = int(self.cart[product_id]['quantity']) + int(quantity)
            self.cart[product_id]['quantity'] = str(quantity)
        self.save()

    def update(self, product, quantity, size, color):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['size'] = size
            self.cart[product_id]['color'] = color
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        cart_product_ids = self.cart.keys()
        cart_products = Product.objects.filter(id__in=cart_product_ids)
        cart = self.cart.copy()
        for cart_product in cart_products:
            cart[str(cart_product.id)]['cart_product'] = cart_product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = int(item['quantity']) * item['price']
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price'])*int(item['quantity']) for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        if self.coupon_id:
            del self.session['coupon_id']
        self.save()


    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100) * self.get_total_price())
        return Decimal(0)

    def get_ship(self):
        if self.get_total_price() >= Decimal(500):
            return 0
        return Decimal(30)

    def get_total_price_after_discount(self):
        if self.coupon:
            return self.get_total_price() + self.get_ship() - self.get_discount()
        return self.get_total_price() + self.get_ship()