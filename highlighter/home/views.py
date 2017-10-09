from django.shortcuts import render
from .models import Project
# Create your views here.

def project_list(request):
    qs = Project.objects.all()

    q = request.GET.get('q','')
    if q:
        qs = qs.filter(title__icontains=q)

    return render(request, 'project_list.html',{
        'project_list':qs,
        'q':q,
    })
