from django.db import models

class Project(models.Model):

    STATUS_CHOICES = (
        ('d','Draft'),
        ('p', 'Published'),
    )

    author = models.CharField(max_length=20) #빈칸이 면 안됨
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    tags = models.CharField(max_length=100,blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title