from django.db import models

# Create your models here.
		
class Series(models.Model):
	def noImageSrc():
		return "http://cdn7.bigcommerce.com/s-gho61/stencil/31cc7cb0-5035-0136-2287-0242ac11001b/e/3dad8ea0-5035-0136-cda0-0242ac110004/images/no-image.svg"

	series_name 		= models.CharField(max_length=250)
	description 		= models.TextField(blank=True)
	release_year		= models.IntegerField(blank=True, default=0)
	finish_year		= models.IntegerField(blank=True, default=0)
	imdb_scor			= models.DecimalField(decimal_places=2, max_digits=3, default=10)
	genres				= models.CharField(max_length=250, blank=True)
	trailer_src			= models.CharField(max_length=250, blank=True)
	img 				= models.CharField(default=noImageSrc,max_length=250)
	folder_id 			= models.CharField(max_length=50, blank=True)
	
	class Meta:
		indexes = [models.Index(fields=['series_name'])]
		ordering = ['id']
	
	def __str__ (self):
		return self.series_name
	
class Season(models.Model):
	def noImageSrc():
		return "http://cdn7.bigcommerce.com/s-gho61/stencil/31cc7cb0-5035-0136-2287-0242ac11001b/e/3dad8ea0-5035-0136-cda0-0242ac110004/images/no-image.svg"

	series		 		= models.ForeignKey(Series, on_delete=models.CASCADE)
	season_name 		= models.CharField(blank=True,max_length=250)
	season_number		= models.IntegerField(default=-1)
	season_scraped_from = models.CharField(blank=True,max_length=250)
	img 				= models.CharField(default=noImageSrc,max_length=250)
	folder_id			= models.CharField(max_length=50, blank=True)
	
	class Meta:
		unique_together = (("series", "season_number"),)
		indexes = [models.Index(fields=['series', 'season_number'])]
		ordering = ['season_number']
	def __str__ (self):
		return self.season_name + ' - ' + str(self.season_number)
	
class Episode(models.Model):
	def noImageSrc():
		return "http://cdn7.bigcommerce.com/s-gho61/stencil/31cc7cb0-5035-0136-2287-0242ac11001b/e/3dad8ea0-5035-0136-cda0-0242ac110004/images/no-image.svg"

	season		 		= models.ForeignKey(Season, on_delete=models.CASCADE)
	episode_number 		= models.IntegerField(default=-1)
	episode_name 		= models.CharField(blank=True,max_length=250)
	episode_raw_name 	= models.CharField(blank=True,max_length=250)
	video_src 			= models.CharField(max_length=250)
	folder_id			= models.CharField(max_length=50, blank=True)

	class Meta:
		unique_together = (("season", "episode_number"))
		indexes = [models.Index(fields=['season', 'episode_number'])]
		ordering = ['episode_number']
		
	def __str__ (self):
		return self.episode_name + ' - ' + str(self.episode_number)
	
class Series_detail(models.Model):
	series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True)
	season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True)
	episode = models.ForeignKey(Episode, on_delete=models.CASCADE, blank=True)
	key = models.CharField(max_length=256)
	value = models.CharField(max_length=512)

	class Meta:
		indexes = [models.Index(fields=['key'])]
	
	
		
##	created_ts 			= models.DateTimeField(editable=False)
##	modified_ts			= models.DateTimeField()
##		
##	def save(self, *args, **kwargs):
##		''' On save, update timestamps '''
##		if not self.id:
##			self.created = timezone.now()
##		self.modified = timezone.now()
##		return super(User, self).save(*args, **kwargs)
