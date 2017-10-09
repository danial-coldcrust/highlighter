from django.contrib import admin
from .models import Study,GroupTodo,Post

@admin.register(Study)
class CommentAdmin(admin.ModelAdmin):
        pass

@admin.register(GroupTodo)
class CommentAdmin(admin.ModelAdmin):
        pass


@admin.register(Post)
class CommentAdmin(admin.ModelAdmin):
        pass

