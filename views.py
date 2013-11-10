
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from scheduler.forms import EventForm
from scheduler.models import *

def home_view(request):
    return render(request,"scheduler/base.html")

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

@login_required
def account_view(request):
    schedules = Schedule.objects.filter(creator=request.user)
    return render(request, "scheduler/account.html",{'schedules':schedules})
    
@login_required
def create_event_view(request):
    form = EventForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit = False) # Get an event with the form data (don't commit to db yet)
            #TODO: Make this link to a parent schedule somehow
        else:
            return render(request, "scheduler/createevent.html",{'form':form})
    else:
        return render(request, "scheduler/createevent.html",{'form':form})
