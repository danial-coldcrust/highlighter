from django.shortcuts import render
from django.shortcuts import get_object_or_404,render
from .models import Study
# Create your views here.

def study_list(request):
    qs = Study.objects.all()

    q = request.GET.get('q','')
    if q:
        qs = qs.filter(title__icontains=q)

    return render(request, 'study_list.html',{
        'study_list':qs,
        'q':q,
    })


def study_detail(request,id):
    # try:
    #     project = Project.objects.get(id=id)
    # except Project.DoesNotExist:
    #     raise  Http404

    study = get_object_or_404(Study, id=id)
    return render(request, 'study_detail.html', {
        'study' : study
    })