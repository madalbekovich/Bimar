from django.contrib import admin
from . import models

admin.site.register(models.News)
admin.site.register(models.StoreBranch)
admin.site.register(models.FAQ)

class StoryVideosTabularInline(admin.TabularInline):
    extra = 1
    model = models.StoryVideo


@admin.register(models.Story)
class StoryModelAdmin(admin.ModelAdmin):
    inlines = [StoryVideosTabularInline]
    list_display = ['id']