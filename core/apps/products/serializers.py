from rest_framework import serializers
from . import models

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'img']

class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        model = models.Product
        fields = "__all__"