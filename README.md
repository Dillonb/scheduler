Scheduler
========

A system to manage and compare your daily schedules.
Created by [Dillon Beliveau](https://github.com/Dillonb) and [Elliot DeMatteis](https://github.com/brasky).

Installing
----------
1. Clone this git repository to your Django installation.
2. Add scheduler to your list of installed apps.
3. Update your urls.py to include scheduler's.
4. Set up your database.
5. Run manage.py syncdb.

Code for urls.py:

    url(r'^', include('scheduler.urls')),
