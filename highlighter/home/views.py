from django.shortcuts import render
from .models import Project
# Create your views here.

def project_list(request):
    qs = Project.objects.all()
    return render(request, 'project_list.html',{
        'project_list':qs,
    })
