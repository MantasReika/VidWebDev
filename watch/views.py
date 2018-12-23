from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.conf import settings
from .models import Serie, Season, Episode
from .models import Movie

import os

from . import openLoadAPI as api
import json

#######
def formatVideoPlayer(videoHost, videoSrc):
	openLoadHtmlPlayer = '<iframe src="%s" scrolling="no" frameborder="0" width="700" height="430" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>'
	youtubeHtmlPlayer = '<iframe width="700" height="430" src="%s"></iframe>'
	defaultHtml = '<a href="%s">%s</a>'
	if videoHost == 'openload':
		return openLoadHtmlPlayer % (videoSrc)
	elif videoHost == 'youtube':
		youtubeHtmlPlayer % (videoSrc)
	else:
		return defaultHtml % (videoSrc, videoSrc)

# Create your views here.

def index(request):
	context = {}
	return HttpResponse(render(request, 'watch/index.html', context))

def moviesIndex(request):
	if request.method == 'GET':
		# create a form instance and populate it with data from the request:
		print()
		print("if request.method == 'GET'")

		url_search_kw = request.GET.getlist('search_kw')
		url_genre = request.GET.getlist('genres')
		url_ratings = request.GET.getlist('rating')
		url_from_yr = request.GET.get('from_yr')
		url_to_yr = request.GET.get('to_yr')
		
		print("search_kw: %s" % url_search_kw)
		print("genres: %s" % url_genre)
		print("ratings: %s" % url_ratings)
		print("from_yr: %s" % url_from_yr)
		print("to_yr: %s" % url_to_yr)
		print()
		
		allMovies = Movie.objects.all()
		filteredMovies = Movie.objects.all()
		
		if url_ratings != []:
			ratings = []
			for rating in url_ratings:
				ratings.append(int(rating.split("_")[0]))
				ratings.append(int(rating.split("_")[1]))
			
			ratings = sorted(ratings)
			print(ratings)
			filteredMovies = filteredMovies.filter(imdb_scor__gt=ratings[0], imdb_scor__lt=ratings[1])
		
		if url_genre != []:
			print('"%s"' % url_genre)
			filteredMovies = filteredMovies.filter(genres__icontains=url_genre[0])
			print(filteredMovies)
		
		#for i in url
		#if len(url_genres) > 0:
		#	filteredMovies = Movie.objects.filter(genres__icontains=url_genres)
		
		#if len(url_rating) > 0:
	#		ratingTopVal = url_rating[0].split("_")[0]
#		#
		#if len(url_rating) > 0:
	#		ratingDownVal = url_rating[0].split("_")[1]
#		
		#if len() > 0:
		#	ratingFilterMovies = Movie.objects.filter(rating__)
	
	#if filteredMovies != []:
		context = {'allMovies' : filteredMovies}
	#else:
	#	context = {'allMovies' : allMovies}
	return HttpResponse(render(request, 'watch/html/dest/moviegrid.html', context))

"""        form = NameForm(request.POST)
# check whether it's valid:
if form.is_valid():
# process the data in form.cleaned_data as required
# ...
# redirect to a new URL:
return HttpResponseRedirect('/thanks/')

# if a GET (or any other method) we'll create a blank form
	else:
		print("if request.method != 'GET'")
		
	allMovies = Movie.objects.all()
	context = {'allMovies' : allMovies}
	return HttpResponse(render(request, 'watch/html/dest/moviegrid.html', context))"""

def watchMovie(request, movieId):
	try:
		movie = Movie.objects.get(id=movieId)
	except Movie.DoesNotExist:
		raise Http404("Movie do not exist where movie_id %s" %(movieId))
		
	videoPlayer = formatVideoPlayer(movie.video_host, movie.video_src)
	context = {
		'movie' : movie,
		'videoPlayer' : videoPlayer
		}
	
	return HttpResponse(render(request, 'watch/html/dest/watchMovie.html', context))
	
