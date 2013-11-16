import datetime
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from scheduler.forms import EventForm, ScheduleForm, AddFriendForm
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
            if not(Schedule.objects.filter(name=schedule.name).exists()): #if a schedule with the same name doesn't already exist
                schedule.save() #commit to db
                return redirect("/schedule/"+str(schedule.id)) # Redirect to the view page for that schedule
            else: #if a schedule with the same name exists:
                return render(request,"scheduler/errorpage.html",{'message':"A schedule with the same name alredy exists."})
        else:
            return render(request, "scheduler/createschedule.html",{'form':form})
    else:
        return render(request, "scheduler/createschedule.html",{'form':form})
    return render(request, "scheduler/createschedule.html")

def schedule_view(request, scheduleid, view=0, week=datetime.datetime.now()):
    schedule = get_object_or_404(Schedule, id=scheduleid)
    canView = False
    # Schedule is public, allow anyone to view it
    if schedule.visibility == schedule.VISIBILITY_PUBLIC:
        canView = True
    elif schedule.visibility == schedule.VISIBILITY_FRIENDSONLY:
        #set canView true if the request user and schedule creator are friends:
        if schedule.creator == request.user:
            canView = True
        else:
            canView = Friend.objects.are_friends(request.user, schedule.creator)
        #if the request user is the creator set canView true:

    # If the schedule is private, only allow the owner to view it.
    elif schedule.visibility == schedule.VISIBILITY_PRIVATE:
        if schedule.creator == request.user: # If the current user is the owner
            canView = True
        else:
            canView = False
    if canView:

        weekday = week.weekday()
        # If sunday, monday is the day after (not 6 days before)
        if weekday == 6:
            monday = week + datetime.timedelta(days=1)
        else:
            monday = week - datetime.timedelta(days=week.weekday())

        week = [monday - datetime.timedelta(days=1), # Sunday
                monday,                              # Monday
                monday + datetime.timedelta(days=1), # Tuesday
                monday + datetime.timedelta(days=2), # Wednesday
                monday + datetime.timedelta(days=3), # Thursday
                monday + datetime.timedelta(days=4), # Friday
                monday + datetime.timedelta(days=5), # Saturday
                ]
        events = []

        for day in week:
            events.append((day, Event.objects.on_date(day, schedule)))

        return render(request, "scheduler/schedule.html",{'schedule':schedule, 'events':events})
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

@login_required
def friends_accept_view(request, friendid):
    friend = get_object_or_404(Friend, id=friendid)
    if friend.status != Friend.STATUS_SENT:
        raise Http404
    if friend.friend == request.user:
        friend.status = Friend.STATUS_ACCEPTED
        friend.save()
    else:
        return render(request,"scheduler/errorpage.html",{'message':"PERMISSION DENIED"})
    return redirect("/friends")

@login_required
def friends_decline_view(request, friendid):
    friend = get_object_or_404(Friend, id=friendid)
    if friend.status != Friend.STATUS_SENT:
        raise Http404
    if friend.friend == request.user:
        friend.delete()
    else:
        return render(request,"scheduler/errorpage.html",{'message':"PERMISSION DENIED"})
    return redirect("/friends")


@login_required
def friends_add_view(request):
    if request.method == "POST":
        form = AddFriendForm(request.POST)
        if form.is_valid():
            # Get the friend relationship if it already exists
            friend = Friend.objects.get_friend_object(request.user, form.get_newfriend_user())
            # If the relationship did not previously exist, create it as a request with the current user as the creator.
            if friend == None:
                if form.get_newfriend_user() == request.user:
                    return render(request,"scheduler/errorpage.html",{'message':"You can't send a friend request to yourself."})
                friend = Friend(creator=request.user, friend=form.get_newfriend_user())
                friend.save()
                return redirect("/friends/")
            else: # If the relationship already exists...
                # See if it was already accepted/matched and tell them they are already friends
                if friend.status == Friend.STATUS_ACCEPTED or friend.status == Friend.STATUS_MATCHED:
                    return render(request, "scheduler/errorpage.html",{'message':"You are already friends with this user"})
                # It was a sent friend request
                elif friend.status == Friend.STATUS_SENT:
                    # If it was sent by the current user, tell them they can't send another.
                    if friend.creator == request.user:
                        return render(request,"scheduler/errorpage.html",{'message':"You already sent a friend request to this user."})
                    # Otherwise, match the two up and update the original friend request.
                    else:
                        # The other user sent this friend request. Update it to STATUS_MATCHED.
                        friend.status = Friend.STATUS_MATCHED
                        friend.save()
                        return redirect("/friends/")
    else:
        form = AddFriendForm()

    return render(request, "scheduler/addfriend.html", {"form":form})


def account_page_view(request, userid):
    #Get all the schedules from the user indicated:
    user = get_object_or_404(User, id=userid)
    schedules = Schedule.objects.filter(creator=user, visibility=Schedule.VISIBILITY_PUBLIC)
    #get the friend object of that user
    if request.user.is_authenticated():
        #if the request user is the owner of the profile then they can view friends only schedules and private schedules
        if request.user == user:
            #gets private schedules:
            private = Schedule.objects.filter(creator=userid, visibility=Schedule.VISIBILITY_PRIVATE)
            #gets friends only schedules:
            friendsOnly = Schedule.objects.filter(creator=userid, visibility=Schedule.VISIBILITY_FRIENDSONLY)
            #returns public, friends only and private schedules:
            return render(request, "scheduler/user.html",{'schedules':schedules, 'friendsOnly':friendsOnly, 'private':private})
            #allows friend only schedule viewing:
        else:
            #if the request user isnt the owner of the profile see if they are friends.
            if Friend.objects.are_friends(request.user, user):
                #get friends only schedules:
                friendsOnly = Schedule.objects.filter(creator=userid, visibility=Schedule.VISIBILITY_FRIENDSONLY)
                #returns public and friendsonly schedules:
                return render(request, "scheduler/user.html",{'schedules':schedules, 'friendsOnly':friendsOnly})
    #returns only public schedules: (Happens when user is not authenticated or user is not friends with the account we're viewing)
    return render(request, "scheduler/user.html",{'schedules':schedules})
    



