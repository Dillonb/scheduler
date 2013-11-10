from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


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

    def __str__(self):
        return "%s's event"%(self.schedule.creator.username)

admin.site.register(Schedule)
admin.site.register(Event)
