from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crud.models import ClassName,Announcement,Quiz,Question,UserAnswer
from django.db import transaction
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from users.forms import ClassCode
from django.urls import reverse
from system.forms import UserAnswerForm
from crud.forms import ChoiceForm
from posts.models import Post
from posts.forms import PostForm
# from posts.models import Post

@login_required
def index(request):
    student = request.user
    user_classname = ClassName.objects.filter(student=student)  
    class_author = ClassName.objects.filter(author = request.user)
    student_class = ClassName.objects.filter(student = request.user)
    user_allowed = []
    for user in user_classname:
        user_allowed.append(user.student.all())
  
    user_classname_list = student.classname_set.all()    
    posts = Post.objects.all().order_by('-date_posted') 
    paginator = Paginator(posts,2)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    announcement = Announcement.objects.filter(classname__student = student)
    
    
    if request.method == 'POST':
        class_code = request.POST.get('code')          
        classname = ClassName.objects.get(class_code = class_code)
        if classname:
            student = request.user
            classname.student.add(student)
            messages.success(request,f'You are now enrolled in class {classname}')
            return redirect('index')
        else:
            messages.error(request,f'Class code in invalid')
            return redirect('index')

    context = {
        'announcement':announcement,
        'class':user_classname,
        'posts':posts,
        'user_allowed':user_allowed,
        'user_classname_list':user_classname_list,
        'class_author':class_author,
        'student_class':student_class,
        'page_obj': page_obj
    }
    return render(request,'system/index.html',context)


def landing_page(request):
 
    return render(request,'system/landing_page.html')

@login_required
def student_class_detail(request,class_id):
    classname = ClassName.objects.get(id = class_id)
    quiz_list = Quiz.objects.filter(classname = classname)
    user = request.user
    student_list = classname.student.all()
    is_taken = UserAnswer.objects.filter(user = request.user.id)
    for item in is_taken:
        print(item.user)
    # print(is_taken)
    
    stud_list = []
    for key,student in enumerate(student_list,start=1):
        stud_list.append((key,student))
    context={
        'is_taken':is_taken,
        'class':classname,
        'quiz':quiz_list,
        'student':stud_list,        
        'user':user, 
    }
    return render(request,'system/student_class_detail.html',context)

#student take quiz
@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    classname = ClassName.objects.get(quiz = quiz)
    question = Question.objects.filter(quiz = quiz)
    student = request.user
  
    if request.method == 'POST':
        with transaction.atomic():
            UserAnswer.objects.filter(user=request.user,
                                    question__quiz=quiz).delete()
            for key, value in request.POST.items():
                if key == 'csrfmiddlewaretoken':
                    continue
                #{'question-1':2}
                question_id = key.split('-')[1]
                question = Question.objects.get(id=question_id)
                answer_id = int(request.POST.get(key))
                if answer_id not in question.choice_set.values_list('id',flat=True):
                    raise SuspiciousOperation('Answer is not valid for this question')
                user_answer = UserAnswer.objects.create(
                    user = request.user,
                    question=question,
                    answer_id = answer_id,
                    quiz = quiz
                )
        return redirect(reverse('show-results',args=(quiz.id,)))  
    
    question_list = []
    for key,question in enumerate(question,start=1):
        question_list.append((key,question))

    context={
        'quiz':quiz,
        'class':classname,
        'question':question_list,
        'student':student,
       
    }
    return render(request,'system/take_quiz.html',context)

def calculate_score(user, quiz):
    questions = Question.objects.filter(quiz=quiz)
    correct_answers = UserAnswer.objects.filter(
        user=user,
        question__quiz=quiz,
        answer__correct=True
    )
 
    percent = round((correct_answers.count() / questions.count()) * 100,2)
    score = correct_answers.count()
    total_score = len(questions)
    if percent >= 70:
        passed = True
    passed = False
    score_list = {
        'score':score,
        'total_score':total_score,
        'percent':percent
    }
    # return f'{score} / {total_score} - {percent} %'
    return score_list
@login_required
def show_results(request, quiz_id):
    # if not request.user.is_authenticated():
    #     raise PermissionDenied
    quiz = Quiz.objects.get(id=quiz_id)
    classname = ClassName.objects.get(quiz = quiz)
    student = request.user
    user_answer = UserAnswer.objects.filter(
        user = request.user,
        question__quiz=quiz
    )
    answer_list = []
    for key,value in enumerate(user_answer,start=1):
        answer_list.append((key,value))
    
    score_list = calculate_score(request.user, quiz)
    score = score_list['score']                
    total_score = score_list['total_score']                
    percent = score_list['percent']                
    context ={
        'quiz':quiz,
        'score':score,
        'total_score':total_score,
        'percent':percent,
        'user_answer':answer_list,
        'student':student,
        'class':classname,
    }
    return render(request,'system/show_results.html',context)



