from django.contrib import admin
from .models import Project
# Register your models here.



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['author','id','title','created_at','updated_at']
    #리스트값들 이 내모델클래스 의필드  과일치해야 함