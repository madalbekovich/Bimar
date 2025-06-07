from rest_framework import serializers
from . import models

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ["id", "title", "description", "created_at"]

class StoryVideosSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.StoryVideo
        fields = [
            "url",
            "created_at",
        ]

class StoriesSerializers(serializers.ModelSerializer):
    stories = StoryVideosSerializers(many=True)
    class Meta:
        model = models.Story
        fields = ["id", "title", "img", "created_at", "stories", "link"]

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'

class StoreBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreBranch
        fields = '__all__'