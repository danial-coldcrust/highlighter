from django.db import models
from django.contrib.auth.models import User
#회원관리 장고에서 지원해줌 근데 커스터마이징 불가

class Profile(models.Model):
    user = models.ForeignKey('auth.User') #FIXME:Bad case!!
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=50)