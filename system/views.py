from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from crud.models import *
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from users.forms import ClassCode
from django.urls import reverse
from system.forms import UserAnswerForm
from crud.forms import ChoiceForm,AnnouncementForm
from crud.models import Announcement
from posts.models import Post
from posts.forms import PostForm
# from posts.models import Post

@login_required
def index(request):
    student = request.user
    user_classname = ClassName.objects.filter(student=student)  
    class_author = ClassName.objects.filter(author = request.user)
    student_class = ClassName.objects.filter(student = request.user)
    class_code_list = []
    class_list = ClassName.objects.all()
    student_class = []
    for key,item in enumerate(user_classname,start=1):
        student_class.append(item)
        if key ==3:
            break
    for item in class_list:
        class_code_list.append(item.class_code)
    print(class_code_list)
    user_allowed = []
    for user in user_classname:
        user_allowed.append(user.student.all())
  
    user_classname_list = student.classname_set.all()    
    posts = Post.objects.all().order_by('-date_posted') 
    paginator = Paginator(posts,2)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    announcement = Announcement.objects.filter(classname__student = student)
    events = []
    for key,item in enumerate(announcement,start=1):
        events.append(item)
        if key == 2:
            break
    print(events)
    # print(user_classname)
    
    if request.method == 'POST':
        class_code = request.POST.get('code') 
        if class_code in class_code_list:
            student = request.user
            classname = ClassName.objects.get(class_code = class_code)
            classname.student.add(student)
            messages.success(request,f'You are now enrolled in class {classname}')
            return redirect('index')
        else:
            messages.error(request,f'Invalid class code. Please try again')
            return redirect('index')

    context = {
        'announcement':events,
        'class':student_class,
        'class_count':len(student_class),
        'posts':posts,
        'user_allowed':user_allowed,
        'user_classname_list':user_classname_list,
        'class_author':class_author,
        'student_class':student_class,
        'page_obj': page_obj
    }
    return render(request,'system/index.html',context)
   
@login_required
def student_class_list(request):
    student = request.user
    class_list = ClassName.objects.filter(student = request.user)
    
    # print(class_list)
    student_classes = student.classname_set.all()
    
    context={
        'class_list':class_list,
    }
    return render(request,'system/student_class_list.html',context)



def landing_page(request):
 
    return render(request,'system/landing_page.html')
   

@login_required
def student_class_detail(request,class_id):
    classname = ClassName.objects.get(id = class_id)
    quiz_list = Quiz.objects.filter(classname = classname)
    user = request.user
    student_list = classname.student.all()
    is_taken = UserAnswer.objects.filter(user = request.user.id)
    # for item in is_taken:
    #     print(item.user)
    # print(is_taken)
    in_useranswer = []
    for quiz in quiz_list:
        quiz_done = quiz.useranswer_set.filter(user = request.user).filter(quiz = quiz)       
        for item in quiz_done:
            in_useranswer.append(item.quiz)
        print(in_useranswer)
   
    stud_list = []
    for key,student in enumerate(student_list,start=1):
        stud_list.append((key,student))
    context={
        'is_taken':is_taken,
        'class':classname,
        'quiz':quiz_list,
        'student':stud_list,        
        'user':user, 
        'in_useranswer':in_useranswer,       
        
    }
    return render(request,'system/student_class_detail.html',context)

#student take quiz
@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id = quiz_id)
    classname = ClassName.objects.get(quiz = quiz)
    question = Question.objects.filter(quiz = quiz)
    student = request.user
    
    print(UserAnswer.objects.all())
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
                
               
                user_answer = UserAnswer.objects.filter(question = question).filter(answer_id = answer_id).filter(user = request.user)
                if user_answer:
                    user_answer.user = request.user,
                    user_answer.question = question,
                    user_answer.answer_id = answer_id,
                    user_answer.quiz = quiz
                    user_answer.save()
                else:
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
    
    if percent >= 50:
        passed = True
    else:
        passed = False
    print(passed)
    score_list = {
        'score':score,
        'total_score':total_score,
        'percent':percent
    }
    result = QuizResult.objects.filter(quiz = quiz).filter(user=user)
    if result:
        result.quiz = quiz,
        result.user = user,
        result.score = score,
        result.total_score = total_score,
        result.percent = percent,
        result.status = passed
        result.update()
    else:
        quiz_result = QuizResult.objects.create(
                        quiz = quiz,
                        user = user,
                        score = score,
                        total_score = total_score,
                        percent = percent,
                        status = passed
                )
        quiz_result.save()

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

@login_required
def announcement_create(request):
    all_classes = ClassName.objects.filter(author = request.user)
    form = AnnouncementForm()
    # print(form.author)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save(commit = False)
            form.author = request.POST.get('author')
            form.save()
            messages.success(request,f'A new announcement has been created')
            return redirect('announcement-list')
        else:
            messages.error(request,f'An error occured.Please try again. Invalid date and time format.')
            print(form.errors.as_data())


    context={
        'form':form,
        'classes':all_classes,
    }
    return render(request,'system/announcement_create.html',context)

@login_required
def announcement_list(request):
    announcements = Announcement.objects.filter(author = request.user)
    print(announcements)
   

    context={
        'announcements':announcements,
    }
    return render(request,'system/announcement_list.html',context)

@login_required
def announcement_delete(request,announcement_id):
    announcement = Announcement.objects.get(id = announcement_id)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request,f'An announcement has been deleted')
        # return HttpResponseRedirect(reverse('announcement-detail',args=[announcement.id]))
        return redirect('announcement-list')

    context={
        'announcement':announcement,
    }
    return render(request,'system/announcement_delete.html',context)

@login_required
def announcement_detail(request,announcement_id):
    announcement = Announcement.objects.get(id = announcement_id)  

    context={
        'announcement':announcement,
    }
    return render(request,'system/announcement_detail.html',context)

@login_required
def announcement_update(request,announcement_id):
    announcement = Announcement.objects.get(id = announcement_id)  
    form = AnnouncementForm(instance = announcement)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST,instance = announcement)
        if form.is_valid():
            form.save(commit = False)
            form.classname = request.POST.get('classname')
            form.author = request.POST.get('author')
            form.save()
            messages.success(request,f'Announcement has been updated')
            return redirect('announcement-list')
        else:
        
            print(form.errors.as_data())

    context={
        'form':form,
        'announcement':announcement,
    }
    return render(request,'system/announcement_update.html',context)
    
