from unicodedata import category

from rest_framework import generics
from . import serializers, models, filters
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter

from rest_framework.permissions import (
    IsAuthenticated
)

class CategoryListView(generics.ListAPIView):
    """Список категорий"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryListSerializer
    filter_backends = (rest_filter.DjangoFilterBackend, )
    filterset_class = filters.CategoryFilter

class ProductListView(generics.ListAPIView):
    """Список товаров"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    filter_backends = (rest_filter.DjangoFilterBackend, )
    filterset_class = filters.ProductFilter

class ProductDetailListView(generics.RetrieveAPIView):
    """Деталь товара"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    lookup_field = 'id'

class PromotionListView(generics.ListAPIView):
    """Список акции"""
    queryset = models.Product.objects.filter(is_promotion=True)
    serializer_class = serializers.ProductListSerializer
    filter_backends = (rest_filter.DjangoFilterBackend, )
    filterset_class = filters.PromotionFilter

class SearchProductView(views.APIView):
    """QR-code-camera, поиск на наличие товара"""
    def get(self, request, barcode_id: str):
        try:
            queryset = models.Product.objects.get(code=barcode_id)
            serializer = serializers.ProductListSerializer(queryset).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as _ex:
            return Response({"message": "Упс! Такой товар не найден"}, status=status.HTTP_404_NOT_FOUND)

class SimilarProductView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    """Список похожих продуктов, на основе идентификатора категории"""
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return self.queryset.filter(category=category_id)
        return self.queryset.none()

class PromoActionProductView(generics.ListAPIView):
    """Хиты продаж"""
    queryset = models.Product.objects.filter(best_product=True)[:4]
    serializer_class = serializers.ProductListSerializer

class PromoActionAllProductView(generics.ListAPIView):
    """Хиты продаж все"""
    queryset = models.Product.objects.filter(best_product=True)
    serializer_class = serializers.ProductListSerializer

class ProductCategoryListView(generics.ListAPIView):
    """ПАСС"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return self.queryset.filter(category=category_id)
        return self.queryset.none()


class SetFeaturedToProductView(generics.CreateAPIView):
    """Добавить товара в корзину"""
    permission_classes = [IsAuthenticated]
    queryset = models.FeaturedProduct.objects.all()
    serializer_class = serializers.SetFeaturedProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FeaturedProductListView(generics.ListAPIView):
    """Моя корзина"""
    permission_classes = [IsAuthenticated]
    queryset = models.FeaturedProduct.objects.all()
    serializer_class = serializers.FeaturedProductListSerializer
    filter_backends = (rest_filter.DjangoFilterBackend, )
    filterset_class = filters.FeaturedFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
