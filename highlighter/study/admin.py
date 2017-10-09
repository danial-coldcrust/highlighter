from django.contrib import admin
from .models import Study

@admin.register(Study)
class CommentAdmin(admin.ModelAdmin):
        pass