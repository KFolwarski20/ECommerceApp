from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from typing import TYPE_CHECKING


class Category(TranslatableModel):
    if TYPE_CHECKING:
        name: str
        slug: str

    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True)
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(TranslatableModel):
    if TYPE_CHECKING:
        name: str
        slug: str

    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=models.TextField(blank=True),
    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])

    @property
    def in_stock(self):
        return self.available and self.stock > 0
