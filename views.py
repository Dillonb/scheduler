from django.contrib.auth import logout
from django.shortcuts import render

def home_view(request):
    return render(request,"scheduler/base.html")
def login_view(request):
    pass
def logout_view(request):
    logout(request)
    return render(request, "scheduler/loggedout.html")
