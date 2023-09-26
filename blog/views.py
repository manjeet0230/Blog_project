from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group


# Home view
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts })

# About view
def about(request):
    return render(request, 'blog/about.html')

# Contact view
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard view
from django.shortcuts import get_object_or_404

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()  # Fetch all Post objects
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

# Logout view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup view

def user_signup(request):
    # if not request.user.is_authenticated:
      if request.method == 'POST':
          form = SignUpForm(request.POST)
          if form.is_valid():
           
           messages.success(request, 'Account created successfully !!')
           user = form.save()
           group = Group.objects.get(name='Author')
           user.groups.add(group)

      else:
        form = SignUpForm()
      return render(request, 'blog/signup.html', {'form':form})


# Login view
def user_login(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                 login(request, user)
                messages.success(request, 'Logged in successfully')
                return HttpResponseRedirect('/dashboard/')
        else:
         form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    
#Add new Post view
def add_post(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
         form = PostForm(request.POST)
         if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            post = Post(title=title, body = body)
            post.save()
            return HttpResponseRedirect('/dashboard/')
      else:
         form = PostForm()  
      return render(request, 'blog/addpost.html', {'form':form})
      
   else:
      return HttpResponseRedirect('/login/')
   
 #Update Post view
def update_post(request, id):
   if request.user.is_authenticated:
      if request.method == 'POST':
         pi = Post.objects.get(pk=id)
         form = PostForm(request.POST, instance=pi)
         if form.is_valid():
          form.save()
          return HttpResponseRedirect('/dashboard/')
      else:
         pi = Post.objects.get(pk=id)
         form = PostForm(instance=pi)
      return render(request, 'blog/updatepost.html', {'form': form})
   else:
      return HttpResponseRedirect('/login/')


   
#Delete Post view
def delete_post(request, id):
   if request.user.is_authenticated:
      if request.method == 'POST':
         pi = Post.objects.get(pk=id)
         pi.delete()
         return HttpResponseRedirect('/dashboard/')
   else:
      return HttpResponseRedirect('/login/')
   

from django.shortcuts import render, get_object_or_404


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def allposts(request):
   posts = Post.objects.all()
   return render(request, 'blog/allposts.html', {'posts':posts})
