from django.db import models

# Create your models here.

class Movie(models.Model):
	def noImageSrc():
		return "http://cdn7.bigcommerce.com/s-gho61/stencil/31cc7cb0-5035-0136-2287-0242ac11001b/e/3dad8ea0-5035-0136-cda0-0242ac110004/images/no-image.svg"

	movie_name 			= models.CharField(max_length=250)
	description 		= models.TextField(blank=True)
	video_src 			= models.CharField(max_length=250)
	release_date		= models.DateField(blank=True)
	imdb_scor			= models.IntegerField(default=10)
	genres				= models.CharField(max_length=250, blank=True)
	trailer_src			= models.CharField(max_length=250, blank=True)
	img 				= models.CharField(default=noImageSrc,max_length=250)
	
	
	def __str__ (self):
		return self.movie_name
	
