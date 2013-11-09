from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^$','scheduler.views.home_view'),
        url(r'^accounts/login$','scheduler.views.login_view'),
        url(r'^accounts/logout$','scheduler.views.logout_view'),
        url(r'^accounts/is_loggedin$','scheduler.views.is_loggedin_view'),
        url(r'^accounts/register$','scheduler.views.register_view'),
        url(r'^account$','scheduler.views.account_view'),
        url(r'^createevent$','scheduler.views.create_event_view'),
        )
