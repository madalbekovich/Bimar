from rest_framework import serializers
from . import models
from apps.products.models import Product
from django.core.validators import ValidationError
from apps.users.models import User, BonusCard
from django.db import transaction


class ProductObjectSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    count = serializers.IntegerField(min_value=1)

    def to_internal_value(self, data):
        # Преобразуем count из строки в число, если нужно
        if 'count' in data and isinstance(data['count'], str):
            try:
                data['count'] = int(data['count'])
            except ValueError:
                raise serializers.ValidationError({'count': 'Должно быть числом'})
        return super().to_internal_value(data)


class BonusPurchaseSerializer(serializers.ModelSerializer):
    product_for_order = ProductObjectSerializer(many=True)
    bonus_id = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.PurchasesHistory
        fields = ['bonus_id', 'product_for_order']

    def validate_bonus_id(self, value):
        """Проверяем существование пользователя"""
        try:
            bonus_card = BonusCard.objects.get(bonus_id__bonus_id=value)
            if not bonus_card.user:
                raise ValidationError("Пользователь с указанным bonus_id не найден")
        except BonusCard.DoesNotExist:
            raise ValidationError("Пользователь с указанным bonus_id не найден")
        return value

    def validate_product_for_order(self, value):
        """Проверяем существование всех товаров"""
        for item in value:
            product_id = str(item['product_id'])  # Приводим к строке
            # Ищем продукт сначала по code, потом по id
            if not (Product.objects.filter(code=product_id).exists() or
                    Product.objects.filter(id=product_id).exists()):
                raise ValidationError(f"Товар с кодом/ID {product_id} не найден")
        return value

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('product_for_order')
        bonus_id = validated_data.pop('bonus_id')

        # Исправленный поиск пользователя
        bonus_card = BonusCard.objects.get(bonus_id__bonus_id=bonus_id)
        user = bonus_card.user

        total_bonus = 0
        purchase_records = []

        for item_data in products_data:
            product_id = str(item_data['product_id'])  # Приводим к строке
            count = item_data['count']

            # Ищем продукт сначала по code, потом по id
            try:
                product = Product.objects.get(code=product_id)
            except Product.DoesNotExist:
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise ValidationError(f"Товар с кодом/ID {product_id} не найден")

            # Безопасное получение значений с проверкой на None
            product_price = getattr(product, 'price', None) or 0
            product_bonus_count = getattr(product, 'bonus_count', None) or 0

            item_bonus = product_bonus_count * count
            total_bonus += item_bonus
            print("INFO+", item_bonus)

            purchase_record = models.PurchasesHistory(
                user=user,
                product_id=product,
                count=count,
                bonus_count=item_bonus,
                total_price=product_price * count,
                location=getattr(product, 'location', None),
                price_for=getattr(product, 'price_for', ''),
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