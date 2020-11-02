from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import View
from .models import Category, Product
from .recommender import Recommender, GetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings
# Create your views here.
# import redis
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
import weasyprint


# rr = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
#                 db=settings.REDIS_DB)
categories = Category.objects.all()
r1 = GetView()


class Index(LoginRequiredMixin, View):
    login_url = 'account:login'

    def get(self, request):
        products = Product.objects.all()
        view = {}
        for product in products:
            # score = rr.zscore('score', product.id)
            score = r1.get_score('score', product.id)
            if score:
                score = math.floor(score)
                view[product.id] = str(score)
        print(view)
        # phân trang cho sản phẩm
        paginator = Paginator(products, 8)
        page = request.GET.get('page_number')
        print(page)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
            print(products)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            products = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'shop/main_content_ajax.html', {'categories': categories, 'products': products,
                                                                   'score': view, 'page': page})
        return render(request, 'shop/main_content.html',
                      {'categories': categories, 'products': products, 'score': view, 'page': page})

    def post(self, request):
        product_id = request.POST.get('id1')
        action = request.POST.get('action1')
        print(product_id)
        print(action)
        if product_id and action:
            product = Product.objects.get(id=product_id)
            if action == 'like':
                product.user_like.add(request.user)
            else:
                product.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})

        return JsonResponse({'status': 'error'})


class ProductList(View):
    def get(self, request, category_slug):
        # categories = Category.objects.all()
        products = Product.objects.all()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products_list = Product.objects.filter(category=category)
            return render(request, 'shop/product_list.html',
                      {'products': products, 'categories': categories,
                       'category': category, 'products_list': products_list})


class ProductDetail(View):
    def get(self, request, id, product_slug):
        # categories = Category.objects.all()
        products = Product.objects.all()
        product_detail = Product.objects.get(id=id, slug=product_slug)
        category = Category.objects.get(name=product_detail.category)
        r = Recommender()
        
        
        recommended_products = r.suggest_products_for([product_detail], 4)
        # total_view = r1.total_view(id)
        # rr.zincrby('score', 1, id)
        total_view = r1.save_score('score', id)
        return render(request, 'shop/product/single_product.html',
                    {'product_detail': product_detail, 'products': products,
                    'categories': categories, 'category': category,
                    'recommended_products': recommended_products, 'total_view': total_view})
        
        # return render(request, 'shop/product/single_product.html',
        #                 {'product_detail': product_detail, 'products': products,
        #                 'categories': categories, 'category': category,
        #                 'total_view': total_view})


@staff_member_required
def admin_qrcode(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # html = render_to_string('qrcode/qrcode.html', {'products': products})
    # response = HttpResponse(content_type='application/pdf')
    # # response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'invoice.css')])
    # return response
    return render(request, 'qrcode/qrcode.html', {'product': product, 'loop_times': range(10)})


def scan_qr(request):
    return render(request, 'qrcode/scanqr.html')


