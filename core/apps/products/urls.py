from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('list/', views.ProductListView.as_view()),
    path('promotions/', views.PromotionListView.as_view()),
    path('<int:barcode_id>/', views.SearchProductView.as_view()),
]