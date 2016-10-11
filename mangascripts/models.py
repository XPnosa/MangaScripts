from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Manga(models.Model):
	name = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	def __str__(self):
		return str(self.name)
	class Meta:
		unique_together = ('name', 'author')


class Volume(models.Model):
	manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
	n_vol = models.IntegerField(default=0)
	title = models.CharField(max_length=200)
	def __str__(self):
		return str(self.manga.name) + " > Vol." + str(self.n_vol)
	class Meta:
		unique_together = ('manga', 'n_vol', 'title')


class Chapter(models.Model):
	volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
	n_chap = models.IntegerField(default=0)
	title = models.CharField(max_length=200)
	script = models.TextField()
	def __str__(self):
		return str(self.volume) + " > Cap." + str(self.n_chap)
	class Meta:
		unique_together = ('volume', 'n_chap', 'title', 'script')
