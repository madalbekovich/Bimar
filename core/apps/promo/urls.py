from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register(r'wh-bonus', views.BonusPurchaseViewSet, basename='bonus-purchases')

urlpatterns = [
    path('', include(router.urls)),
    path('write-off', views.BonusWriteOff.as_view()),
    path('current-bonus', views.CurrentBonusView.as_view())
]