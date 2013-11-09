from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    
    schedule = models.ForeignKey(Schedule)
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES)

