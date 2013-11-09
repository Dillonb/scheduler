from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def home_view(request):
    return render(request,"scheduler/base.html")

def login_view(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password) 
        if user:
            if user.is_active:
                login(request,user)
            else:
                return HttpResponse("User not active.")
        else:
            return HttpResponse("User invalid.")
        return HttpResponse("Logged in successfully.")
    else:
        return render(request,"scheduler/login.html", {"form":form})

def logout_view(request):
    logout(request)
    return render(request, "scheduler/loggedout.html")

def is_loggedin_view(request):
    if request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "scheduler/register.html", {
        'form': form,
    })
