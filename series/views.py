from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Series, Season, Episode

from . import openLoadAPI as api
import json
# Create your views here.

def index(request):
	allSeries = Series.objects.all()
	context = {'allSeries' : allSeries}
	
	return HttpResponse(render(request, 'series/series.html', context))
	
	
def seriesSeasons(request, seriesId):
	try:
		series = Series.objects.get(id=seriesId)
	except Series.DoesNotExist:
		raise Http404("Series does not exist where series_id = %s" % seriesId)

	try:
		seasons = series.season_set.all()
	except Season.DoesNotExist:
		raise Http404("Seasons does not exist where series_id = %s" % seriesId)

	context = {
		'series'  : series,
		'seasons' : seasons,
		}
	
	return HttpResponse(render(request, 'series/seasons.html', context))
	
def seriesEpisodes(request, seriesId, seasonId):
	try:
		series = Series.objects.get(id=seriesId)
	except Series.DoesNotExist:
		raise Http404("Series does not exist where series_id = %s" % seriesId)

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
	
	return HttpResponse(render(request, 'series/episodes.html', context))
	
def episode(request, seriesId, seasonId, episodeId):
	try:
		series = Series.objects.get(id=seriesId)
	except Series.DoesNotExist:
		raise Http404("Series does not exist where series_id = %s" % seriesId)

	try:
		season = Season.objects.get(id=seasonId)
	except Season.DoesNotExist:
		raise Http404("Season does not exist where season_id = %s" % seasonId)

	try:
		episode = Episode.objects.get(id=episodeId)
	except Episode.DoesNotExist:
		raise Http404("Episode do not exist where series_id %s, season_id = %s, episode_id = %s" %(seriesId, seasonId, episodeId))
		
	context = {
		'series' : series,
		'season' : season,
		'episode' : episode,
		}
	
	
##	return HttpResponse(render(request, 'series/single_episode.html', context))
	return HttpResponse(render(request, 'series/html/dest/seriessingle.html', context))
	
def createSeries(request):
	login = "08af2f7ed0f90e4c"
	key	= "Vt9iQlnS"
	
	""" TODO: get list of series to update from series.csv file """
	trailerSrc = "https://www.youtube.com/watch?v=gcTkNV5Vg1E"
	imgSrc = "https://production-gameflipusercontent.fingershock.com/us-east-1:d1d29838-417f-42ee-9268-2b7776c9b340/8851aa5a-3a9d-442d-ad01-047b2b206034/ed8bcccf-dbf8-4edd-8b2a-18671ba08c6a"
	seriesFolderName = "Series"
	seriesFolderId = api.getFolderIdByName(login, key, seriesFolderName)
	assert seriesFolderId != "", "failed assert folderId not empty"
	seriesFolders = api.getFolderFoldersById(login, key, seriesFolderId)
	for serie in seriesFolders:
		serieFolderName = serie['name']
		serieFolderId = serie['id']
		try:
			seriesObj = Series.objects.get(series_name=serieFolderName)
			seriesObj.folder_id = serieFolderId
			seriesObj.img = imgSrc
			seriesObj.trailer_src = trailerSrc
		except Series.DoesNotExist:
			seriesObj = Series(	
				series_name 		= serieFolderName,
				description 		= "",
				imdb_scor			= 8,
				trailer_src			= trailerSrc,
				img 				= imgSrc,
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
				seasonObj.img = imgSrc
				
			except Season.DoesNotExist:
				seasonObj = Season(
					series		 		= seriesObj,
					season_name 		= seasonName,
					season_number		= seasonNr,
					img 				= imgSrc,
					folder_id			= seasonFolderId)
			seasonObj.save()
			
			episodes = api.getFolderFilesById(login, key, seasonFolderId)
			for episode in episodes:
				episodeNr = api.getEpisodeNumber(episode["name"])
				embedLink = "https://openload.co/embed/" + episode["linkextid"]
				episodeName = api.cleanEpisodeName(episode['name'], [serieFolderName, "-", "(1080p x265 10bit Joy)"])
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