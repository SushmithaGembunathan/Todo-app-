from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from .forms import RegisterForm
from .forms import TaskForm
from django.http import HttpResponseRedirect

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.method == 'POST':
        # Create a new task
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    if request.user.is_superuser:
        users = User.objects.all()
        tasks = Task.objects.select_related('user').all()
        return render(request, 'dashboard.html', {
            'is_admin': True,
            'users': users,
            'tasks': tasks,
        })

    else:
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {
            'is_admin': False,
            'form': form,
            'tasks': tasks,
        })

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.user == task.user or request.user.is_superuser:
        task.delete()
    return redirect('dashboard')

@login_required
def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.user == task.user or request.user.is_superuser:
        task.is_completed = not task.is_completed
        task.save()
    return redirect('dashboard')