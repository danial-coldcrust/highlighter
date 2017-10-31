from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404,render,redirect
from .models import Project
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import ProjectForm
# Create your views here.
import math, random
from collections import defaultdict, Counter

from haystack.query import SearchQuerySet



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


    a = request.GET.get('a','')
    fq = request.GET.get('q', '')
    if a:
        qs = qs.filter(title__icontains=a)
    if fq:
        results = SearchQuerySet().models(Project).filter(content=fq)
        for t in results:
            print(t.text)


    return render(request, 'home/project_list.html', {
        'project_list':qs,
        'q':a,
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



u_dict = {}
def project_like(request,id):

    project = get_object_or_404(Project, id=id)
    login_user = request.user
    user = get_object_or_404(User,username=login_user)
    profile = get_object_or_404(Profile,user_id=user.id)

    if login_user in u_dict and project.id in u_dict[login_user]:
        print("login_usr: {}, project.id: {}",format(login_user),format(project.id))
        pass
    else:
        project.like += 1
        project.save()
        if login_user in u_dict:
            global dict
            u_dict[login_user].add(project.id)
        else:
            u_dict[login_user] = set()
            u_dict[login_user].add(project.id)

        print(u_dict)


        profile.array_rated_project_indexs += (str(project.id)+',')
        profile.save()

    return redirect('/home/'+id)

def project_rcmd(request):
    login_user = request.user
    User = get_user_model()
    user = get_object_or_404(User,username=login_user)
    profile = get_object_or_404(Profile, user_id=user.id)
    login_user_rated_list_field = profile.array_rated_project_indexs
    users = User.objects.all()

    login_user_rated_list = login_user_rated_list_field.split(',')[0:-1]
    print(login_user_rated_list)
    users_interests = []
    login_user_id = None

    # for cnt in range(len(users)):
    #     profile = get_object_or_404(Profile, user_id=users[cnt].id)
    #     users_profile_rated = profile.array_rated_project_indexs.split(',')[0:-1]
    #     print(users_profile_rated)
    #
    #     if login_user_rated_list == users_profile_rated:
    #         login_user_id = cnt
    #         # print(login_user_id)
    #         users_interests.append(users_profile_rated)
    #     else:
    #         users_interests.append(users_profile_rated)

    for user in users:
        print(user.id,user)
        profile = get_object_or_404(Profile,user_id=user.id)
        users_profile_rated = profile.array_rated_project_indexs.split(',')[0:-1]
        users_interests.append(users_profile_rated)

    for cnt in range(len(users_interests)):
        if login_user_rated_list == users_interests[cnt]:
            login_user_id = cnt
            print(cnt)

    #print(users_interests)
    #print(login_user_id)


    def dot(v, w):
        return sum(v_i * w_i for v_i, w_i in zip(v, w))

    def cosine_similarity(v, w):
        return dot(v, w) / math.sqrt(dot(v, v) * dot(w, w))

    unique_interests = sorted(list({interest
                                    for user_interests in users_interests
                                    for interest in user_interests}))
    #print("unique_interests", unique_interests)

    def make_user_interest_vector(user_interests):
        return [1 if interest in user_interests else 0 for interest in unique_interests]

    # print("make_user_interest_vector:",make_user_interest_vector(users_interests[0]))
    # print("make_user_interest_vector:",make_user_interest_vector(users_interests[1]))


    user_interest_matrix = list(map(make_user_interest_vector, users_interests))
    ##print(user_interest_matrix)

    # inverse
    interest_user_matrix = [[user_interest_vector[j]
                             for user_interest_vector in user_interest_matrix]
                            for j, _ in enumerate(unique_interests)]
    ##print(interest_user_matrix)

    interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                              for user_vector_j in interest_user_matrix]
                             for user_vector_i in interest_user_matrix]

    #print(interest_similarities)






    def most_similar_interests_to(interest_id):
        similarities = interest_similarities[interest_id]
        pairs = [(unique_interests[other_interest_id], similarity)
                 for other_interest_id, similarity in enumerate(similarities)
                 if interest_id != other_interest_id and similarity > 0]
        return sorted(pairs,
                      key=lambda pair: pair[1],
                      reverse=True)

    #print('most_similar_interests_to:',most_similar_interests_to(login_user_id))

    def item_based_suggestions(user_id, include_current_interests=False):
        suggestions = defaultdict(float)
        user_interest_vector = user_interest_matrix[user_id]
        for interest_id, is_interested in enumerate(user_interest_vector):
            if is_interested == 1:
                similar_interests = most_similar_interests_to(interest_id)
                for interest, similarity in similar_interests:
                    suggestions[interest] += similarity

        suggestions = sorted(suggestions.items(),
                             key=lambda pair: pair[1],
                             reverse=True)

        if include_current_interests:
            return suggestions
        else:
            # return [(suggestion, weight)
            return [suggestion
                    for suggestion, weight in suggestions
                    if suggestion not in users_interests[user_id]]

    #print("item_based_suggestions",item_based_suggestions(login_user_id))

    #render with project_list
    #project = get_object_or_404(Project, id=login_user_id)

    return render(request, 'home/project_rcmd.html',{
        'item_based_suggestions': item_based_suggestions(login_user_id)
    })