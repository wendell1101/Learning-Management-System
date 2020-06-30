from django import forms
from .models import ClassName,Quiz, Question, UserAnswer, Announcement,Choice

class ClassForm(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = ['title','subject']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['text']

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['text']        

class ChoiceForm(forms.ModelForm):
    text = forms.CharField(
                max_length=200, required=True,
                widget=forms.TextInput(
                    attrs={'placeholder':'Enter your choice'}
                )
    )
    class Meta:
        model = Choice
        fields = ['text','correct']        
   

class UserAnswer(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['answer']     

#announcement
class AnnouncementForm(forms.ModelForm):

    text = forms.CharField(
       
        widget=forms.Textarea(attrs={'placeholder':'Input details here'})
    
    )
    due = forms.DateTimeField(
        input_formats=['%Y-%d-%m %H:%M:%S'], 
    
        widget = forms.TextInput(attrs={'placeholder': 'Enter Date'})
    
    )
    class Meta:
        model = Announcement 
        fields = ['classname','title','text','due','author']
    
    
        


   