def seriesIndex(request):
	allSeries = Serie.objects.all()
	context = {'allSeries' : allSeries}
#		viewMode = request.GET.get('view')
#		if viewMode == 'list':
#			return HttpResponse(render(request, 'watch/html/dest/movielist.html', context))
#		else:
	return HttpResponse(render(request, 'watch/html/dest/seriesgrid.html', context))
	
	
def seriesSeasons(request, seriesId):
	try:
		series = Serie.objects.get(id=seriesId)
	except Serie.DoesNotExist:
		raise Http404("Serie does not exist where series_id = %s" % seriesId)

	try:
		seasons = series.season_set.all()
	except Season.DoesNotExist:
		raise Http404("Seasons does not exist where series_id = %s" % seriesId)

	context = {
		'series'  : series,
		'seasons' : seasons,
		}
	
	return HttpResponse(render(request, 'watch/html/dest/seasonsgrid.html', context))
	
def seriesEpisodes(request, seriesId, seasonId):
	try:
		series = Serie.objects.get(id=seriesId)
	except Serie.DoesNotExist:
		raise Http404("Serie does not exist where series_id = %s" % seriesId)

	try:
		season = Season.objects.get(id=seasonId)
	except Season.DoesNotExist:
		raise Http404("Season does not exist where season_id = %s" % seasonId)

	try:
		episodes = season.episode_set.all()
	except Season.DoesNotExist:
		raise Http404("Episodes do not exist where series_id %s, season_id = %s" %(seriesId, seasonId))
		
	context = {
		'series' : series,
		'season' : season,
		'episodes' : episodes,
		}
	
	return HttpResponse(render(request, 'watch/episodes.html', context))
	
def watchEpisode(request, seriesId, seasonId, episodeId):
	try:
		series = Serie.objects.get(id=seriesId)
	except Serie.DoesNotExist:
		raise Http404("Serie does not exist where series_id = %s" % seriesId)

	try:
		season = Season.objects.get(id=seasonId)
	except Season.DoesNotExist:
		raise Http404("Season does not exist where season_id = %s" % seasonId)

	try:
		episode = Episode.objects.get(id=episodeId)
	except Episode.DoesNotExist:
		raise Http404("Episode do not exist where series_id %s, season_id = %s, episode_id = %s" %(seriesId, seasonId, episodeId))
		
	videoPlayer = formatVideoPlayer(episode.video_host, episode.video_src)
	
	context = {
		'series' : series,
		'season' : season,
		'episode' : episode,
		'videoPlayer' : videoPlayer
		}
	
	
##	return HttpResponse(render(request, 'series/single_episode.html', context))
	return HttpResponse(render(request, 'watch/html/dest/watchEpisode.html', context))
	
