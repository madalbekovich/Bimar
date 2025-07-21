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

class SetFeaturedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeaturedProduct
        fields = ['product', 'location']

class FeaturedProductListSerializer(serializers.ModelSerializer):
    preview_img = serializers.SerializerMethodField()
    price = serializers.CharField(source='product.price', read_only=True)
    price_for = serializers.CharField(source='product.price_for', read_only=True)
    class Meta:
        model = models.FeaturedProduct
        fields = ['preview_img', 'price', 'price_for', 'product', 'location']

    def get_preview_img(self, obj):
        if obj.product and obj.product.preview_img:
            return f"{settings.BASE_URL}media/{obj.product.preview_img}"
        return None
