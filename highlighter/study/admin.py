from django.contrib import admin
from .models import Study,GroupTodo

@admin.register(Study)
class CommentAdmin(admin.ModelAdmin):
        pass

@admin.register(GroupTodo)
class CommentAdmin(admin.ModelAdmin):
        pass


