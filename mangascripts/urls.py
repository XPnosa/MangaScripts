from django.conf.urls import url
from mangascripts.views import MangaListView, VolumeListView, ChapterListView, VChapterListView
from mangascripts.views import MangaNew, VolumeNew, ChapterNew
from mangascripts.views import MangaUpdate, VolumeUpdate, ChapterUpdate
from mangascripts.views import MangaDel, VolumeDel, ChapterDel

from . import views

urlpatterns = [
	# Genericas
	# List
	url(r'^$', MangaListView.as_view(), name='manga'), 
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volumes$', VolumeListView.as_view(), name='volume'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapters$', ChapterListView.as_view(), name='chapter'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapters$', VChapterListView.as_view(), name='vchapter'),
	# Insert
	url(r'^new-manga$', MangaNew.as_view(), name='manga-new'), 
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/new-volume$', VolumeNew.as_view(), name='volume-new'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/new-chapter$', ChapterNew.as_view(), name='chapter-new'), 
	# Update
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/edit=(?P<pk>[0-9]+)$', MangaUpdate.as_view(), name='manga-edit'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/edit=(?P<pk>[0-9]+)$', VolumeUpdate.as_view(), name='volume-edit'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/edit=(?P<pk>[0-9]+)$', ChapterUpdate.as_view(), name='chapter-edit'),
	# Delete
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/del=(?P<pk>[0-9]+)$', MangaDel.as_view(), name='manga-del'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/del=(?P<pk>[0-9]+)$', VolumeDel.as_view(), name='volume-del'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/del=(?P<pk>[0-9]+)$', ChapterDel.as_view(), name='chapter-del'),

	# No genericas
	# url(r'^$', views.index, name='index'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volumes$', views.volume, name='volume'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapters$', views.chapter, name='chapter'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapters$', views.vchapter, name='vchapter'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script$', views.script, name='script'),
	url(r'^favorites-manga$', views.manga_fav, name='manga_fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/favorites-volumes$', views.volume_fav, name='volume_fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/favorites-chapters$', views.chapter_fav, name='chapter_fav'),
]
