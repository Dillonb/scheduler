
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from scheduler.forms import EventForm, ScheduleForm
from django.contrib.auth.models import User
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
def create_event_view(request,scheduleid):
    schedule = get_object_or_404(Schedule, id=scheduleid) # The parent schedule
    # If the current user does not own the schedule, do not allow them to create an event on it.
    if schedule.creator != request.user:
        return render(request, "scheduler/errorpage.html", {'message':"PERMISSION DENIED"})
    form = EventForm(data=request.POST) # Load the form
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit = False) # Get an event with the form data (don't commit to db yet)
            event.schedule = schedule # Set the parent schedule
            event.save() # NOW we can save to the database.
            return redirect("/schedule/"+str(event.schedule.id)) 
        else:
            return render(request, "scheduler/createevent.html",{'form':form,'schedule':schedule})
    else:
        return render(request, "scheduler/createevent.html",{'form':form,'schedule':schedule})

@login_required
def create_schedule_view(request):
    form = ScheduleForm(data=request.POST) #Load form
    if request.method == 'POST':
        if form.is_valid():
            schedule = form.save(commit = False) #get schedule with form data, doesnt commit
            schedule.creator = request.user #add creator id
            schedule.save() #commit to db
            return redirect("/schedule/"+str(schedule.id)) # Redirect to the view page for that schedule
        else:
            return render(request, "scheduler/createschedule.html",{'form':form})
    else:
        return render(request, "scheduler/createschedule.html",{'form':form})
    return render(request, "scheduler/createschedule.html")

def schedule_view(request, scheduleid):
    schedule = get_object_or_404(Schedule, id=scheduleid)
    canView = False

    # Schedule is public, allow anyone to view it
    if schedule.visibility == schedule.VISIBILITY_PUBLIC:
        canView = True
    # TODO: Fill this in after implementing friends.
    elif schedule.visibility == schedule.VISIBILITY_FRIENDSONLY:
        pass 
    # If the schedule is private, only allow the owner to view it.
    elif schedule.visibility == schedule.VISIBILITY_PRIVATE:
        if schedule.creator == request.user: # If the current user is the owner
            canView = True
        else:
            canView = False
    if canView:
        return render(request, "scheduler/schedule.html",{'schedule':schedule})
    else:
        return render(request,"scheduler/errorpage.html",{'message':"PERMISSION DENIED"})

@login_required
def friends_view(request):
    friends = Friend.objects.all_friends_for_user(request.user)
    pending_requests = []
    sent_requests = []
    accepted_friends = []
    for friend in friends:
        if friend.status == Friend.STATUS_SENT:
            if friend.creator == request.user:
                sent_requests.append(friend)
            else:
                pending_requests.append(friend)
        elif friend.status == Friend.STATUS_ACCEPTED or friend.status == Friend.STATUS_MATCHED:
            accepted_friends.append(friend)

    return render(request,"scheduler/friends.html", {'friends': accepted_friends,'sent_requests':sent_requests, 'pending_requests':pending_requests})
