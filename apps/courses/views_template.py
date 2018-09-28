from django.shortcuts import render

# Create your views here.
def index(request):
    if 'user_id' not in req.session:
        return redirect('users:new')

    context = {
        'users': User.objects.all()
    }
    return render(request, 'users/index.html', context)

def new(request):
    return render(request, 'users/new.html')

def create(request):
    pass

def edit(request):
    pass

def show(request):
    pass

def update(request):
    pass

def login(request):
    pass
def logout(request):
    pass

def delete(request, user_id):
    if req.method == 'POST':
        User.objects.delete_user_by_id(user_id)
        return redirect('courses:index')

def logout(request):
    request.session.clear()
    return redirect('courses:index')