from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

#might have extra imports

def register_view(request):
    if request.user.is_authenticated:
        return redirect('quizzes:main-view')
    else:
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)


                return redirect('accounts:login')

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('quizzes:main-view')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in succesfully!")
                return redirect('quizzes:main-view')
            else:
                messages.info(request, 'Username OR password is incorrect!')
                return redirect('accounts:login')
        else:
            context = {}
            return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out succesfully!")
    return redirect('accounts:login')
