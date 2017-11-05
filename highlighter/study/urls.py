from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.study_list, name='study_list'),
    url(r'^(?P<id>\d+)/$',views.study_detail),
    url(r'^(?P<id>\d+)/participate$', views.study_participate, name='study_participate'),
]