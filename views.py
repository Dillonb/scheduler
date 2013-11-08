from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    return render(request,"scheduler/base.html")
def login_view(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = authenticate(username=form.username, password=form.password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponse("Logged in successfully.")
            else:
                pass
                #TODO: Account disabled error page
        else:
            pass
            #TODO: Login invalid error page
    else:
        return render(request,"scheduler/login.html", {"form":form})
def logout_view(request):
    logout(request)
    return render(request, "scheduler/loggedout.html")
