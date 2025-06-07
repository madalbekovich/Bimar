from rest_framework import serializers
from . import models
from apps.products.models import Product
from django.core.validators import ValidationError
from apps.users.models import User
from django.db import transaction

class ProductObjectSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    count = serializers.IntegerField(min_value=1)

class BonusPurchaseSerializer(serializers.ModelSerializer):
    product_for_order = ProductObjectSerializer(many=True)
    bonus_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.PurchasesHistory
        fields = ['bonus_id', 'product_for_order']

    def validate_bonus_id(self, value):
        """Проверяем существование пользователя"""
        try:
            User.objects.get(bonus_id=value)
        except User.DoesNotExist:
            raise ValidationError("Пользователь с указанным bonus_id не найден")
        return value

    def validate_product_for_order(self, value):
        """Проверяем существование всех товаров"""
        for item in value:
            product_code = item['product_id']
            if not Product.objects.filter(code=product_code).exists():
                raise ValidationError(f"Товар с кодом {product_code} не найден")
        return value

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('product_for_order')
        bonus_id = validated_data.pop('bonus_id')

        user = User.objects.get(bonus_id=bonus_id)

        total_bonus = 0
        purchase_records = []

        for item_data in products_data:
            product_code = item_data['product_id']
            count = item_data['count']

            product = Product.objects.get(code=product_code)

            item_bonus = (product.bonus_count * count) if hasattr(product, 'bonus_count') else 0
            total_bonus += item_bonus
            print("INFO+", item_bonus)

            purchase_record = models.PurchasesHistory(
                user=user,
                product_id=product,
                count=count,
                bonus_count=item_bonus,
                total_price=product.price * count if hasattr(product, 'price') else 0,
                location=product.location,
                price_for=product.price_for,
            )
            purchase_records.append(purchase_record)

        models.PurchasesHistory.objects.bulk_create(purchase_records)

        if total_bonus > 0:
            user.bonus = (user.bonus or 0) + total_bonus
            user.save(update_fields=['bonus'])

        return {
            'user': user,
            'total_bonus': total_bonus,
            'purchases': purchase_records
        }


