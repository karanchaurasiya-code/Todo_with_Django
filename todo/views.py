from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from todo.models import TODO
from todo import models
from django.contrib.auth.decorators import login_required

# Signup View


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')

        # Check if username already exists
        if User.objects.filter(username=fnm).exists():
            messages.error(request, "Username already taken.")
            return redirect('/signup')

        # Create user
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        messages.success(request, "Account created successfully.")
        return redirect('/login')

    return render(request, 'sign.html')

# Login View


def login(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')
        print(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/todopage')  # Redirect to homepage or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login')

    return render(request, 'login.html')


@login_required(login_url='/login')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO(title=title, user=request.user)
        obj.save()
        res = models.TODO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage', {'res': res})
    res = models.TODO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})


@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = models.TODO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})


@login_required(login_url='/login')
def delete_todo(request, srno):
    obj = models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')


def signout(request):
    logout(request)
    return redirect('/login')
