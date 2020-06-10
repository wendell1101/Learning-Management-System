from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from posts.forms import PostForm
from crud.models import *
from django.contrib import messages

@login_required
def post_create(request):
    is_class_author = ClassName.objects.filter(author = request.user)
    is_class_student = ClassName.objects.filter(student = request.user)
    user_list = User.objects.all()
    form = PostForm()
    if request.method =='POST':      
        form = PostForm(request.POST, request.FILES)   
        print(request.POST.get('author'))    
       
        if form.is_valid():
            form.save(commit=False)
            form.classname = request.POST.get('classname')
            form.image = request.FILES.get('image') 
            form.attachment = request.FILES.get('attachment')
            form.author = request.POST.get('author')
            form.save()
            messages.success(request,f'A new post has been created')
            return redirect('index')
        else:
            form = PostForm()      
    context={        
        'form':form,
        'is_class_author':is_class_author,
        'is_class_student':is_class_student,
        'user':user_list       
    }
    return render(request,'posts/post_create.html',context)

@login_required
def post_update(request,post_id):
    is_class_author = ClassName.objects.filter(author = request.user)
    is_class_student = ClassName.objects.filter(student = request.user)
    user_list = User.objects.all()
    post = Post.objects.get(id = post_id)
    form = PostForm(instance = post)   
    if request.method =='POST':      
        form = PostForm(request.POST, request.FILES,instance=post)   
        print(request.POST.get('author'))    
       
        if form.is_valid():
            form.save(commit=False)
            form.classname = request.POST.get('classname')
            form.image = request.FILES.get('image') 
            form.attachment = request.FILES.get('attachment')
            form.author = request.POST.get('author')
            form.save()
            messages.success(request,f'A post has been updated')
            return redirect('index')
        else:
            form = PostForm(instance = post)
     
    context={        
        'form':form,
        'is_class_author':is_class_author,
        'is_class_student':is_class_student,
        'user':user_list,
        'post':post      
    }
    return render(request,'posts/post_update.html',context)

@login_required
def post_delete(request,post_id):    
    post = Post.objects.get(id = post_id)
      
    if request.method =='POST':      
       post.delete()
       messages.success(request,f'A post has been deleted')
       return redirect('index')
     
    context={        
       'post':post,  
    }
    return render(request,'posts/post_delete.html',context)

    