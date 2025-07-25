﻿from django.db import models
from . import choices
from apps.main.models import StoreBranch
from apps.users.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    img = models.ImageField(upload_to="product/category/%Y_%m", verbose_name="Изображение")
    location = models.ForeignKey(StoreBranch, on_delete=models.CASCADE, verbose_name='Филиал')

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

class Product(models.Model):
    # is_popular = models.BooleanField(default=False, verbose_name=_('успей купить'))
    bonusAccrual = models.BooleanField(verbose_name="Зачисляется бонус", default=True)
    is_on_sale = models.BooleanField(verbose_name="Наличие товара", default=True)
    is_promotion = models.BooleanField(verbose_name="Товар находится в акции", default=False)
    is_popular = models.BooleanField(verbose_name="Популярный товар", default=False)
    is_new = models.BooleanField(verbose_name="Новый товар", default=False)
    best_product = models.BooleanField(verbose_name="Хит продаж", default=False)

    bonus_count = models.IntegerField(verbose_name='Кл-во бонусов при покупке товара', null=True, blank=True)
    preview_img = models.ImageField(verbose_name="Обложка", upload_to="product/preview_img", null=True, blank=True)
    location = models.ForeignKey(StoreBranch, on_delete=models.CASCADE, verbose_name='Филиал')
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(verbose_name="Название товара", max_length=300)
    description = models.TextField("Описание товара", blank=True, null=True)
    price = models.IntegerField(verbose_name="Цена")
    old_price = models.CharField(verbose_name="Старая цена", max_length=100, blank=True, null=True)
    discount_percentage = models.IntegerField(verbose_name='Процентная скидка', null=True, blank=True)
    code = models.CharField("Артикул", max_length=100, null=True, blank=True, unique=True)
    brand = models.CharField(verbose_name="Название брэнда", null=True, blank=True)
    country_production = models.CharField(verbose_name="Страна производства", )
    weight = models.CharField(verbose_name="Вес", null=True, blank=True)
    expiration_date = models.CharField(verbose_name="Срок годности", null=True, blank=True)
    nutritional_value = models.CharField(verbose_name="Пищевая ценность", null=True, blank=True)
    price_for = models.CharField(verbose_name="Цена за", choices=choices.PRICE_FOR_CHOICES, default="шт", max_length=500, editable=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения", blank=True, null=True)
    from_wh = models.BooleanField(editable=False, default=False)

    class Meta:
        verbose_name = "Товара"
        verbose_name_plural = "Товар"
        ordering = ["-id"]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(verbose_name="Картинки товара", upload_to="product/images/")



class FeaturedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(StoreBranch, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Избранное пользователя'
        verbose_name_plural = 'Избранные пользователей'

    def __str__(self):
        return f"Пользователь {self.user.username} добавил в корзину {self.product.title}."
