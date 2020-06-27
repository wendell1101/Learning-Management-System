from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserAnswer,ClassName,Question,Quiz,Choice,QuizResult
from .models import UserAnswer as AnswerList
from .forms import ClassForm,QuizForm,QuestionForm,UserAnswer , AnnouncementForm, ChoiceForm
from system.views import calculate_score

@login_required(login_url='index')
def administration(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            classname = ClassName.objects.filter(author = request.user)
            context = {
                'class':classname,
            }
        else:
            return HttpResponseRedirect(reverse('index'))
        return render(request,'crud/administration.html',context)



@login_required
def class_create(request):
    form = ClassForm()    
   
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid(): 
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            classname = form.save(commit=False)
            classname.class_code = get_random_string(length=10)
            classname.save()
            form.save()
            messages.success(request,f'A class has been created successfully')
            return redirect('administration')
    else:
        form = ClassForm()
    context = {
        'form':form,
    }
    return render(request,'crud/class_create.html',context)
    

@login_required
def class_detail(request,class_id):
    form = ClassName.objects.get(id = class_id)
    student = form.student.all()
    student_list = []
    for key,value in enumerate(student,start=1):
        student_list.append((key,value)) 
    context = {
        'class':form,
        'student':student_list
    }
    return render(request,'crud/class_detail.html',context)

@login_required   
def class_delete(request,class_id):
    form = ClassName.objects.get(id = class_id)
    if request.method == 'POST':
        form.delete()
        messages.success(request,f'A class has been deleted successfuly')
        return redirect('administration')
    context = {
        'class':form
    }
    return render(request,'crud/class_confirm_delete.html',context)


@login_required
def class_update(request,class_id):
    course = ClassName.objects.get(id = class_id)
    form = ClassForm()
    if request.method == 'POST':
        form = ClassForm(request.POST,instance = course)
        if form.is_valid():
            form.save()
            messages.success(request,f'A class has been updated successfully')
            return redirect('administration')
    else:
        form = ClassForm(instance = course)
    context = {
        'form':form
    }
    return render(request,'crud/class_update.html',context)

#student
@login_required
def student_delete(request,student_id):
    classname = ClassName.objects.get(student = student_id)
   
    student = classname.student

    if request.method == 'POST':
        student.delete()
        messages.success(request,f'Student has been deleted')
        return HttpResponseRedirect(reverse('class-detail',args=[classname.id]))
    else:
        student = classname.student
    print(student)
    context = {
        'student':student,
        'class':classname
    }
    return render(request,'crud/student_delete.html',context)


# Quiz

@login_required
def create_quiz(request, class_id):
    classname = ClassName.objects.get(id = class_id)
    quiz_list = Quiz.objects.filter(classname = classname)   
    quiz = QuizForm()
    if request.method == 'POST':
        classname = ClassName.objects.get(id = class_id)
        quiz = QuizForm(request.POST)
        if quiz.is_valid():  
            quiz = quiz.save(commit=False)
            quiz.classname = classname  
            quiz.save()
           
            return HttpResponseRedirect(reverse('quiz-list', args=[classname.id]))
        else:
            messages.error(request,f'Error occured, quiz has not been created')
            quiz = QuizForm()
      
    
    context={
        'quiz':quiz,
        'quiz_list':quiz_list,
        'class_id':classname.id
        
    }
    return render(request,'crud/create_quiz.html',context)

@login_required
def create_question(request,quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    class_id = quiz.classname.id
    question_list = Question.objects.filter(quiz = quiz) 
  
    question = QuestionForm()
    if request.method == 'POST':
        question = QuestionForm(request.POST)
        if question.is_valid():
            
            question = question.save(commit = False)
            question.quiz = quiz
            question.save()
       
            return HttpResponseRedirect(reverse('quiz-detail', args=[quiz.id]))
        else:
            question = QuestionForm()
    
    context={
        'quiz':quiz,
        'question':question,
        'question_list':question_list,
        'class_id':class_id
       
    }
    return render(request,'crud/create_question.html',context)

@login_required
def create_choice(request,question_id):
    question = Question.objects.get(id = question_id)
    quiz = Quiz.objects.get(question = question)
    form = ChoiceForm()
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.question = question
            form.save()
            return HttpResponseRedirect(reverse('quiz-detail',args=[quiz.id]))
        else:
            form = ChoiceForm()

    context = {
        'question':question,
        'form':form,
        'quiz':quiz,
    }
    return render(request,'crud/create_choice.html',context)


#Quiz LIst

@login_required
def quiz_list(request,class_id):
    classname = ClassName.objects.get(id = class_id)
    quiz_list = Quiz.objects.filter(classname = classname)
 
   
    context={
        'quiz_list':quiz_list,
        'class_id':classname.id
    }
    return render(request,'crud/quiz_list.html',context)

#quiz detail

@login_required
def quiz_results(request,quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    useranswer = quiz.useranswer_set.filter(quiz = quiz)
    questions = Question.objects.filter(quiz=quiz)
    result = QuizResult.objects.filter(quiz = quiz)
    useranswer = []
    for item in enumerate(result,start=1):
        useranswer.append(item)
    print(useranswer)
  
    
    
    context={
        'quiz':quiz,
        'result':useranswer,
        
    }
 
    return render(request,'crud/quiz_results.html',context)

@login_required
def quiz_detail(request,quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    classname = ClassName.objects.get(quiz=quiz)
    question = Question.objects.filter(quiz = quiz)
    question_list=[]
    for key,value in enumerate(question,start=1):
        question_list.append((key,value))
    
    context={
        'quiz':quiz,
        'question_list':question_list,
        'class_id':classname.id,  
    }
    return render(request,'crud/quiz_detail.html',context)

#update quiz
@login_required
def quiz_update(request,quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    classname = ClassName.objects.get(quiz=quiz)
    form = QuizForm(instance = quiz)
    if request.method == 'POST':
        form = QuizForm(request.POST,instance = quiz)
        if form.is_valid():
            form.save(commit = False)
            form.classname = classname
            form.save()
            messages.success(request,f'Quiz name has been updated')
            return HttpResponseRedirect(reverse('quiz-list',args=[classname.id]))
    else:
        form = QuizForm(instance = quiz)

    context={
        'form':form,
        'quiz':quiz,
        'class_id':classname.id,
    }
    return render(request,'crud/quiz_update.html',context)

#delete quiz
@login_required
def quiz_delete(request,quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    question = Question.objects.filter(quiz=quiz)
    classname = ClassName.objects.get(quiz=quiz)
    form = QuizForm(instance = quiz)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request,f'{quiz} has been deleted')
        return HttpResponseRedirect(reverse('quiz-list',args=[classname.id]))
    else:
        form = QuizForm(instance = quiz)
    print(question)
    context={
        'form':form,
        'quiz':quiz,
        'class_id':classname.id,
        'question':question
    }
    return render(request,'crud/quiz_delete.html',context)

#update question
@login_required
def question_update(request,question_id):
    question = Question.objects.get(id = question_id)
    choice = Choice.objects.filter(question = question)
    quiz = Quiz.objects.get(question=question)
    form_question = QuestionForm(instance=question)
    
    if request.method == 'POST':
        form_question = QuestionForm(request.POST, instance=question)
        if form_question.is_valid():
            form_question.save(commit=False)
            form_question.quiz = quiz
            form_question.save()
            messages.success(request,f'A question has been updated')
            return HttpResponseRedirect(reverse('quiz-detail',args=[quiz.id]))
    else:
        form = QuestionForm(instance=question)
    context = {
        'question':question,
        'quiz':quiz,
        'quiz_id' : quiz.id,
        'form_question':form_question,
    }
    return render(request,'crud/question_update.html',context)

#delete question
@login_required
def question_delete(request,question_id):
    question = Question.objects.get(id = question_id)
    quiz = Quiz.objects.get(question = question)
    if request.method == 'POST':
        question.delete()
        messages.success(request,f'{question} has been deleted')
        return HttpResponseRedirect(reverse('quiz-detail',args=[quiz.id]))
    else:
        form = QuizForm(instance = quiz)
    context={
        'question':question,
        'form':form,
        'quiz_id':quiz.id
    }
    return render(request,'crud/question_delete.html',context)


#choice detail
@login_required
def choice_detail(request,choice_id):
    choice = Choice.objects.get(id = choice_id)
    quiz = Quiz.objects.get(question__choice = choice)
    question = Question.objects.get(choice = choice)
    
    context = {
        'choice':choice,
        'question':question,
        'quiz':quiz
    }
    return render(request,'crud/choice_detail.html',context)

#choice delete
@login_required
def choice_delete(request,choice_id):
    choice = Choice.objects.get(id = choice_id)
    quiz = Quiz.objects.get(question__choice = choice)
    question = Question.objects.get(choice = choice)
    if request.method =='POST':
        choice.delete()
        messages.success(request,f'A choice has been deleted')
        return HttpResponseRedirect(reverse('quiz-detail',args=[quiz.id]))
    context = {
        'choice':choice,
        'question':question,
        'quiz':quiz
    }
    return render(request,'crud/choice_delete.html',context)


#update choice
@login_required
def choice_update(request,choice_id):
    choice = Choice.objects.get(id = choice_id)
    quiz = Quiz.objects.get(question__choice = choice)
    question = Question.objects.get(choice = choice)
    form = ChoiceForm(instance = choice)  
    if request.method == 'POST':
        form = ChoiceForm(request.POST,instance = choice)
        if form.is_valid():
            form.save()
            messages.success(request,f'A choice has been updated')
            return HttpResponseRedirect(reverse('quiz-detail',args=[quiz.id]))
        else:
            form = ChoiceForm(instance = choice)
    context={
        'form':form,
        'quiz':quiz,
        'choice':choice,
        'question':question,
    }
    return render(request,'crud/choice_update.html',context)
#announcement

@login_required
def announcement_create(request,class_id):
    classname = ClassName.objects.get(id = class_id)
    form = AnnouncementForm()
    if request.method == 'POST':
        print(classname)
        form = AnnouncementForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request,f'New announcement has been created')
            return HttpResponseRedirect(reverse('class-detail',args=[classname.id]))
    else:
        form = AnnouncementForm()
    
    context = {
        'form':form,
        'class':classname
    }
    return render(request,'crud/announcement_create.html',context)