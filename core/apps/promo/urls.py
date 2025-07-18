from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from . import views

router = DefaultRouter()
router.register(r'wh-bonus', views.BonusPurchaseViewSet, basename='bonus-purchases')

urlpatterns = [
    path('', include(router.urls)),

    # Принимает /write-off и /write-off/
    re_path(r'write-off/?$', views.BonusWriteOff.as_view()),

    # Принимает /current-bonus и /current-bonus/
    re_path(r'current-bonus/?$', views.CurrentBonusView.as_view()),
]
