from django.db import models
from django.conf import settings

class Study(models.Model):

    #id는 자동생성
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='설명')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GroupTodo(models.Model):
    study = models.ForeignKey(Study)
    todo= models.CharField(max_length=20)
    completed= models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.todo

class Post(models.Model):

    STATUS_CHOICES = (
        ('d','Draft'),
        ('p', 'Published'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    study = models.ForeignKey(Study)
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title