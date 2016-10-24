from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.

from .models import Manga, Volume, Chapter

# Genericas
# Listas

class MangaListView(ListView): 
	model = Manga
	paginate_by = 10

class VolumeListView(ListView): 
	model = Volume
	paginate_by = 10

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(VolumeListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

class ChapterListView(ListView): 
	model = Chapter
	paginate_by = 10

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Chapter.objects.filter(volume__manga__name=self.manga)

	def get_context_data(self, **kwargs):
		context = super(ChapterListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		context['volumeless'] = True
		return context

class VChapterListView(ListView): 
	model = Chapter
	paginate_by = 10

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Chapter.objects.filter(volume__manga__name=self.manga, volume__n_vol=self.kwargs["volume_n_vol"])

	def get_context_data(self, **kwargs):
		context = super(VChapterListView, self).get_context_data(**kwargs)
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		context['manga'] = self.manga
		context['volume'] = self.volume
		return context

# Manga

class MangaAdd(CreateView):
	model = Manga
	fields = ['name','author','user']

class MangaUpdate(UpdateView):
	model = Manga
	fields = ['author']

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Manga.objects.filter(name=self.manga)

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

class MangaDelete(DeleteView):
	model = Manga
	success_url = reverse_lazy('manga')

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Manga.objects.filter(name=self.manga)

	def get_context_data(self, **kwargs):
		context = super(DeleteView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

# Volumen

class VolumeAdd(CreateView):
	model = Volume
	fields = ['manga','n_vol','title','user']

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		context['manga'] = self.manga
		return context

class VolumeUpdate(UpdateView):
	model = Volume
	fields = ['title']

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		return context

class VolumeDelete(DeleteView):
	model = Volume
	#success_url = reverse_lazy('manga')

	def get_success_url(self, **kwargs):
		return reverse_lazy('volume', kwargs = {'manga_name': self.manga.name})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(DeleteView, self).get_context_data(**kwargs)
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		context['manga'] = self.manga
		return context

# Capitulo

class ChapterAdd(CreateView):
	model = Chapter
	fields = ['volume','n_chap','title','script','translated','user']

	def get_success_url(self, **kwargs):
		return reverse_lazy('chapter', kwargs = {'manga_name': self.get_manga().name})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.volume = Volume.objects.filter(manga=self.manga)
		context['manga'] = self.manga
		context['volumeless'] = True
		context['volume_list'] = self.volume
		return context

class VChapterAdd(CreateView):
	model = Chapter
	fields = ['volume','n_chap','title', 'script', 'translated','user']

	def get_success_url(self, **kwargs):
		return reverse_lazy('vchapter', kwargs = {'manga_name': self.get_manga().name, 'volume_n_vol':self.get_volume().n_vol})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_volume(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		return self.volume

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		context['manga'] = self.manga
		context['volume'] = self.volume
		return context

class ChapterUpdate(UpdateView):
	model = Chapter
	fields = ['title','script','translated']

	def get_success_url(self, **kwargs):
		return reverse_lazy('chapter', kwargs = {'manga_name': self.get_manga().name})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.kwargs["manga_name"], n_chap=self.kwargs["chapter_n_chap"])
		return Chapter.objects.filter(volume__manga__name=self.manga, n_chap=self.chapter.get_chap())

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		context['chapter'] = self.chapter
		context['volumeless'] = True
		return context

class VChapterUpdate(UpdateView):
	model = Chapter
	fields = ['title','script','translated']

	def get_success_url(self, **kwargs):
		return reverse_lazy('vchapter', kwargs = {'manga_name': self.get_manga().name, 'volume_n_vol':self.get_volume().n_vol})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_volume(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		return self.volume

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.kwargs["manga_name"], n_chap=self.kwargs["chapter_n_chap"])
		return Chapter.objects.filter(volume__manga__name=self.manga, n_chap=self.chapter.get_chap())

	def get_context_data(self, **kwargs):
		context = super(UpdateView, self).get_context_data(**kwargs)
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		context['manga'] = self.manga
		context['volume'] = self.volume
		context['chapter'] = self.chapter
		return context

class ChapterDelete(DeleteView):
	model = Chapter
	#success_url = reverse_lazy('manga')

	def get_success_url(self, **kwargs):
		return reverse_lazy('chapter', kwargs = {'manga_name': self.volume.manga.name})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.kwargs["manga_name"], n_chap=self.kwargs["chapter_n_chap"])
		return Chapter.objects.filter(volume__manga__name=self.manga, n_chap=self.chapter.get_chap())

	def get_context_data(self, **kwargs):
		context = super(DeleteView, self).get_context_data(**kwargs)
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.manga, n_chap=self.kwargs["chapter_n_chap"])
		context['manga'] = self.manga
		context['chapter'] = self.chapter
		context['volumeless'] = True
		return context

class VChapterDelete(DeleteView):
	model = Chapter
	#success_url = reverse_lazy('manga')

	def get_success_url(self, **kwargs):
		return reverse_lazy('vchapter', kwargs = {'manga_name': self.manga, 'volume_n_vol':self.get_volume().n_vol})

	def get_manga(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return self.manga

	def get_volume(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		return self.volume

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.kwargs["manga_name"], n_chap=self.kwargs["chapter_n_chap"])
		return Chapter.objects.filter(volume__manga__name=self.manga, n_chap=self.chapter.get_chap())

	def get_context_data(self, **kwargs):
		context = super(DeleteView, self).get_context_data(**kwargs)
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		self.chapter = Chapter.objects.get(volume__manga__name=self.manga, n_chap=self.kwargs["chapter_n_chap"])
		context['manga'] = self.manga
		context['volume'] = self.volume
		context['chapter'] = self.chapter
		return context

# No genericas

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

@login_required(login_url='/accounts/login/')
def script(request, manga_name, chapter_n_chap):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter = Chapter.objects.get(volume__manga__name=manga_name, n_chap=chapter_n_chap)
	context = {'manga': manga, "chapter": chapter}
	return render(request, 'mangascripts/script.html', context)

@login_required(login_url='/accounts/login/')
def vscript(request, manga_name, chapter_n_chap, volume_n_vol):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter = Chapter.objects.get(volume__manga__name=manga_name, n_chap=chapter_n_chap)
	volume = Volume.objects.get(manga__name=manga_name, n_vol=volume_n_vol)
	context = {'manga': manga, 'volume': volume, "chapter": chapter,}
	return render(request, 'mangascripts/script.html', context)

#def manga_fav(request):
	#manga_list = Manga.objects.filter(favorite=True).order_by('name')
	#context = {'object_list': manga_list, 'favorite':True}
	#return render(request, 'mangascripts/manga_list.html', context)

#def volume_fav(request, manga_name):
	#manga = get_object_or_404(Manga, name=manga_name)
	#volume_list = Volume.objects.filter(manga=manga.pk, favorite=True).order_by('n_vol')
	#context = {'manga': manga, 'object_list': volume_list, 'favorite':True}
	#return render(request, 'mangascripts/volume_list.html', context)

#def chapter_fav(request, manga_name):
	#manga = get_object_or_404(Manga, name=manga_name)
	#chapter_list = Chapter.objects.filter(volume__manga__name=manga_name, favorite=True).order_by('n_chap')
	#context = {'manga': manga, 'object_list': chapter_list, 'favorite':True}
	#return render(request, 'mangascripts/chapter_list.html', context)

def login(request):
	pass

def logout_view(request):
	logout(request)
	return redirect('/')
