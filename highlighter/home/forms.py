from django import forms

def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자이상입력하세요')
    pass

class ProjectForm(forms.Form):
    title = forms.CharField(validators=[min_length_3_validator])
    content = forms.CharField(widhet=forms.Textarea) #위젯설정해줌

