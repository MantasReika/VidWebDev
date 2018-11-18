"""videoWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'watch'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^series/$', views.seriesIndex, name="seriesIndex"),    
    url(r'^(?P<seriesId>[0-9]+)/$', views.seriesSeasons, name="seriesSeasons"),
    url(r'^(?P<seriesId>[0-9]+)/(?P<seasonId>[0-9]+)/$', views.seriesEpisodes, name="seriesEpisodes"),
	url(r'^(?P<seriesId>[0-9]+)/(?P<seasonId>[0-9]+)/(?P<episodeId>[0-9]+)/$', views.watchEpisode, name="watchEpisode"),
	
	url(r'^movies/$', views.moviesIndex, name="moviesIndex"),
	url(r'^movies/(?P<movieId>[0-9]+)$', views.watchMovie, name="watchMovie"),
	
    url(r'^createSeries$', views.createSeries, name="createSeries"),
	url(r'^createMovies$', views.createMovies, name="createMovies"),
	
	
]