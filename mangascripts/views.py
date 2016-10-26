from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.

from .models import Manga, Volume, Chapter, User
from .models import Manga_fav, Volume_fav, Chapter_fav, Chapter_read

# Genericas
# Listas

class MangaListView(ListView): 
	model = Manga
	paginate_by = 10

	def get_fav_mangas(self):
		if self.request.user.is_authenticated:
			fav_list = Manga_fav.objects.filter(user=self.request.user)
		else:
			fav_list = {}
		return fav_list

	def get_context_data(self, **kwargs):
		context = super(MangaListView, self).get_context_data(**kwargs)
		obj_list = self.get_fav_mangas()
		context['fav'] = []
		for obj in obj_list:
			context['fav'].append(obj.manga.pk)
		return context

class VolumeListView(ListView): 
	model = Volume
	paginate_by = 10

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Volume.objects.filter(manga=self.manga)

	def get_fav_volumes(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		if self.request.user.is_authenticated:
			fav_list = Volume_fav.objects.filter(volume__manga__name=self.manga, user=self.request.user)
		else:
			fav_list = {}
		return fav_list

	def get_context_data(self, **kwargs):
		context = super(VolumeListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		obj_list = self.get_fav_volumes()
		context['fav'] = []
		for obj in obj_list:
			context['fav'].append(obj.volume.pk)
		return context

class ChapterListView(ListView): 
	model = Chapter
	paginate_by = 10

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Chapter.objects.filter(volume__manga__name=self.manga)

	def get_fav_chapters(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		if self.request.user.is_authenticated:
			fav_list = Chapter_fav.objects.filter(chapter__volume__manga__name=self.manga, user=self.request.user)
		else:
			fav_list = {}
		return fav_list

	def get_read_chapters(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		if self.request.user.is_authenticated:
			read_list = Chapter_read.objects.filter(chapter__volume__manga__name=self.manga, user=self.request.user)
		else:
			read_list = {}
		return read_list

	def get_context_data(self, **kwargs):
		context = super(ChapterListView, self).get_context_data(**kwargs)
		context['manga'] = self.manga
		context['volumeless'] = True
		obj_list = self.get_read_chapters()
		context['read'] = []
		for obj in obj_list:
			context['read'].append(obj.chapter.pk)
		obj_list = self.get_fav_chapters()
		context['fav'] = []
		for obj in obj_list:
			context['fav'].append(obj.chapter.pk)
		return context

class VChapterListView(ListView): 
	model = Chapter
	paginate_by = 10

	def get_queryset(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		return Chapter.objects.filter(volume__manga__name=self.manga, volume__n_vol=self.kwargs["volume_n_vol"])

	def get_fav_chapters(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		if self.request.user.is_authenticated:
			fav_list = Chapter_fav.objects.filter(chapter__volume__manga__name=self.manga, user=self.request.user)
		else:
			fav_list = {}
		return fav_list

	def get_read_chapters(self):
		self.manga = get_object_or_404(Manga, name=self.kwargs["manga_name"])
		if self.request.user.is_authenticated:
			read_list = Chapter_read.objects.filter(chapter__volume__manga__name=self.manga, user=self.request.user)
		else:
			read_list = {}
		return read_list

	def get_context_data(self, **kwargs):
		context = super(VChapterListView, self).get_context_data(**kwargs)
		self.volume = Volume.objects.get(manga=self.manga, n_vol=self.kwargs["volume_n_vol"])
		context['manga'] = self.manga
		context['volume'] = self.volume
		obj_list = self.get_read_chapters()
		context['read'] = []
		for obj in obj_list:
			context['read'].append(obj.chapter.pk)
		obj_list = self.get_fav_chapters()
		context['fav'] = []
		for obj in obj_list:
			context['fav'].append(obj.chapter.pk)
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
		return reverse_lazy('chapter', kwargs = {'manga_name': self.manga.name})

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

# Script

@login_required(login_url='/accounts/login/')
def script(request, manga_name, chapter_n_chap):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter = Chapter.objects.get(volume__manga__name=manga_name, n_chap=chapter_n_chap)
	obj_list = Chapter_read.objects.filter(chapter__volume__manga__name=manga, user=request.user)
	read_chapters = []
	for obj in obj_list:
		read_chapters.append(obj.chapter.pk)
	obj_list = Chapter_fav.objects.filter(chapter__volume__manga__name=manga, user=request.user)
	fav_chapters = []
	for obj in obj_list:
		fav_chapters.append(obj.chapter.pk)
	context = {'manga': manga, "chapter": chapter, 'read':read_chapters, 'fav':fav_chapters}
	return render(request, 'mangascripts/script.html', context)

@login_required(login_url='/accounts/login/')
def vscript(request, manga_name, chapter_n_chap, volume_n_vol):
	manga = get_object_or_404(Manga, name=manga_name)
	chapter = Chapter.objects.get(volume__manga__name=manga_name, n_chap=chapter_n_chap)
	volume = Volume.objects.get(manga__name=manga_name, n_vol=volume_n_vol)
	obj_list = Chapter_read.objects.filter(chapter__volume__manga__name=manga, user=request.user)
	read_chapters = []
	for obj in obj_list:
		read_chapters.append(obj.chapter.pk)
	obj_list = Chapter_fav.objects.filter(chapter__volume__manga__name=manga, user=request.user)
	fav_chapters = []
	for obj in obj_list:
		fav_chapters.append(obj.chapter.pk)
	context = {'manga': manga, 'volume': volume, "chapter": chapter, 'read':read_chapters, 'fav':fav_chapters}
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

# Favs

def manga_fav(request, manga_name, manga_pk, page):
	url = "/mangascripts?page="+str(page)
	m = Manga.objects.get(pk=manga_pk)
	try:
		mf = Manga_fav(user=request.user, manga=m)
		mf.save()
	except:
		pass
	return redirect(url)

def manga_unfav(request, manga_name, manga_pk, page):
	url = "/mangascripts?page="+str(page)
	m = Manga.objects.get(pk=manga_pk)
	try:
		mf = Manga_fav.objects.get(user=request.user, manga=m)
		mf.delete()
	except:
		pass
	return redirect(url)

def volume_fav(request, manga_name, volume_n_vol, volume_pk, page):
	url = "/mangascripts/"+manga_name+"/volumes?page="+str(page)
	v = Volume.objects.get(pk=volume_pk)
	try:
		vf = Volume_fav(user=request.user, volume=v)
		vf.save()
	except:
		pass
	return redirect(url)

def volume_unfav(request, manga_name, volume_n_vol, volume_pk, page):
	url = "/mangascripts/"+manga_name+"/volumes?page="+str(page)
	v = Volume.objects.get(pk=volume_pk)
	try:
		vf = Volume_fav.objects.get(user=request.user, volume=v)
		vf.delete()
	except:
		pass
	return redirect(url)

def chapter_fav(request, manga_name, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav(user=request.user, chapter=c)
		cf.save()
	except:
		pass
	return redirect(url)

def chapter_unfav(request, manga_name, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav.objects.get(user=request.user, chapter=c)
		cf.delete()
	except:
		pass
	return redirect(url)

def vchapter_fav(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav(user=request.user, chapter=c)
		cf.save()
	except:
		pass
	return redirect(url)

def vchapter_unfav(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav.objects.get(user=request.user, chapter=c)
		cf.delete()
	except:
		pass
	return redirect(url)

def script_fav(request, manga_name, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav(user=request.user, chapter=c)
		cf.save()
	except:
		pass
	return redirect(url)

def script_unfav(request, manga_name, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav.objects.get(user=request.user, chapter=c)
		cf.delete()
	except:
		pass
	return redirect(url)

def vscript_fav(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav(user=request.user, chapter=c)
		cf.save()
	except:
		pass
	return redirect(url)

def vscript_unfav(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cf = Chapter_fav.objects.get(user=request.user, chapter=c)
		cf.delete()
	except:
		pass
	return redirect(url)

# Read

def chapter_read(request, manga_name, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read(user=request.user, chapter=c)
		cr.save()
	except:
		pass
	return redirect(url)

def chapter_unread(request, manga_name, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read.objects.get(user=request.user, chapter=c)
		cr.delete()
	except:
		pass
	return redirect(url)

def vchapter_read(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read(user=request.user, chapter=c)
		cr.save()
	except:
		pass
	return redirect(url)

def vchapter_unread(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk, page):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapters?page="+str(page)
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read.objects.get(user=request.user, chapter=c)
		cr.delete()
	except:
		pass
	return redirect(url)

def script_read(request, manga_name, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read(user=request.user, chapter=c)
		cr.save()
	except:
		pass
	return redirect(url)

def script_unread(request, manga_name, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read.objects.get(user=request.user, chapter=c)
		cr.delete()
	except:
		pass
	return redirect(url)

def vscript_read(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read(user=request.user, chapter=c)
		cr.save()
	except:
		pass
	return redirect(url)

def vscript_unread(request, manga_name, volume_n_vol, chapter_n_chap, chapter_pk):
	url = "/mangascripts/"+manga_name+"/volume-"+volume_n_vol+"/chapter-"+chapter_n_chap+"/script"
	c = Chapter.objects.get(pk=chapter_pk)
	try:
		cr = Chapter_read.objects.get(user=request.user, chapter=c)
		cr.delete()
	except:
		pass
	return redirect(url)

# Auth

def login(request):
	pass

def logout_view(request):
	logout(request)
	return redirect('/mangascripts/logout_redirect')

def logoutr(request):
	return render(request, 'mangascripts/logout.html')
