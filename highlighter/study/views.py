from django.shortcuts import render
from django.shortcuts import get_object_or_404,render
from .models import Study
from accounts.models import Profile
from accounts.models import User
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

    return render(request, 'study/study_detail.html', {
        'study' : study
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
