from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherRegisterForm,StudentRegisterForm, ClassCode
from django.contrib.auth.decorators import login_required
from crud.models import ClassName
from django.contrib.auth.models import User
# from users.forms import UserForm

def teacher_register(request):
    form = TeacherRegisterForm()
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'An account has been created for {username}! You can now login')
            return redirect('login')
    else:
        form = TeacherRegisterForm()    
    context = {
        'form':form
    }
    return render(request,'users/register_teacher.html',context)

def student_register(request):
    class_code = ClassCode()
    form = StudentRegisterForm()

    if request.method == 'POST':
        class_code = ClassCode(request.POST)
        form = StudentRegisterForm(request.POST)
        if form.is_valid() and class_code.is_valid():
            class_code = request.POST['class_code']
            print(class_code)           
            is_true = ClassName.objects.get(class_code = class_code)
            if is_true: 
                firstname = request.POST['first_name']
                lastname = request.POST['last_name']
                form.save(commit=False)  
                form.first_name = firstname
                form.last_name = lastname
                form.save()
                user = User.objects.last()
                is_true.student.add(user.id)
                username = form.cleaned_data.get('username')
                messages.success(request,f'An account has been created for {username}! You can now login')
                return redirect('login')
            else:
                return redirect('student-register')
                messages.error(request,f'Invalid class code. Please try again')            
    else:
        form = TeacherRegisterForm()    
        class_code = ClassCode()
    context = {
        'form':form,
        'class_code':class_code,   
    }
    return render(request,'users/register_student.html',context)

@login_required
def profile(request):
    classname = ClassName.objects.filter(student = request.user)
    context={
        'class':classname
    }
    return render(request,'users/profile.html',context)

@login_required
def profile_update(request,user_id):
    classname = ClassName.objects.filter(student = request.user)
    user = request.user   
    form = StudentRegisterForm(instance = user)
    # print(form)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST,instance = user)
        if form.is_valid():
            form.save()
            messages.success(request,f'User profile has been updated')
            return redirect('index')
        else:
            form = StudentRegisterForm(instance = user)
        
    context = {
        'form':form,
        'class':classname
    }
    return render(request,'users/profile_update.html',context)
    
        