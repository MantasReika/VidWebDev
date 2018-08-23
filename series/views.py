from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.conf import settings
from .models import Series, Season, Episode

import os

from . import openLoadAPI as api
import json
# Create your views here.

def index(request):
	allSeries = Series.objects.all()
	context = {'allSeries' : allSeries}
	viewMode = request.GET.get('view')
	if viewMode == 'list':
		return HttpResponse(render(request, 'series/html/dest/movielist.html', context))
	else:
		return HttpResponse(render(request, 'series/html/dest/moviegrid.html', context))
	
	
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
	print(settings.BASE_DIR)
	meta = api.metaData(os.path.join(settings.BASE_DIR, "OpenLoadUpdateDatabase.csv"))
	
	seriesFolderName = "Series"
	seriesFolderId = api.getFolderIdByName(login, key, seriesFolderName)
	assert seriesFolderId != "", "failed assert folderId not empty"
	seriesFolders = api.getFolderFoldersById(login, key, seriesFolderId)
	for serie in seriesFolders:
		serieFolderName = serie['name']
		serieFolderId = serie['id']
		meta.setCurrentMovie(serieFolderName)
		try:
			seriesObj 				= Series.objects.get(series_name=serieFolderName)
			seriesObj.folder_id 	= serieFolderId
			seriesObj.release_year 	= meta.getReleaseYear()
			seriesObj.finish_year 	= meta.getFinishYear()
			seriesObj.imdb_scor 	= meta.getImdb()
			seriesObj.trailer_src 	= meta.getTrailer()
			seriesObj.img 			= meta.getImage()
			seriesObj.genres 		= meta.getGenres()
			seriesObj.description	= meta.getDescription()
		except Series.DoesNotExist:
			seriesObj = Series(	
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
				episodeName = api.cleanEpisodeName(episode['name'], [serieFolderName] + meta.getCleanNameParts())
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