from crud.models import ClassName,Quiz,Question,Choice,UserAnswer
from django import forms
class UserAnswerForm(forms.ModelForm):
    
    class Meta:
        model = UserAnswer
        fields = ['answer']
    