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
            project.user_id = '1'
            # 딕셔너리
            project.title = form.cleaned_data['title']
            project.content= form.cleaned_data['content']
            project.save()


            print(form.cleaned_data)
            return redirect('/home/')
        else:
            form.errors

    else:
        form = ProjectForm()
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