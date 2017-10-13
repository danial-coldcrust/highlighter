from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$',views.project_new,name="project_new"),
    url(r'^(?P<id>\d+)/edit/$',views.project_edit),

    url(r'^$',views.project_list, name='project_list'),
    url(r'^(?P<id>\d+)/$',views.project_detail, name='project_detail'),
    url(r'^(?P<id>\d+)/like$',views.project_like, name='project_like'),
]