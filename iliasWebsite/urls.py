
from django.contrib import admin
from django.conf.urls import patterns, include, url

urlpatterns = [
    # Examples:
    url(r'^', include("iliasApp.urls", namespace='iliasApp')),
    url(r'^admin/', include(admin.site.urls)),
]