def createSeries(request):
	login = "08af2f7ed0f90e4c"
	key	= "Vt9iQlnS"
	print(settings.BASE_DIR)
	meta = api.metaData(os.path.join(settings.BASE_DIR, "OpenLoadUpdateSeriesDatabase.csv"))
	
	seriesFolderName = "Series"
	seriesFolderId = api.getFolderIdByName(login, key, seriesFolderName)
	assert seriesFolderId != "", "failed assert folderId not empty"
	seriesFolders = api.getFolderFoldersById(login, key, seriesFolderId)
	for serie in seriesFolders:
		serieFolderName = serie['name']
		serieFolderId = serie['id']
		meta.setCurrentMovie(serieFolderName)
		try:
			seriesObj 				= Serie.objects.get(series_name=serieFolderName)
			seriesObj.folder_id 	= serieFolderId
			seriesObj.release_year 	= meta.getReleaseYear()
			seriesObj.finish_year 	= meta.getFinishYear()
			seriesObj.imdb_scor 	= meta.getImdb()
			seriesObj.trailer_src 	= meta.getTrailer()
			seriesObj.img 			= meta.getImage()
			seriesObj.genres 		= meta.getGenres()
			seriesObj.description	= meta.getDescription()
		except Serie.DoesNotExist:
			seriesObj = Serie(	
				series_name 		= serieFolderName,
				release_year		= meta.getReleaseYear(),
				finish_year			= meta.getFinishYear(),
				imdb_scor			= meta.getImdb(),
				trailer_src			= meta.getTrailer(),
				img 				= meta.getImage(),
				genres				= meta.getGenres(),
				description 		= meta.getDescription(),
				folder_id 			= serieFolderId)
		seriesObj.save()
		
		seasons = api.getFolderFoldersById(login, key, serieFolderId)
		
		for season in seasons:
			seasonName = season['name']
			seasonNr = api.getSeasonNumber(season['name'])
			seasonFolderId = season['id']
			try:
				seasonObj = Season.objects.get(series=seriesObj, season_number=seasonNr)
				seasonObj.folder_id = seasonFolderId
				seasonObj.img = meta.getImage()
				
			except Season.DoesNotExist:
				seasonObj = Season(
					series		 		= seriesObj,
					season_name 		= seasonName,
					season_number		= seasonNr,
					img 				= meta.getImage(),
					folder_id			= seasonFolderId)
			seasonObj.save()
			
			episodes = api.getFolderFilesById(login, key, seasonFolderId)
			for episode in episodes:
				episodeNr = api.getEpisodeNumber(episode["name"])
				embedLink = "https://openload.co/embed/" + episode["linkextid"]
				episodeName = api.cleanName(episode['name'], [serie['name']] + meta.getCleanNameTextParts(), meta.getCleanNameRegexParts(), meta.getReplaceNameParts() )
				try:
					episodeObj = Episode.objects.get(season=seasonObj, episode_number=episodeNr)
					episodeObj.episode_name = episodeName
					episodeObj.episode_raw_name = episode['name']
					episodeObj.video_src = embedLink
					episodeObj.folder_id = episode['folderid']
					
				except Episode.DoesNotExist:
					episodeObj = Episode(
						season		 		= seasonObj,
						episode_number 		= episodeNr,
						episode_name 		= episodeName,
						episode_raw_name	= episode["name"],
						video_src 			= embedLink,
						folder_id			= episode['folderid'])
						
				episodeObj.save()

	return HttpResponse("")	
	
def createMovies(request):
	""" 
	Update movies database from OpenLoad server 
	Has to find 'Movies' folder in OpenLoad root directory
	Collects all files from 'Movies' folder and creates records in Movies table
	"""
	login = "08af2f7ed0f90e4c"
	key	= "Vt9iQlnS"
	resp = ""
	
	moviesFolderName = "Movies"
	moviesFolderId = api.getFolderIdByName(login, key, moviesFolderName)
	
	assert moviesFolderId != None, "Folder named '%s' not found..." % moviesFolderName
	movies = api.getFolderFilesById(login, key, moviesFolderId)			
	for movie in movies:
		movieRawName = movie["name"]
		movieName = api.cleanName(movieRawName, ['.mp4'])
		embedLink = "https://openload.co/embed/" + movie["linkextid"]
		try:
			movieObj = Movie.objects.get(movie_name=movieName)
			movieObj.video_src = embedLink
			resp += 'Updated: %s<br>' % movieName
		except Movie.DoesNotExist:
			movieObj = Movie(
				movie_name 			= movieName,
				movie_raw_name		= movieRawName,
				video_src 			= embedLink,
				description 		= "",
				release_year		= 0,
				imdb_scor			= 9.9,
				genres				= "",
				trailer_src			= "",
				img 				= "",
				folder_id 			= "")
			
			resp += 'Created: %s<br>' % movieName
		
		movieObj.save()
	return HttpResponse("<h1>Done. <br> moviesFolderId: %s</h1><br>%s" % (moviesFolderId, resp))
