from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^$','scheduler.views.home_view'),
        url(r'^login$','scheduler.views.login_view'),
        url(r'^logout$','scheduler.views.logout_view'),
        url(r'^is_loggedin','scheduler.views.is_loggedin_view'),
        )
