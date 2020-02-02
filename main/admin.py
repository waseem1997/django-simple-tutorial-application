from django.contrib import admin
from main import models


# Register your models here.

class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
        ("URL", {'fields': ["tutorial_slug"]}),
        ("Series", {'fields': ["tutorial_series"]}),
        ("Content", {"fields": ["tutorial_content"]})
    ]
    admin.site.register(models.TutorialCategory)
    admin.site.register(models.TutorialSeries)
    admin.site.register(models.Tutorial)
