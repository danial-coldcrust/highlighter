from django.db import models
from django.conf import settings
from django import forms
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from django.urls import reverse
from study.models import Study


def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자이상입력하세요')
    pass

class Project(models.Model):

    STATUS_CHOICES = (
        ('d','Draft'),
        ('p', 'Published'),
    )

    #user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100, verbose_name='제목',validators=[min_length_3_validator])

    body = models.TextField(verbose_name='내용',default=".")
    photo = models.ImageField(blank=True, upload_to='home/project/%Y/%m/%d')
    # photo_thumbnail = ImageSpecField(source='photo', processors=[Thumbnail(300, 300)], format='JPEG',
    #                                         options={'quality', 60})
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="Draft")
    like = models.IntegerField(blank=True, default=0)
    tag_set = models.ManyToManyField('Tag',blank=True)
    #태그는솔찍히빈칸이여도됨
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Study,blank=True, null=True)

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

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    read = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)