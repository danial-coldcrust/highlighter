from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404,render,redirect
from .models import Project
from accounts.models import Profile
from accounts.models import User
from .forms import ProjectForm
# Create your views here.

def project_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():#모든validate호출하기
            project = Project()
            project = form.save()
            messages.success(request,' 새 포스팅을 저장했다습니다')

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

ulist = list()
plist = list()
def project_like(request,id):
    project = get_object_or_404(Project, id=id)
    login_user = request.user
    user = User.objects.get(username=login_user)
    profile = Profile.objects.get(user_id=user.id)


    if login_user in ulist and project.id in plist:
        pass
    else:
        project.like += 1
        project.save()
        ulist.append(login_user)
        plist.append(project.id)
        profile.array_rated_project_indexs += (project.title+', ')
        profile.save()

    return redirect('/home/'+id)
