from django.db import models
from apps.users.models import User
from apps.products.models import Product
from apps.main.models import StoreBranch
from apps.products import choices

class PurchasesHistory(models.Model):
    """История покупки и зачисления бонусов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.IntegerField(default=0)
    bonus_count = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    location = models.ForeignKey(StoreBranch, on_delete=models.CASCADE)
    price_for = models.CharField(verbose_name="Цена за", choices=choices.PRICE_FOR_CHOICES, default="шт", max_length=500, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')