import datetime
from haystack import indexes
from .models import Project

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    title = indexes.CharField(model_attr='title')
    pub_date = indexes.DateTimeField(model_attr='created_at')
    suggestions = indexes.FacetCharField()
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def prepare(self, obj):
        prepared_data = super(ProjectIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Project






def user_based_suggestions(user_id, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)

    for similar_user, similarity in most_similar_users_with_me(user_id):
        for interest in users_interests[similar_user]:
            suggestions[interest] += similarity
            print(suggestions)

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda pair: pair[1],
                         reverse=True)

    # and (maybe) exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        print([(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]][0:12])
        # return [(suggestion, weight)
        return [suggestion
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]][0:12]























