from django.http import Http404
from django.shortcuts import get_object_or_404,render,redirect
from .models import Project
from .forms import ProjectForm
# Create your views here.

def project_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():#모든validate호출하기
            project = Project()
            project = form.save()

            return redirect('/home/')
        else:
            form.errors

    else:
        form = ProjectForm()
        #처음에열릴때

    return render(request,'home/project_form.html',{
        'form': form,
    })

def project_edit(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project) #project_new에인스턴스추가만하면 수정기능 끝
        if form.is_valid():#모든validate호출하기
            project = Project()
            project = form.save()

            return redirect('/home/')
        else:
            form.errors

    else:
        form = ProjectForm(instance=project) #project_new에인스턴스추가만하면 수정기능 끝
        #처음에열릴때

    return render(request,'home/project_form.html',{
        'form': form,
    })

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