from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.edit import UpdateView


# Create your views here.

from .models import Manga, Volume, Chapter

class MangaListView(ListView): 
	model = Manga

class VolumeListView(ListView): 
	model = Volume

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(VolumeListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

class ChapterListView(ListView): 
	model = Chapter

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Chapter.objects.filter(volume__manga__name=self.manga)

	def get_context_data(self, **kwargs):
		context = super(ChapterListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

class VChapterListView(ListView): 
	model = Chapter

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Chapter.objects.filter(volume__manga__name=self.manga, volume__n_vol=self.kwargs["volume_n_vol"])

	def get_context_data(self, **kwargs):
		context = super(VChapterListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

class ChapterUpdate(UpdateView):
	model = Chapter
	fields = ['read']
	#success_url = reverse_lazy('script')

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.kwargs["manga_name"], n_chap=self.kwargs["chapter_n_chap"])
		return Chapter.objects.filter(volume__manga__name=self.manga, n_chap=self.chapter.get_chap())

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		context['chapter'] = self.chapter
		return context

def index(request):
	manga_list = Manga.objects.order_by('name')
	context = {'manga_list': manga_list}
	return render(request, 'mangascripts/index.html', context)

def volume(request, manga_name):
	manga = get_object_or_404(Manga, name=manga_name)
	context = {'manga': manga}
	return render(request, 'mangascripts/volume.html', context)

def chapter(request, manga_name):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter_list = Chapter.objects.filter(volume__manga__name=manga_name).order_by('n_chap')
	context = {"manga":manga, "chapter_list" : chapter_list}
	return render(request, 'mangascripts/chapter.html', context)

def vchapter(request, manga_name, volume_n_vol):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter_list = Chapter.objects.filter(volume__manga__name=manga_name, volume__n_vol=volume_n_vol).order_by('n_chap')
	context = {"manga":manga, "chapter_list" : chapter_list}
	return render(request, 'mangascripts/vchapter.html', context)

def script(request, manga_name, chapter_n_chap):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter = Chapter.objects.get(volume__manga__name=manga_name, n_chap=chapter_n_chap)
	context = {'manga': manga, "chapter" : chapter}
	return render(request, 'mangascripts/script.html', context)
