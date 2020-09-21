from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Category
from django.views.generic import CreateView
from .forms import *
from .filter import BlogFilter
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage,EmailMultiAlternatives
from django.template.loader import get_template
import os
from .decorators import superuser_only, user_only
from random import randint
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Home
#@user_only
def home(request):
    blog = BlogPost.objects.all().order_by('-date')
    myfilter = BlogFilter(request.GET,queryset=blog)
    blog = myfilter.qs
    p = Paginator(blog,7)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    

    # Category

    category = Category.objects.all()

    #Contact Form

    name = request.POST.get('name')
    forms = ContactForm()
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
            email = request.POST.get('email')
            subject = request.POST.get('name')
            message = request.POST.get('message','')

            template = get_template('contact_template.txt')
            context = {
                'name': subject,
                'email': email,
                'message': message
            }
            content = template.render(context)
            email_msg = EmailMessage(
                'New contact form submission',
                content,
                'Yali Programming' + '',
                ['mathanbba56@gmail.com'],
                headers = { 'Reply-To': email }
            )
            email_msg.send()
        else:
            forms = ContactForm()
    else:
        forms = ContactForm()
    # Subscribe Form
    latest_post = BlogPost.objects.all().order_by('-date')[0:5]
    email = Subscribe.objects.all()
    subscribers = []
    for emails in email:
        subscribers.append(emails)
    subscribe = SubscribeForm()
    if request.method == 'POST':
        subscribe = SubscribeForm(request.POST)
        
        if subscribe.is_valid():
            subscribe.save()
            user_email = subscribe.cleaned_data['subscribers']
            template = get_template('subscribe_template.html')
            context = {
                'latest_post':latest_post
            }
            content = template.render(context)
            email = EmailMessage(
                'Thank you',
                content,
                'Yali Programming' + '',
                [user_email],
            )
            email.content_subtype = 'html'
            
            # email.attach(image.name,image.read(),image.content_type)
            email.send()
            return redirect('home')
        else:
            subscribe = SubscribeForm()
    else:
        subscribe = SubscribeForm()
    context= {
        'blogs':page_obj,
        'category':category,
        'forms':forms,
        'name':name,
        'subscribe':subscribe
    }
    return render(request,'home.html',context)

# Blog post and Comment section 

#@user_only

def post_detail(request,slug):
    blog = get_object_or_404(BlogPost,slug=slug)
    latest_post = BlogPost.objects.all().order_by('-date')[0:5]
    category = Category.objects.all()
    name = request.POST.get('name')
    # Contact Form
    forms = ContactForm()
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
            email = request.POST.get('email')
            subject = request.POST.get('name')
            message = request.POST.get('message','')
            template = get_template('contact_template.txt')
            context = {
                'name': subject,
                'email': email,
                'message': message
            }
            content = template.render(context)
            email_msg = EmailMessage(
                'New contact form submission',
                content,
                'Yali Programming' + '',
                ['mathanbba56@gmail.com'],
                headers = { 'Reply-To': email }
            )
            email_msg.send()
        else:
            forms = ContactForm()
    else:
        forms = ContactForm()
    # Subscribe Form
    email = Subscribe.objects.all()
    subscribers = []
    for emails in email:
        subscribers.append(emails)
    subscribe = SubscribeForm()
    if request.method == 'POST':
        subscribe = SubscribeForm(request.POST)
        if subscribe.is_valid():
            subscribe.save()
            email = subscribe.cleaned_data['subscribers']
            template = get_template('subscribe_template.html')
            context = {
                'latest_post':latest_post
            }
            content = template.render(context)
            email = EmailMessage(
                'Thank you',
                content,
                'Yali Programming' + '',
                [email],
            )
            email.content_subtype = 'html'
            
            # email.attach(image.name,image.read(),image.content_type)
            email.send()
            return redirect('post-detail', slug=slug )
        else:
            subscribe = SubscribeForm()
    else:
        subscribe = SubscribeForm()
    return render(request,'post_detail.html',{'blog':blog,'latest_post':latest_post,'category':category,'forms':forms,'name':name,'subscribe': subscribe})
#@user_only
def add_comment(request,slug):
    post = get_object_or_404(BlogPost,slug=slug)
    form = CommentForm()
    form.instance.user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.user = request.user
        user_name = request.user.username
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            opinion = form.cleaned_data['comment']
            template = get_template('comment_template.html')
            context = {
                'post':post,
                'user_name':user_name,
                'opinion':opinion
            }
            content = template.render(context)
            email = EmailMessage(
                'New comment',
                content,
                'Yali Programming' + '',
                ['mathanbba56@gmail.com'],
            )
            email.content_subtype = 'html'
            
            # email.attach(image.name,image.read(),image.content_type)
            email.send()
            return redirect('post-detail',slug=slug)
        else:
            form = CommentForm()
    
    return render (request,'add_comment.html',{'form':form})

