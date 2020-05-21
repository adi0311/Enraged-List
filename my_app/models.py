from django.db import models

# Create your models here.
class Search(models.Model):
	search = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now=True) 

	def __str__(self):
		return '{}'.format(self.search)

	class Meta:
		verbose_name_plural = 'Searches'

class VisitedArticle(models.Model):
	article_title = models.CharField(max_length=128)
	article_url = models.CharField(max_length=500)
	date_created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.article_title

	class Meta:
		verbose_name_plural = 'Articles'
