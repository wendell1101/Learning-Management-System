from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherRegisterForm,StudentRegisterForm, ClassCode
from django.contrib.auth.decorators import login_required
from crud.models import ClassName
from users.models import Profile
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


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
    class_code_list = []
    class_list = ClassName.objects.all()
    for item in class_list:
        class_code_list.append(item.class_code)
    print(class_code_list)
    if request.method == 'POST':
        class_code = ClassCode(request.POST)
        form = StudentRegisterForm(request.POST)
       

        if form.is_valid() and class_code.is_valid():
            class_code = request.POST['class_code']
            
        
            if class_code in class_code_list: 
                form.save()
                user = User.objects.last()
                class_register = ClassName.objects.get(class_code = class_code)
                class_register.student.add(user.id)
                username = form.cleaned_data.get('username')
                messages.success(request,f'An account has been created for {username}! You can now login')
                return redirect('login')
            else:
                messages.error(request,f'Invalid class code. Please try again') 
                return redirect('student-register')
                          
    else:
        form = StudentRegisterForm()    
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
def profile_update(request,username):
    classname = ClassName.objects.filter(student = request.user)
    profile = Profile.objects.get(user = request.user)
    active_user = User.objects.get(username = username)
    # print(active_user)
    # print(profile)
    # print(request.user.profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)

        print(u_form.errors)
        if u_form.is_valid() and p_form.is_valid():
         
            u_form.save()
            p_form.save()
            messages.success(request,f'User information has been updated!')
            return redirect('profile')
        else:
            print(p_form.errors)
            messages.success(request,f'Error in updating your profile!')
    else:
       
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
   
        
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'class':classname
    }
    return render(request,'users/profile_update.html',context)
    
        