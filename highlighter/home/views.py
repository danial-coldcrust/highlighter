
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

import json
from django.http import HttpResponse
from haystack.query import SearchQuerySet

from random import sample, randint


def project_new(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():#모든validate호출하기
            project = Project()
            project = form.save()
            messages.success(request,' 새 포스팅을 저장했습니다')

            return redirect('/homee/')
        else:
            form.errors

    else:
        form = ProjectForm()
        #처음에열릴때

    return render(request,'homee/project_form.html',{
        'form': form,
    })

def project_edit(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project) #project_new에인스턴스추가만하면 수정기능 끝
        if form.is_valid():#모든validate호출하기
            project = Project()
            project = form.save()

            return redirect('/homee/')
        else:
            form.errors

    else:
        form = ProjectForm(instance=project) #project_new에인스턴스추가만하면 수정기능 끝
        #처음에열릴때

    return render(request,'homee/project_form.html',{
        'form': form,
    })

def project_list(request):
    qs = Project.objects.all()


    a = request.GET.get('a','')

    if a:
        qs = qs.filter(title__icontains=a)
        print(qs)


    return render(request, 'homee/project_list.html', {
        'project_list':qs,
        # 'project_list_full':sqs,
        'q':a,
    })





def project_detail(request,id):
    # try:
    #     project = Project.objects.get(id=id)
    # except Project.DoesNotExist:
    #     raise  Http404

    project = get_object_or_404(Project, id=id)
    return render(request, 'homee/project_detail.html', {
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

        # print(u_dict)


        profile.array_rated_project_indexs += (str(project.id)+',')
        profile.save()

    return redirect('/homee/'+id)

def project_rcmd(request):
    login_user = request.user

    User = get_user_model()
    user = get_object_or_404(User,username=login_user)
    profile = get_object_or_404(Profile, user_id=user.id)
    login_user_rated_list_field = profile.array_rated_project_indexs
    users = User.objects.all()
    all_profile = Profile.objects.all()
    login_user_rated_list = login_user_rated_list_field.split(',')[0:-1]
    #print(login_user_rated_list)
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
        #print(user.id,user) # FIXME: user and profile is important
        profile = get_object_or_404(Profile,user_id=user.id)
        users_profile_rated = profile.array_rated_project_indexs.split(',')[0:-1]
        users_interests.append(users_profile_rated)

    id_list = [t.id for t in all_profile]

    print(id_list)

    for t in range(len(id_list)):
        if id_list[t] == profile.id:
            login_user_id = t
            print(login_user_id)





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

    #print("make_user_interest_vector:",make_user_interest_vector(users_interests[0]))
    # print("make_user_interest_vector:",make_user_interest_vector(users_interests[1]))
    user_interest_matrix = list(map(make_user_interest_vector, users_interests))
    # inverse
    interest_user_matrix = [[user_interest_vector[j]
                             for user_interest_vector in user_interest_matrix]
                            for j, _ in enumerate(unique_interests)]

    # print(interest_user_matrix)

    interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                              for user_vector_j in interest_user_matrix]
                             for user_vector_i in interest_user_matrix]
    # print(interest_similarities)

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
                    if suggestion not in users_interests[user_id]][:10]

    print("item_based_suggestions",item_based_suggestions(login_user_id))

    int_list = []
    for t in map(int, item_based_suggestions(login_user_id)):
        int_list.append(t)


    qs = Project.objects.filter(id__in=int_list)

    # ---------------------------------------------------------------------------------------------------------------------------------#


    def reverse(num_list):
        reverse_list = []
        for t in num_list:
            if t == 1:
                reverse_list.append(0)
            else:
                reverse_list.append(1)
        return reverse_list

    user_indifferent_matrix = []
    for t in range(len(user_interest_matrix)):
        if t == login_user_id:
            user_indifferent_matrix.append(reverse(user_interest_matrix[t]))
        else:
            user_indifferent_matrix.append(user_interest_matrix[t])

    # for t in user_indifferent_matrix:
    #     print(t)
    # inverse
    indifferent_user_matrix = [[user_interest_vector[j]
                                for user_interest_vector in user_indifferent_matrix]
                               for j, _ in enumerate(unique_interests)]

    # for t in indifferent_user_matrix:
    #     print(t)

    # print([[print("first:",user_vector_i, user_vector_j,math.sqrt(dot(user_vector_i, user_vector_i) * dot(user_vector_j, user_vector_j))) for user_vector_j in interest_user_matrix] for user_vector_i in interest_user_matrix])
    #
    # print("")
    #
    # print([[print("second:",user_vector_i, user_vector_j,math.sqrt(dot(user_vector_i, user_vector_i) * dot(user_vector_j, user_vector_j)))  for user_vector_j in indifferent_user_matrix] for user_vector_i in indifferent_user_matrix])


    # similarity
    indifferent_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                                 for user_vector_j in indifferent_user_matrix]
                                for user_vector_i in indifferent_user_matrix]

    # print(indifferent_similarities[login_user_id])

    def most_similar_indifferent_to(interest_id):
        similarities = indifferent_similarities[interest_id]
        pairs = [(unique_interests[other_interest_id], similarity)
                 for other_interest_id, similarity in enumerate(similarities)
                 if interest_id != other_interest_id and similarity > 0]
        return sorted(pairs,
                      key=lambda pair: pair[1],
                      reverse=True)

    # print('most_similar_indifferent_to:',most_similar_indifferent_to(0))


    def item_based_suggestions_indifferent(user_id, include_current_interests=False):
        suggestions = defaultdict(float)
        user_interest_vector = user_indifferent_matrix[user_id]

        for interest_id, is_interested in enumerate(user_interest_vector):
            if is_interested == 1:
                similar_interests = most_similar_indifferent_to(interest_id)
                for interest, similarity in similar_interests:
                    suggestions[interest] += similarity

        suggestions = sorted(suggestions.items(),
                             key=lambda pair: pair[1],
                             reverse=True)

        if include_current_interests:
            return suggestions
        else:
            return [suggestion
                    for suggestion, weight in suggestions
                    if suggestion not in users_interests[user_id]][:15]

    print("item_based_suggestion_indifferent:", item_based_suggestions_indifferent(login_user_id))

    int_list2 = []
    for t in map(int, item_based_suggestions_indifferent(login_user_id)):
        int_list2.append(t)

    random_list = random.sample(int_list2, random.randint(1, len(int_list2)))

    qs_not = Project.objects.filter(id__in=random_list[:2])
    return render(request, 'homee/project_rcmd.html', {
        'project_list': qs,
        'indifferent': qs_not,
    })


def project_search(request):
    keyword_query = request.GET.get('keyword', '')
    full_text =''
    suggested=""#FIXME: delete init before assigned
    qs = Project.objects.all()

    if keyword_query:
        global suggested
        full_text = SearchQuerySet().models(Project).filter(content=keyword_query)
        suggested = SearchQuerySet().spelling_suggestion(keyword_query)

        print(suggested )
        # auto = SearchQuerySet().autocomplete(title_auto=keyword_query)
        # print([result.title for result in auto])
        # suggestions =
        # data = json.dumps({
        #     'results': suggestions
        # })

    return render(request, 'homee/project_search.html', {
        'keyword_query' : keyword_query,
        'suggested' : suggested,
        'full_text' : full_text,
        'project_list':qs,
    })