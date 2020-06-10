from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class ClassName(models.Model):
    title = models.CharField(verbose_name= 'Class', max_length=100)
    subject= models.CharField(verbose_name= 'Subject', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='author')
    class_code = models.CharField(max_length=20) 
    student = models.ManyToManyField(User)
    
    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.title


class Quiz(models.Model):
    text = models.CharField(verbose_name='Quiz Title',max_length=100)
    classname = models.ForeignKey(ClassName, on_delete = models.CASCADE)

    def __str__(self):
        return self.text
class Question(models.Model):
    text = models.CharField(verbose_name='question',max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)

    def __str__(self):
        return self.text

class Choice(models.Model):
    text = models.CharField(verbose_name='Choice',max_length=100)
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    correct = models.BooleanField()
    
    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    answer = models.ForeignKey(Choice, on_delete = models.CASCADE,verbose_name='',related_name='answer', default='')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE, default = '')
 

    class Meta:
        unique_together = ['question','answer']
        
    def __str__(self):
        return f'{self.question.text}-{self.answer.text}'



class Announcement(models.Model):
    classname = models.ForeignKey(ClassName,on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    due = models.DateTimeField()

    def __str__(self):
        return self.text

  



    



