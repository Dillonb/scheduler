from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^$','scheduler.views.home_view'),
        url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'scheduler/login.html'}),        
        url(r'^accounts/logout$','scheduler.views.logout_view'),
        url(r'^accounts/is_loggedin$','scheduler.views.is_loggedin_view'),
        url(r'^accounts/register$','scheduler.views.register_view'),
        url(r'^accounts/profile$','scheduler.views.account_view'),
        url(r'^createevent$','scheduler.views.create_event_view'),
        )
