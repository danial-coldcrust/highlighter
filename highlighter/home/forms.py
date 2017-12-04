from django import forms
from .models import Project


class ProjectForm(forms.Form):
    # class Meta:
    #     model = Project
    #
    #     fields = '__all__'
    #


    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)



    # def save(self,commit):
    #     project = Project()
    #
    #     # project.user_id = '1'
    #     # 딕셔너리
    #     # project.title = form.cleaned_data['title']
    #     # project.content= form.cleaned_data['content']
    #     project = Project(**self.cleaned_data)  # 이방식쓸려면modelform써야됨
    #     if commit:
    #         project.save()
    #         return project
