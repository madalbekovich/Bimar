from . import serializers, models
from rest_framework import generics

class NotificationsListView(generics.ListAPIView):
    queryset = models.Notification.objects
    serializer_class = serializers.NotificationsSerializer

class StoriesListView(generics.ListAPIView):
    queryset = models.Story.objects.all().order_by("id")
    serializer_class = serializers.StoriesSerializers

class NewsListView(generics.ListAPIView):
    queryset = models.News.objects.all().order_by("-id")
    serializer_class = serializers.NewsSerializer

class NewsListDetailView(generics.RetrieveAPIView):
    queryset = models.News.objects.all().order_by("id")
    serializer_class = serializers.NewsSerializer
    lookup_field = 'id'

class StoreBranchListView(generics.ListAPIView):
    queryset = models.StoreBranch.objects.all()
    serializer_class = serializers.StoreBranchSerializer

class FAQListView(generics.ListAPIView):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer