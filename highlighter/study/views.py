from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404,render
from .models import Study
from accounts.models import Profile
from accounts.models import User
from .forms import ProjectForm
from home.models import Project

# Create your views here.

def study_list(request):
    qs = Study.objects.all()
    q = request.GET.get('q','')
    if q:
        qs = qs.filter(title__icontains=q)

    return render(request, 'study/study_list.html', {
        'study_list':qs,
        'q':q,
    })


def study_detail(request,id):
    study = get_object_or_404(Study, id=id)
    # I'm not sure why .filter but just .get() is schema design error
    # https://stackoverflow.com/questions/22063748/django-get-returned-more-than-one-topic
    project = Project.objects.filter(type=id)


    return render(request, 'study/study_detail.html', {
        'study' : study,
        'project' : project,
    })


def study_participate(request,id):
    study = get_object_or_404(Study, id=id)
    login_user = request.user
    user = get_object_or_404(User, username=login_user)
    profile= get_object_or_404(Profile, user_id=user.id)
    study.user_set.add(profile.id)
    study.save()

    return render(request, 'study/study_detail.html', {
        'study' : study
    })


def study_makeproject(request,id):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        project = Project()

        login_user = request.user
        user = get_object_or_404(User, username=login_user)

        study = get_object_or_404(Study, id=id)

        if form.is_valid():
            project.user_id = user.id
            project.title = form.cleaned_data['title']

            project.body = form.cleaned_data['body']
            project.status= "p"
            project.like= 0
            project.type = study
            project.save()
            return redirect('/study/')



    else:
        form = ProjectForm()
    return render(request,'study/study_makeproject.html',{
        'form':form,
    })
