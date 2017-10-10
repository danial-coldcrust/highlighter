from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        #fields = ['user','title','content']
        fields = '__all__'

    # title = forms.CharField(validators=[min_length_3_validator])
    # content = forms.CharField(widget=forms.Textarea) #위젯설정해줌
    #



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
