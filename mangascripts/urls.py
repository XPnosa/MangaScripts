from django.conf.urls import url
from mangascripts.views import MangaListView, VolumeListView, ChapterListView, VChapterListView
from mangascripts.views import MangaAdd, VolumeAdd, ChapterAdd, VChapterAdd
from mangascripts.views import MangaUpdate, VolumeUpdate, ChapterUpdate, VChapterUpdate
from mangascripts.views import MangaDelete, VolumeDelete, ChapterDelete, VChapterDelete
from mangascripts.views import UserDetailView, UserUpdate, InfoUpdate
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views

urlpatterns = [
	# Genericas
	# List
	url(r'^$', MangaListView.as_view(), name='manga'), 
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volumes$', VolumeListView.as_view(), name='volume'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapters$', ChapterListView.as_view(), name='chapter'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapters$', VChapterListView.as_view(), name='vchapter'),
	# Insert
	url(r'^new-manga$', MangaAdd.as_view(), name='manga-new'), 
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/new-volume$', VolumeAdd.as_view(), name='volume-new'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/new-chapter$', ChapterAdd.as_view(), name='chapter-new'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/new-chapter$', VChapterAdd.as_view(), name='vchapter-new'), 
	# Update
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/edit=(?P<pk>[0-9]+)$', MangaUpdate.as_view(), name='manga-edit'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/edit=(?P<pk>[0-9]+)$', VolumeUpdate.as_view(), name='volume-edit'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/edit=(?P<pk>[0-9]+)$', ChapterUpdate.as_view(), name='chapter-edit'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/edit=(?P<pk>[0-9]+)$', VChapterUpdate.as_view(), name='vchapter-edit'),
	# Delete
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/del=(?P<pk>[0-9]+)$', MangaDelete.as_view(), name='manga-del'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/del=(?P<pk>[0-9]+)$', VolumeDelete.as_view(), name='volume-del'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/del=(?P<pk>[0-9]+)$', ChapterDelete.as_view(), name='chapter-del'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/del=(?P<pk>[0-9]+)$', VChapterDelete.as_view(), name='vchapter-del'),
	# Filter
	url(r'^favorites-mangas$', MangaListView.as_view(), name='favorites-mangas'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/favorites-volumes$', VolumeListView.as_view(), name='favorites-volumes'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/favorites-chapters$', ChapterListView.as_view(), name='favorites-chapters'),
	# User
	url(r'^user-details/user=(?P<pk>[0-9]+)$', UserDetailView.as_view(), name='user-details'),
	url(r'^user-edit/user=(?P<pk>[0-9]+)$', UserUpdate.as_view(), name='user-edit'),
	url(r'^info-edit/user=(?P<pk>[0-9]+)$', InfoUpdate.as_view(), name='info-edit'),
	url(r'^password/$', views.change_password, name='change_password'),

	# No genericas
	# url(r'^$', views.index, name='index'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volumes$', views.volume, name='volume'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapters$', views.chapter, name='chapter'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapters$', views.vchapter, name='vchapter'),
	# Favs
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/fav=(?P<manga_pk>[0-9]+)?page=(?P<page>[0-9]+)/(?P<favorites>(True|False))$', views.manga_fav, name='manga-fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/unfav=(?P<manga_pk>[0-9]+)?page=(?P<page>[0-9]+)/(?P<favorites>(True|False))$', views.manga_unfav, name='manga-unfav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/fav=(?P<volume_pk>[0-9]+)?page=(?P<page>[0-9]+)/(?P<favorites>(True|False))$', views.volume_fav, name='volume-fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/unfav=(?P<volume_pk>[0-9]+)?page=(?P<page>[0-9]+)/(?P<favorites>(True|False))$', views.volume_unfav, name='volume-unfav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/fav=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)/(?P<favorites>(True|False))$', views.chapter_fav, name='chapter-fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/unfav=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)/(?P<favorites>(True|False))$', views.chapter_unfav, name='chapter-unfav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/fav=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)$', views.vchapter_fav, name='vchapter-fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/unfav=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)$', views.vchapter_unfav, name='vchapter-unfav'),
	# Read
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/read=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)$', views.chapter_read, name='chapter-read'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/unread=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)$', views.chapter_unread, name='chapter-unread'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/read=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)$', views.vchapter_read, name='vchapter-read'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/unread=(?P<chapter_pk>[0-9]+)?page=(?P<page>[0-9]+)$', views.vchapter_unread, name='vchapter-unread'),
	# Script
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script$', views.script, name='script'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/fav=(?P<chapter_pk>[0-9]+)$', views.script_fav, name='script-fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/unfav=(?P<chapter_pk>[0-9]+)$', views.script_unfav, name='script-unfav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/read=(?P<chapter_pk>[0-9]+)$', views.script_read, name='script-read'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/unread=(?P<chapter_pk>[0-9]+)$', views.script_unread, name='script-unread'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script$', views.vscript, name='vscript'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/fav=(?P<chapter_pk>[0-9]+)$', views.vscript_fav, name='vscript-fav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/unfav=(?P<chapter_pk>[0-9]+)$', views.vscript_unfav, name='vscript-unfav'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/read=(?P<chapter_pk>[0-9]+)$', views.vscript_read, name='vscript-read'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/unread=(?P<chapter_pk>[0-9]+)$', views.vscript_unread, name='vscript-unread'),
	# Auth
	url(r'^accounts/login/$', views.login, name='login'),
	url(r'^logout$', views.logout_view, name='logout_view'),
	url(r'^logout_redirect$', views.logoutr, name='logoutr'),
	url(r'^register$', views.register, name='register'),
	url(r'^register_redirect$', views.register_redirect, name='register_redirect'),
	url(r'^password_redirect$', views.password_redirect, name='password_redirect'),
]
