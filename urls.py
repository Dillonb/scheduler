from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^$','scheduler.views.home_view'),
        url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'scheduler/login.html'}),        
        url(r'^accounts/logout/$','scheduler.views.logout_view'),
        url(r'^accounts/is_loggedin/$','scheduler.views.is_loggedin_view'),
        url(r'^accounts/register/$','scheduler.views.register_view'),
        url(r'^accounts/profile/$','scheduler.views.account_view'),
        url(r'^createevent/(?P<scheduleid>\d+)$','scheduler.views.create_event_view'),
        url(r'^schedule/(?P<scheduleid>\d+)/(?P<starttime>\d+)?$','scheduler.views.schedule_view'),
        url(r'^schedule/(?P<otheruserid>\d+)/(?P<starttime>\d+)/compare/(?P<viewinguserid>\d+)$','scheduler.views.schedule_compare_view'),
        url(r'^accounts/createschedule/$','scheduler.views.create_schedule_view'),
        url(r'^friends/$','scheduler.views.friends_view'),
        url(r'^friends/accept/(?P<friendid>\d+)$','scheduler.views.friends_accept_view'),
        url(r'^friends/add/$','scheduler.views.friends_add_view'),
        url(r'^friends/decline/(?P<friendid>\d+)$','scheduler.views.friends_decline_view'),
        url(r'^user/(?P<userid>\d+)$','scheduler.views.account_page_view'),
        url(r'^editschedule/(?P<scheduleid>\d+)$','scheduler.views.edit_schedule_view'),
        url(r'^editevent/(?P<eventid>\d+)$','scheduler.views.edit_event_view'),
        url(r'^setmainschedule/(?P<scheduleid>\d+)$','scheduler.views.set_main_schedule_view'),
        url(r'^deleteschedule/(?P<scheduleid>\d+)$','scheduler.views.delete_schedule_view'),
                       
        )