# Signup, Signin, Signout section
#@user_only
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not len(password1) < 8:
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username already exists")
                    return redirect('signup')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.info(request,"email already used try different email")
                        return redirect('signup')
                    else:
                        user = User.objects.create_user(username=username,email=email,password=password1)
                        user.save()
                        user_auth = auth.authenticate(request,username=username,password=password1)
                        if user_auth is not None:
                            auth.login(request,user_auth)
                            return redirect('/')
                        else:
                            messages.info(request,"Somthing went wrong please signup again")
                            return redirect('signup')
            else:
                messages.info(request,"password not match")
                return redirect('signup')
        else:
            messages.info(request,"Your password must contain atleast 8 characters")
            return redirect('signup')
    else:
        return render(request,'users/signup.html')
#@user_only
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('signin')
    else:
        return render(request,'users/signin.html')
#@user_only
def comment_signup(request,slug):
    post = get_object_or_404(BlogPost,slug=slug)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not len(password1) < 8:
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username already exists")
                else:
                    if User.objects.filter(email=email).exists():
                        messages.info(request,"email already used try different email")
                    else:
                        user = User.objects.create_user(username=username,email=email,password=password1)
                        user.save()
                        user_auth = auth.authenticate(request,username=username,password=password1)
                        if user_auth is not None:
                            auth.login(request,user_auth)
                            return redirect('post-detail',slug=slug)
                        else:
                            messages.info(request,"Somthing went wrong please signup again")
            else:
                messages.info(request,"password not match")
        else:
            messages.info(request,"Your password must contain atleast 8 characters")
            return redirect('comment_signup',slug=slug)
        
    return render(request,'users/comment_signup.html',{'blog': post})
#@user_only
def comment_signin(request,slug):
    post = get_object_or_404(BlogPost,slug=slug)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('post-detail', slug=slug)
        else:
            messages.info(request,'Invalid username or password')
            return redirect('comment_signup',slug=slug)
        
    return render(request,'users/comment_signin.html',{'blog': post})
def signout(request):
    auth.logout(request)
    return redirect('/')
#@user_only
def view_category(request,pk):
    categories = BlogPost.objects.filter(category=pk)
    category = Category.objects.all()
    return render(request,'view_category.html',{'categories':categories,'category':category})

#Admin Dashboard
@superuser_only
def dashboard(request):
    blog = BlogPost.objects.all().order_by('-date')
    myfilter = BlogFilter(request.GET,queryset=blog)
    blog = myfilter.qs
    forms = CategoryForm()
    if request.method == 'POST':
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            forms.save()
        else:
            print('form invalid')
    else:
        forms = CategoryForm()
    
    return render(request,'dashboard.html',{'blog':blog,'forms':forms,'myfilter':myfilter})
@superuser_only
def newsletter(request):
    latest_post = BlogPost.objects.all().order_by('-date')[1:5]
    email = Subscribe.objects.all()
    subscribers = []
    for emails in email:
        subscribers.append(emails)
    forms = NewslettertForm()
    if request.method == 'POST':
        forms = NewslettertForm(request.POST,request.FILES)
        
        if forms.is_valid():
            newsletter_subject = forms.cleaned_data['subject']
            newsletter_message = forms.cleaned_data['message']
            # image = forms.cleaned_data['email_pics']


            template = get_template('newsletters_template.html')
            context = {
                'message': newsletter_message,
                'latest_post':latest_post
            }
            content = template.render(context)
            email = EmailMessage(
                newsletter_subject,
                content,
                'Yali Programming' + '',
                subscribers,
            )
            email.content_subtype = 'html'
            
            # email.attach(image.name,image.read(),image.content_type)
            email.send()
            messages.info(request,'Newsletter send successfully')
            return redirect('dashboard')
        else:
            print('form invalid')
    else:
        forms = NewslettertForm()
    return render(request,'newsletters.html',{'forms':forms})
# Create, Update, Delete post section
@superuser_only
def new_post(request):
    latest_post = BlogPost.objects.all().order_by('-date')[0:1]
    email = Subscribe.objects.all()
    subscribers = []
    for emails in email:
        subscribers.append(emails)
    forms = NewPostCreateForm()
    if request.method == 'POST':
        forms = NewPostCreateForm(request.POST,request.FILES)
        if forms.is_valid():
            forms.save()
            post_title = forms.cleaned_data['title']
            template = get_template('newpost_template.html')
            context = {
                'latest_post':latest_post
            }
            content = template.render(context)
            email = EmailMessage(
                post_title,
                content,
                'Yali Programming' + '',
                subscribers,
            )
            email.content_subtype = 'html'
            
            # email.attach(image.name,image.read(),image.content_type)
            email.send()
            return redirect('dashboard')
        else:
            print('form invalid')
    else:
        forms = NewPostCreateForm()
    return render(request,'new-post.html',{'forms':forms})
@superuser_only
def update_post(request,slug):
    blog = BlogPost.objects.get(slug=slug)
    forms = NewPostCreateForm(instance=blog)
    if request.method == 'POST':
        forms = NewPostCreateForm(request.POST,request.FILES, instance=blog)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')
        else:
            print('form invalid')
    return render(request,'new-post.html',{'forms':forms})
@superuser_only
def delete_post(request,slug):
    blog_post = BlogPost.objects.get(slug=slug)
    if request.method == 'POST':
        blog_post.delete()
        return redirect('/')
    return render(request,'delete_post.html',{'item':blog_post})


