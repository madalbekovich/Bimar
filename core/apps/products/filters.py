from email.policy import default

import django_filters as filters
from . import models

class ProductFilter(filters.FilterSet):
    """Сортировка товаров"""
    is_popular = filters.BooleanFilter(field_name='is_popular', label='По популярности')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte', label='По цене: сначала дешёвые')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte', label='По цене: сначала дорогие')
    location = filters.NumberFilter(field_name='location', label='Выбрать филиал')
    is_new = filters.BooleanFilter(field_name='is_new', label='Новинки')
    # ordering = filters.OrderingFilter('discount_percentage',)
    discount_price = filters.BooleanFilter(field_name='discount_percentage', label='По скидке')
    class Meta:
        model = models.Product
        fields = ['is_popular', 'min_price', 'max_price', 'is_new', 'discount_price']

class CategoryFilter(filters.FilterSet):
    """Сортировка категории"""
    location = filters.NumberFilter(field_name='location', label='Выбрать филиал')

class PromotionFilter(filters.FilterSet):
    """Сортировка акции"""
    location = filters.NumberFilter(field_name='location', label='Выбрать филиал')