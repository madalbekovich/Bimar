from typing import Dict
from . import models
from apps.users.models import User
from datetime import datetime

def save_history_purchases(user_id: int, *args, **kwargs) -> None:
    user = User.objects.get(id=user_id)
    product_id = kwargs.get('product_id', '')
    count = kwargs.get('count', '')
    bonus_count = kwargs.get('bonus_count', '')
    total_price = kwargs.get('total_price', '')
    location = kwargs.get('location', '')
    price_for = kwargs.get('price_for', '')
    created_at = datetime.now()

    obj = models.PurchasesHistory.objects.create(
        user=user,
        product_id=product_id,
        count=count,
        bonus_count=bonus_count,
        total_price=total_price,
        location=location,
        price_for=price_for,
        created_at=created_at
    )
    obj.save()

def set_purchases(item):
    pass