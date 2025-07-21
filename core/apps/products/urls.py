from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('list/', views.ProductListView.as_view()),
    path('detail/<int:id>/', views.ProductDetailListView.as_view()),
    path('<int:category_id>/', views.ProductCategoryListView.as_view()),
    path('promotions/', views.PromotionListView.as_view()),
    path('<int:barcode_id>/', views.SearchProductView.as_view()),
    path('similar/<int:category_id>/', views.SimilarProductView.as_view()),
    path('best/', views.PromoActionProductView.as_view()),
    path('best-all/', views.PromoActionAllProductView.as_view()),

    path('set-featured/', views.SetFeaturedToProductView.as_view()),
    path('list-featured/', views.FeaturedProductListView.as_view()),
]
