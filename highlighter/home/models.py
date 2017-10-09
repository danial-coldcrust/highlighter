from django.db import models
from django.conf import settings

class Project(models.Model):

    STATUS_CHOICES = (
        ('d','Draft'),
        ('p', 'Published'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    tag_set = models.ManyToManyField('Tag',blank=True)
    #태그는솔찍히빈칸이여도됨빈칸으로하면에러남
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    project = models.ForeignKey(Project)
    author = models.CharField(max_length=20)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class Todo(models.Model):
    project = models.ForeignKey(Project)
    todo= models.CharField(max_length=20)
    completed= models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.todo

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True) #태그는중복되면안되니깐
    def __str__(self):
        return self.name