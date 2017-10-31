import datetime
from haystack import indexes
from .models import Project

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    title = indexes.CharField(model_attr='title')

    pub_date = indexes.DateTimeField(model_attr='created_at')
    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(ProjectIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Project