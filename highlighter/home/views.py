from django.http import Http404
from django.shortcuts import get_object_or_404,render
from .models import Project
# Create your views here.

def project_list(request):
    qs = Project.objects.all()

    q = request.GET.get('q','')
    if q:
        qs = qs.filter(title__icontains=q)

    return render(request, 'home/project_list.html', {
        'project_list':qs,
        'q':q,
    })

def project_detail(request,id):
    # try:
    #     project = Project.objects.get(id=id)
    # except Project.DoesNotExist:
    #     raise  Http404

    project = get_object_or_404(Project, id=id)
    return render(request, 'home/project_detail.html', {
        'project' : project
    })