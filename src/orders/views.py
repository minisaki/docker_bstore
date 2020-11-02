from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from cart.cart import Cart
from django.views import View
from .tasks import order_created
from shop.recommender import Recommender
# create invoice
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


class OrderCreate(View):
    def post(self, request):
        list_products = []
        cart = Cart(request)
        if cart:
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            gender = int(request.POST['gender'])
            address = request.POST['address']
            phone = request.POST['phone']
            postal_code = request.POST['postal_code']
            order = Order.objects.create(first_name=first_name, last_name=last_name,
                                         email=email, gender=gender,
                                         address=address, phone=phone,
                                         postal_code=postal_code)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['cart_product'],
                                         price=item['price'], quantity=item['quantity'])
                list_products.append(item['cart_product'])
            r = Recommender()
            r.products_bought(list_products)
            cart.clear()
            order_created.delay(order.id)
            message = "Đặt hàng thành công"
            return render(request, 'shop/order/created.html', {'order': order,
                                                           'message': message})
        else:
            message = "Chưa có giỏ hàng"
            return render(request, 'shop/order/created.html', {'message':message})

    def get(self, request):
        return render(request, 'shop/order/created.html')


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # print(order.first_name)
    # print(order.items.all())
    # for item in order.items.all():
    #     print(item.product.name)
    return render(request, 'invoice/invoice.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('invoice/invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'invoice.css')])
    return response