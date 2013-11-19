from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError


class Schedule(models.Model):
    VISIBILITY_PUBLIC = 0
    VISIBILITY_FRIENDSONLY = 1
    VISIBILITY_PRIVATE = 2

    VISIBILITY_CHOICES = (
            (VISIBILITY_PUBLIC, "Public"),
            (VISIBILITY_FRIENDSONLY, "Friends Only"),
            (VISIBILITY_PRIVATE, "Private")
            )
    creator = models.ForeignKey(User)
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES)
    name = models.CharField(max_length=150)

    def __str__(self):
        return "%s %s: %s"%(self.creator, self.visibility, self.name)

class EventManager(models.Manager):
    # Gets all events happening on a certain date.
    def on_date(self, date, schedule):
        # Gets the name of of the day (for use in the django query dict)
        weekdayname = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"][date.weekday()]
        return self.filter(**{'schedule':schedule, 'start_date__lte':date, 'end_date__gte':date, weekdayname:True})

class Event(models.Model):
    VISIBILITY_INHERIT = -1
    VISIBILITY_PUBLIC = 0
    VISIBILITY_FRIENDSONLY = 1
    VISIBILITY_PRIVATE = 2
    VISIBILITY_SHARED = 3

    VISIBILITY_CHOICES = (
            (VISIBILITY_INHERIT, "Inherit from Schedule"),
            (VISIBILITY_PUBLIC, "Public"),
            (VISIBILITY_FRIENDSONLY, "Friends Only"),
            (VISIBILITY_PRIVATE, "Private")
            )

    schedule = models.ForeignKey(Schedule) # Parent schedule
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES) # Visibility permissions

    start_time = models.TimeField() # Holds the time the event starts
    end_time = models.TimeField() # Holds the time the event ends

    start_date = models.DateField() # Holds the FIRST DAY that the event happens on
    end_date = models.DateField() # Holds the LAST DAY that the event happens on

    # Shows which days the event happens on
    sunday = models.BooleanField()
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()

    name = models.CharField(max_length=50) # Name of the event. Short and sweet.
    location = models.CharField(max_length=250) # The location of the event. Address?
    description = models.TextField() # Description of event

    objects = EventManager()

    def __str__(self):
        return "%s's event, (%s): %s-%s"%(self.schedule.creator.username, self.name, self.start_time, self.end_time)

    def clean(self):
        # Make sure the event has a duration. (Doesn't start and end at the same time)
        if self.start_time == self.end_time:
            raise ValidationError("Event must have a duration.")
        # make sure the event starts before it ends.
        if self.start_time > self.end_time:
            raise ValidationError("Event must start before it ends.")

    
    def weekdays(self):
        return [self.sunday, self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday]

    def from_top_by_time(self, time):
        fromtop = float(time.hour) + float(time.minute)/60.0 + float(time.second)/3600.0
        fromtop *= 50 # 50px for each hour
        return int(fromtop)

    def from_top(self):
        return self.from_top_by_time(self.start_time)

    def height(self):
        return self.from_top_by_time(self.end_time) - self.from_top_by_time(self.start_time)

class FriendManager(models.Manager):
    def are_friends(self, user, other):
        # Check both orientations of the friend object.
        friend = self.get_friend_object(user, other)

        if friend.status == Friend.STATUS_SENT: # If a request has not been accepted
            return False # The users are not friends yet.
        return True # Otherwise they are.

    def get_friend_object(self, user, other):
        friend = self.get_or_none(creator=user, friend=other)
        if friend == None:
            friend = self.get_or_none(creator=other, friend=user)
        return friend

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except Friend.DoesNotExist:
            return None

    def all_friends_for_user(self, user):
        friends = []
        for friend in self.filter(creator=user).select_related(depth=1):
            friends.append(friend)
        for friend in self.filter(friend=user).select_related(depth=1):
            friends.append(friend)
        return friends

    def friends_for_user(self, user):
        friends = []
        for friend in self.all_friends_for_user(user):
            if friend.status != Friend.STATUS_SENT:
                friends.append(friend)
        return friends

    def friend_requests_pending_for_user(self, user):
        friends = []
        for friend in self.filter(friend=user, status=Friend.STATUS_SENT).select_related(depth=1):
            friends.append(friend)
        return friends
    
    def friend_requests_sent_for_user(self, user):
        friends = []
        for friend in self.filter(creator=user, status=Friend.STATUS_SENT).select_related(depth=1):
            friends.append(friend)
        return friends

class Friend(models.Model):
    RELATIONSHIP_UNSPECIFIED = -1
    RELATIONSHIP_FAMILY = 0
    RELATIONSHIP_FRIEND = 1
    RELATIONSHIP_COWORKER = 2
    RELATIONSHIP_CLASSMATE = 3

    RELATIONSHIP_CHOICES = (
            (RELATIONSHIP_UNSPECIFIED, "Unspecified"),
            (RELATIONSHIP_FAMILY, "Family Member"),
            (RELATIONSHIP_FRIEND, "Friend"),
            (RELATIONSHIP_COWORKER, "Coworker"),
            (RELATIONSHIP_CLASSMATE, "Classmate")
            )

    STATUS_SENT = 0 # Friend request sent
    STATUS_ACCEPTED = 1 # Friend request accepted (the users are now friends)
    STATUS_MATCHED = 2 # Friend request matched to another. (Both users sent friend requests to each other)

    STATUS_CHOICES = (
            (STATUS_SENT, "Sent"),
            (STATUS_ACCEPTED, "Accepted"),
            (STATUS_MATCHED, "Matched")
            )

    creator = models.ForeignKey(User, related_name="friend_creator_set") # The person who sent the friend request
    friend = models.ForeignKey(User, related_name="friend_set") # The person who received the friend request.
    created = models.DateTimeField(auto_now_add=True, editable=False) # The date the friend request was sent
    status = models.IntegerField(default = STATUS_SENT, choices = STATUS_CHOICES) # Whether or not the friend request has been accepted (If the two users are friends)
    relationship_creator = models.IntegerField(choices = RELATIONSHIP_CHOICES, default = RELATIONSHIP_UNSPECIFIED) # The relationship between the users from the creator's perspective. (family, friend, coworker, classmate)
    relationship_friend = models.IntegerField(choices = RELATIONSHIP_CHOICES, default = RELATIONSHIP_UNSPECIFIED) # The relationship between the users from the friend's perspective. Can be different than relationship_creator.

    objects = FriendManager()


admin.site.register(Schedule)
admin.site.register(Event)
admin.site.register(Friend)
