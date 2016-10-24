from __future__ import unicode_literals

from django.db import models
from django.urls import reverse, reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Manga(models.Model):
	name = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	user = models.IntegerField()
	def __str__(self):
		return str(self.name)
	def get_absolute_url(self):
		return reverse('manga')
	class Meta:
		unique_together = ('name', 'author')
		ordering = ["name"]


class Volume(models.Model):
	manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
	n_vol = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	title = models.CharField(max_length=200)
	user = models.IntegerField()
	def __str__(self):
		return str(self.manga.name) + " > Vol." + str(self.n_vol)
	def get_absolute_url(self):
		return reverse('volume', kwargs={'manga_name':self.manga.name})
	class Meta:
		unique_together = ('manga', 'n_vol')
		ordering = ["n_vol"]


class Chapter(models.Model):
	volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
	n_chap = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	title = models.CharField(max_length=200)
	script = models.TextField()
	user = models.IntegerField()
	translated = models.BooleanField(default=False)
	def __str__(self):
		return str(self.volume.manga.name) + " > Vol." + str(self.volume.n_vol) + " > Cap." + str(self.n_chap)
	def get_chap(self):
		return self.n_chap
	#def get_absolute_url(self):
		#return reverse('chapter', kwargs={'manga_name':self.volume.manga.name})
	class Meta:
		unique_together = ('volume', 'n_chap')
		ordering = ["n_chap"]
