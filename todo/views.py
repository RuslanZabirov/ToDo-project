from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})
            # Tell user


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required()
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required()
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.author = request.user
        newtodo.save()
        return redirect('currenttodos')


@login_required()
def currenttodos(request):
    todos = Todo.objects.filter(author=request.user, datecompleted__isnull=True)
    completed = Todo.objects.filter(author=request.user, datecompleted__isnull=False)
    return render(request, 'todo/currenttodos.html', {'todos': todos, 'completed': completed})


@login_required()
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, author=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error' : 'obad info'})


@login_required()
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, author=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required()
def uncompletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, author=request.user)
    if request.method == "POST":
        todo.datecompleted = None
        todo.save()
        return redirect('currenttodos')




@login_required()
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, author=request.user)
    if request.method == "POST":

        todo.delete()
        return redirect('currenttodos')



