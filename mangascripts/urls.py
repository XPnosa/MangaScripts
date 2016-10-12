from django.conf.urls import url
from mangascripts.views import MangaListView, VolumeListView, ChapterListView, VChapterListView

from . import views

urlpatterns = [
	# Genericas
	url(r'^$', MangaListView.as_view()),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volumes$', VolumeListView.as_view(), name='volume'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapters$', ChapterListView.as_view(), name='chapter'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapters$', VChapterListView.as_view(), name='vchapter'),

	# No genericas
	# url(r'^$', views.index, name='index'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volumes$', views.volume, name='volume'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapters$', views.chapter, name='chapter'),
	# url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/volume-(?P<volume_n_vol>[0-9]+)/chapters$', views.vchapter, name='vchapter'),
	url(r'^(?P<manga_name>[a-zA-Z0-9 ]+)/chapter-(?P<chapter_n_chap>[0-9]+)/script/$', views.script, name='script'),
]
