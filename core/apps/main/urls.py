from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.NotificationsListView.as_view()),
    path("stories/", views.StoriesListView.as_view()),
    path("news/", views.NewsListView.as_view()),
    path("location/", views.StoreBranchListView.as_view()),
]