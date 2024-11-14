from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import Blog_Post,Tag,Comments
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist


def register(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password')
        password2=request.POST.get('password_confirm')
        
        if password1==password2:
            messages.error(request,'Password does not match!')
        if User.objects.filter(username=username).exists():
            messages.error('username already exists ')
            return redirect('signup')
        
        else:
            user =User.objects.create_user(username=username,email=email,password=password1)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            
            login(request, user)  
            return redirect('home')
        
    messages.success(request, "Account created successfully!")  
    return render(request,'blog/register.html')
            
def user_login(request):
    if  request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request,'blog\login.html')

def user_logout(requst):
    logout(requst)
    return redirect('home')

@login_required(login_url='login')
def create_blogs(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags=request.POST.getlist('tags')
        author = request.user
        is_approved = request.user.is_staff 
        blog = Blog_Post.objects.create(
            title=title, 
            content=content, 
            author=author, 
                                        created_at=timezone.now(),
                                                is_approved=is_approved
)
        
        if tags:
            for tag_id in tags:
                try:
                    tag = Tag.objects.get(id=tag_id) 
                    blog.tags.add(tag) 
                except ObjectDoesNotExist:
                    messages.error(request, f"Tag with ID {tag_id} does not exist.")
                    return redirect('create_blog')
                
        blog.save() 
        messages.success(request, "Your blog has been created successfully!")

        return redirect('blog_details', id=blog.id)
    
    tags = Tag.objects.all()
    return render(request, 'blog/create_blog.html', {'tags': tags})

@login_required(login_url='login')
def blog_details(request,id):
    blog=get_object_or_404(Blog_Post,id=id)
    comments = Comments.objects.filter(blog=blog)
    if request.method=='POST':
        content = request.POST.get('content')
        if content:
            comment = Comments(blog=blog, author=request.user, content=content)
            comment.save()
            return redirect('blog_details', id=blog.id)
    context = {'blogs': blog,'comments': comments}
    
    return render(request, 'blog/blog_details.html', context)



def edit_blog(request, id):
    blog = get_object_or_404(Blog_Post, id=id)
    
    if request.user != blog.author:
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect('blog_details', id=blog.id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        blog.title = title
        blog.content = content
        blog.updated_at = timezone.now()  
        blog.save()

        messages.success(request, "Your blog has been updated successfully!")
        return redirect('blog_details', id=blog.id)
    
    context = {
        'blog': blog
    }
    return render(request, 'blog/edit_blog.html', context)
    

@login_required(login_url='login')
def delete_blog(request, id):
    blog = get_object_or_404(Blog_Post, id=id)
    
    if request.user == blog.author:
        blog.delete()
        messages.success(request, "Blog post has been deleted successfully!")
        return redirect('home')  
    else:
        messages.error(request, "You are not authorized to delete this blog.")
        return redirect('blog_details', id=id)     
    
    
def home(request):
    search=request.GET.get('search','')
    
    if search:
        blogs = Blog_Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search) | Q(tags__name__icontains=search)).distinct().order_by('-created_at') 
        
    else:
        blogs=Blog_Post.objects.all().order_by('-created_at') 
    latest_posts = Blog_Post.objects.all().order_by('-created_at') 
    return render(request, 'blog/home.html', {'latest_posts': latest_posts,'blogs':blogs})

def create_tag(request):
    if request.method=='POST':
        tag_name=request.POST.get('name')
        if tag_name:
            if Tag.objects.filter(name=tag_name).exists():
                Tag.objects.create(name=tag_name)
                messages.success(request, "Tag created successfully!")
                return redirect('create_blog')
                
            else:
                messages.error(request, "Tag with this name already exists.")                
        else:
            messages.error(request, "Tag name cannot be empty.")
    
    return render(request, 'blog/create_tag.html')
        
def edit_cmt(request,id) :   
      
    comment=get_object_or_404(Comments,id=id)
    if request.user != comment.author:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('blog_details', id=comment.id)
    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        messages.success(request, "Your comment has been updated.")
        return redirect('blog_details', id=comment.blog.id)
    context = {'comment': comment}
    return render(request, 'blog/edit_cmt.html', context)
    
def delete_cmt(request,id):
    comment = get_object_or_404(Comments, id=id)
    
    if request.user == comment.author:
        comment.delete()
        messages.success(request, "Your Comment  has been deleted successfully!")
        return redirect('blog_details', id=comment.blog.id)
    else:
        messages.error(request, "You are not authorized to delete this blog.")
        return redirect('blog_details', id=id)
    
        