from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create()

        self.category.set_current_language('pl')
        self.category.name = 'Telefony'
        self.category.slug = 'telefony'
        self.category.save()

    def test_category_str(self):
        self.assertEqual(
            str(self.category),
            'Telefony'
        )


class ProductModelTest(TestCase):

    def setUp(self):

        self.category = Category.objects.create()

        self.category.set_current_language('pl')
        self.category.name = 'Telefony'
        self.category.slug = 'telefony'
        self.category.save()

        self.product = Product.objects.create(
            category=self.category,
            price=2999.99,
            stock=5,
            available=True
        )

        self.product.set_current_language('pl')
        self.product.name = 'iPhone'
        self.product.slug = 'iphone'
        self.product.save()

    def test_product_str(self):

        self.assertEqual(
            str(self.product),
            'iPhone'
        )

    def test_product_absolute_url(self):

        url = self.product.get_absolute_url()

        self.assertEqual(
            url,
            f'/pl/{self.product.pk}/{self.product.slug}/'
        )


class ProductViewTest(TestCase):

    def test_product_list_url(self):

        response = self.client.get(
            reverse('shop:product_list')
        )

        self.assertEqual(
            response.status_code,
            200
        )
