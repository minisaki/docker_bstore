import redis
from django.conf import settings
from .models import Product
import math

#connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

# r = redis.Redis(host='re'', port=settings.REDIS_PORT,
# #                 db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id):
        return f'Sản phẩm : {id} đã mua với'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                #lấy các sản phẩm đã mau cùng với sản phẩm
                if product_id != with_id:
                    # tăng điểm cho sản phẩm mua cùng nhau
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        # print(len(products))
        # print('so san pham')
        if len(products) == 1:
            # chỉ có 1 sản phẩm
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0,
                                   -1, desc=True)[:max_results]
        else:
            # tạo khóa tạm thời
            flat_ids = '-'.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # print(tmp_key)
            # nhiều sản phẩm kết hợp tất cả số điểm các sản phẩm
            # lưu trữ tập hợp đc sắp xêps trong khóa tạm thời
            keys = [self.get_product_key(id) for id in product_ids]
            # print(keys)
            r.zunionstore(tmp_key, keys)
            # print(tmp_key)
            # print('tmp_key in lai')
            # xóa id cho các sản phẩm đề xuất
            r.zrem(tmp_key, *product_ids)
            # lấy id sản phẩm theo điểm số của họ, loại hậu duệ
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # xóa khóa tạm
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # đề xuất sản phẩm và sắp xếp theo thứ tự xuất hiện
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        # print(suggested_products)
        # print('so san pham lien quan')
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))


class GetView(object):
    def total_view(self, product_id):
        total_view = r.incr(product_id)
        r.delete(product_id)
        return total_view

    def save_score(self, name, product_id):
        score_save = r.zincrby(name, 1, product_id)
        score_save = math.floor(score_save)
        return score_save

    def get_score(self, name, product_id):
        score = r.zscore(name, product_id)
        return score


