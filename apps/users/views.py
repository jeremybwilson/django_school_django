from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from ..courses.models import Course  # don't need this import because of the related names in Course class
import re, bcrypt

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.

def index(request):
    if 'logged_in' not in request.session:
        return redirect('users:new')

    if 'user_id' not in request.session:
        return redirect('users:new')
    else:
        user_id = int(request.session['user_id'])
        try:
            user_list = User.objects.all()
            specific_user = User.objects.get(id=user_id)
        except:
            return redirect('users:index')
        
    context = {
        'users': user_list,
        'specific_user': specific_user
    }
    return render(request, 'users/index.html', context)

def new(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = False
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    return render(request, 'users/new.html')

def login(request):
    if request.method != 'POST':
        return redirect('users:index')

    valid, result = User.objects.login_user(request.POST)

    if not valid:
        for error in result:
            messages.error(request, error)
        return redirect('users:new')
    else:   # Case : successful login 
        request.session['user_id'] = result
        request.session['logged_in'] = valid
        print "*" * 80
        print "Session user_id:", result
        print "Login status:", valid
        return redirect('users:index')

def create(request):
    if request.method == 'POST':
        valid, result = User.objects.validate_and_create_user(request.POST)
        if not valid:
            for error in result:
                messages.error(request, error)
            return redirect('users:new')
        request.session['user_id'] = result
        request.session['logged_in'] = valid
        print "Session User ID:", result
        print "Login status:", request.session['logged_in']
        return redirect('users:index')
    else:
        return redirect('users:new')

def show(request, user_id):
    if 'user_id' not in request.session:
        return redirect('users:new')

    user_id = int(user_id)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect('users:index')

    context = {
        'user_id': user.id,
        'name': user.name,
        'email': user.email,
        'permission_level': user.permission_level,
        'courses_taught': user.courses_taught.all(),
        'enrolled_courses': user.enrolled_courses.all(),
    }
    return render(request, 'users/show.html', context)

def edit(request, user_id):
    if 'user_id' not in request.session:
        return redirect('users:new')

    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect('users:index')

    context = {
        'user': user
    }
    return render(request, 'users/edit.html', context)

def update(request, user_id):
    if request.method == "POST":
        valid, result = User.objects.validate_and_update_user(user_id, request.POST)
        if not valid:
            for error in result:
                messages.error(request, error)
            return redirect('users:edit', user_id=user_id)
        return redirect('users:index')

def logout(request):
    request.session.clear()
    return redirect('dashboard:index')

def delete(request, user_id):
    if request.method == 'POST':
        User.objects.delete_user_by_id(user_id)
    return redirect('users:index')