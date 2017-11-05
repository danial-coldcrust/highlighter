from django.contrib import admin
from .models import Project,Comment,Tag,Todo

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user','id','title','status','created_at','updated_at','like']

    #리스트값들이 내모델클래스의 필드와일치해야 함

    actions = ['make_published','make_drafted']

        #함수만들어서 리스트에 등록가능하면 내커스필드가 생김

    def make_published(self, request, queryset):
        updated_count = queryset.update(status='p')
        self.message_user(request, '{}건의 프로젝트를발행상태로 변경'.format(updated_count))

    def make_drafted(self, request, queryset):
        updated_count = queryset.update(status='d')
        self.message_user(request, '{}건의 프로젝트를드래프상태로 변경'.format(updated_count))

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
        pass

@admin.register(Todo)
class CommentAdmin(admin.ModelAdmin):
        pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']