from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
# Create your views here.

def index(request):
	allMovies = Movie.objects.all()
	context = {'allMovies' : allMovies}
	
	return HttpResponse(render(request, 'movies/index.html', context))
	
