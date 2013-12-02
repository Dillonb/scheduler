import datetime
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
