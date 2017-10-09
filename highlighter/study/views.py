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
        'project_list':qs,
        'q':q,
    })
