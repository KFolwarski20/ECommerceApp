import redis

from django.conf import settings

from .models import Product


r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class Recommender(object):

    @staticmethod
    def get_product_key(product_id):
        return f'product:{product_id}:purchased_with'

    def products_bought(self, products):
        product_ids = [
            product.pk for product in products
        ]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(
                        self.get_product_key(product_id),
                        1,
                        with_id
                    )

    def suggest_products_for(self, products, max_results=6):
        product_ids = [
            product.pk for product in products
        ]
        if len(product_ids) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0,
                -1,
                desc=True
            )[:max_results]
        else:
            flat_ids = ''.join([str(product_id) for product_id in product_ids])
            tmp_key = 'tmp{}'.format(flat_ids)
            keys = [
                self.get_product_key(product_id) for product_id in product_ids]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(
                tmp_key,
                0,
                -1,
                desc=True
            )[:max_results]

            r.delete(tmp_key)

        suggested_products_ids = [int(product_id) for product_id in suggestions]

        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))

        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products

    def clear_purchases(self):
        for product_id in Product.objects.values_list(
                'pk',
                flat=True
        ):
            r.delete(
                self.get_product_key(product_id)
            )
