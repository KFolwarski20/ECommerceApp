from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from .recommender import Recommender


def product_list(request, category_slug=None):
    language = request.LANGUAGE_CODE

    category = None

    categories = Category.objects.prefetch_related(
        'translations'
    ).filter(
        translations__language_code=language
    )

    products = Product.objects.filter(
        available=True
    ).select_related(
        'category'
    ).prefetch_related(
        'translations'
    )

    if category_slug:
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug
        )
        products = products.filter(
            category=category
        )

    return render(
        request,
        'shop/product/list.html',
        {
                    'category': category,
                    'categories': categories,
                    'products': products
                }
        )


def product_detail(request, pk, slug):
    language = request.LANGUAGE_CODE

    product = get_object_or_404(
        Product.objects.select_related(
            'category'
        ).prefetch_related(
            'translations'
        ),
        pk=pk,
        translations__language_code=language,
        translations__slug=slug,
        available=True
    )
    cart_product_form = CartAddProductForm()

    recommended_products = Recommender().suggest_products_for(
        [product],
        4
    )

    return render(
        request,
        'shop/product/detail.html',
        {
                    'product': product,
                    'cart_product_form': cart_product_form,
                    'recommended_products': recommended_products
                }
        )
