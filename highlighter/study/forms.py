# study/forms.py

from django import forms

class ProjectForm(forms.Form):
    # user =forms.
    #     models.ForeignKey(settings.AUTH_USER_MODEL)
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)