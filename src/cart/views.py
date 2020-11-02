from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from shop.models import Product
from django.views import View
from shop.recommender import Recommender
# Create your views here.


class CartAdd(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        quantity = request.POST['qtybutton']
        size = request.POST['product-size']
        color = request.POST['product-color']
        cart.add(product=product, quantity=quantity, size=size, color=color)

        cart.save()
        return redirect('cart:cart_detail')


class CartRemove(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartUpdate(View):
    def post(self, request, product_id, size, color):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        quantity = request.POST['qtybutton']
        size = request.POST['product-size']
        color = request.POST['product-color']
        cart.update(product=product, quantity=quantity, size=size, color=color)
        cart.save()
        return redirect('cart:cart_detail')


class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
        if cart:
            r = Recommender()
            cart_products = [item['cart_product'] for item in cart]
            recommended_products = r.suggest_products_for(cart_products,
                                                      max_results=10)
            return render(request, 'shop/cart/cart_detail.html', {'cart': cart,
                                                              'recommended_products': recommended_products})
        return redirect('shop:index')



