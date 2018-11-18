from django.contrib import admin
from .models import Serie, Season, Episode
from .models import Movie
	
# Register your models here.

admin.site.register(Episode)
admin.site.register(Season)
admin.site.register(Serie)

admin.site.register(Movie)
