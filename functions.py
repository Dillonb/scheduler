import datetime
from django.core.cache import cache
from scheduler.models import Profile, Event
def datetime_to_week(dt):
        weekday = dt.weekday()
        # If sunday, monday is the day after (not 6 days before)
        if weekday == 6:
            monday = dt + datetime.timedelta(days=1)
        else:
            # Subtract the day of the week from the current day to get monday.
            monday = dt - datetime.timedelta(days=weekday)

        # Create an array of datetime objects holding every day of the (current) week
        week = [monday - datetime.timedelta(days=1), # Sunday
                monday,                              # Monday
                monday + datetime.timedelta(days=1), # Tuesday
                monday + datetime.timedelta(days=2), # Wednesday
                monday + datetime.timedelta(days=3), # Thursday
                monday + datetime.timedelta(days=4), # Friday
                monday + datetime.timedelta(days=5), # Saturday
                ]
        return week

# Checks if value1 is between value2 and value3
def value_between(value1, value2, value3):
    return (value1 >= value2 and value1 <= value3)

def events_overlap(event1, event2):
    if event1 == event2:
        return False # They are the same event.

    # Check both events to see if they start while the other one is going on.
    if value_between(event1.start_time, event2.start_time, event2.end_time):
        return True
    if value_between(event2.start_time, event1.start_time, event1.end_time):
        return True

    # Check both events to see if they end while the other one is going on.
    if value_between(event1.end_time, event2.start_time, event2.end_time):
        return True
    if value_between(event2.end_time, event1.start_time, event1.end_time):
        return True

    # Otherwise, they don't overlap
    return False

def combine_events(event1, event2):
    # get EARLIER start_time
    if event1.start_time < event2.start_time:
        start_time = event1.start_time
    else:
        start_time = event2.start_time

    # get LATER end_time
    if event1.end_time > event2.end_time:
        end_time = event1.end_time
    else:
        end_time = event2.end_time

    # The final, combined event
    return Event(
            name="Combined Event",
            location="N/A",
            description="Combined two events",
            start_time=start_time,
            end_time=end_time,
            sunday=True,monday=True,tuesday=True,wednesday=True,thursday=True,friday=True,saturday=True, # Set all to true (it won't matter, because this event set is already matched to a day.
            start_date=datetime.datetime(1970,1,1),
            end_date=datetime.datetime(3000,12,31)
            )

# Alias because why not
def get_busy(events):
    return get_times_when_busy(events)

def get_times_when_busy(events):
    had_an_overlap = False # Do we need to check again to make sure?
    for event in events:
        for event2 in events:
            if event == event2:
                continue

            if events_overlap(event, event2):
                had_an_overlap = True # We need to check again
                events.append(combine_events(event, event2))
                # Remove the two events we just combined from the list so they don't get processed again.

                try:
                    events.remove(event)
                except ValueError:
                    pass
                try:
                    events.remove(event2)
                except ValueError:
                    pass
    if had_an_overlap:
        return get_times_when_busy(events) # Recurse and check again.
    else:
        return events

def get_schedule_time_for_user(schedule, user):
    """Checks the database cache for information on what date the specified user was last viewing on the specified schedule."""
    time=cache.get(str(user.id)+"_"+str(schedule.id)+"_"+"_last_time")
    if time == None:
        return ""
    else:
        return str(time)

def set_schedule_time_for_user(schedule, user, time):
    """Saves the data needed for the above function (the time the specified user was last viewing on the specified schedule."""
    cache.set(str(user.id)+"_"+str(schedule.id)+"_"+"_last_time", time, 3600)

def from_top_by_time(self, time):
    fromtop = float(time.hour) + float(time.minute)/60.0 + float(time.second)/3600.0
    fromtop *= 50 # 50px for each hour
    return int(fromtop)
