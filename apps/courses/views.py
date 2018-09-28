from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course
from ..users.models import User

# Create your views here.
def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False

    if 'user_id' not in request.session:
        return redirect('users:new')
    else:
        user_id = int(request.session['user_id'])
        try:
            course_list = Course.objects.all()
            # user_list = User.objects.all()
            specific_user = User.objects.get(id=user_id)
        except:
            return redirect('users:index')
        
    context = {
        # 'users': user_list,
        'courses': course_list,
        'specific_user': specific_user
    }

    return render(request, 'courses/index.html', context)

def new(request):
    context = {
        'teachers': User.objects.filter(permission_level="TEACHER")
    }
    return render(request, 'courses/new.html', context)

def create(request):
    valid, result = Course.objects.validate_and_create_course(request.POST)
    if not valid:
        for errors in result:
            messages.error(request, errors)
        return redirect('courses:new')

    return redirect('courses:index')

