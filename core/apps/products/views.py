from rest_framework import generics
from . import serializers, models, filters
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter

class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryListSerializer


class ProductListView(generics.ListAPIView):
    """Список товаров"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    filter_backends = (rest_filter.DjangoFilterBackend, )
    filterset_class = filters.ProductFilter

class PromotionListView(generics.ListAPIView):
    """Список акции"""
    queryset = models.Product.objects.filter(is_promotion=True)
    serializer_class = serializers.ProductListSerializer

class SearchProductView(views.APIView):
    """QR-code-camera, поиск на наличие товара"""
    def get(self, request, barcode_id: str):
        try:
            queryset = models.Product.objects.get(code=barcode_id)
            serializer = serializers.ProductListSerializer(queryset).data
            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as _ex:
            return Response({"message": "Упс! Такой товар не найден"}, status=status.HTTP_404_NOT_FOUND)