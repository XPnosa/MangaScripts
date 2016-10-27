#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from mangascripts.models import Manga, Volume, Chapter
import requests, random, bs4, time, sys, re

# Constantes
TAG_RE = re.compile(r'<[^>]+>')
AUX_RE = re.compile(r'ngd[^>]+o')
NOT_AVAILABLE = "No disponible"

try:
	SCRAP_USER = User.objects.get(username='scrap')
except:
	sc_user = User(username='scrap', password='pasword.'+str(random.randint(1000000,9999999)))
	sc_user.save()
	SCRAP_USER = sc_user

# Variables
debug = False

# Funciones
def remove_tags(text):
	return TAG_RE.sub('', text)

def remove_aux(text):
	return AUX_RE.sub('', text)

# Clases
class ScrapOP:
	'''Clase Scrap para One Piece'''
	def __init__(self):
		self.__manga = "One Piece"
		self.__author = "Eiicriro Oda"
		self.__volumes = []
		self.__chapters = []
		self.__first = True
		self.__dbObj = self.__set_manga()
		self.__get_volumes_and_chapters()
		self.__get_scripts()
		self.__update_db()

	# Crear o recuperar el objeto de base de datos Manga.
	def __set_manga(self):
		try:
			m = Manga.objects.get(name=self.__manga)
			self.__first = False
		except:
			m = Manga(name=self.__manga, author=self.__author, user=SCRAP_USER)
			m.save()
		finally: 
			return m

	# Obtener la lista de volumenes y capitulos de la Web
	def __get_volumes_and_chapters(self):
		url = "http://es.onepiece.wikia.com/wiki/Volúmenes_y_Capítulos_de_One_Piece/Lista_de_Cap%C3%ADtulos"
		res = requests.get(url)
		if ("200" in str(res)):
			soup = bs4.BeautifulSoup(res.text, "lxml")
			elems = soup.select('.wikitable > tr > td')
			for ele in elems:
				e = str(ele)
				strVol = "Volumen "
				srtChp = 'title="Cap'
				if e.find(strVol) >= 0:
					n_vol = e[e.find(strVol)+len(strVol):e.find('</b>')]
					if len(n_vol) <= 4:
						n_vol = int(n_vol)
						name_vol = remove_tags(e[e.find(' "')+2:e.find('"',e.find(' "')+2)]).strip(" '") 
						self.__volumes.append({"n_vol":n_vol, "title":name_vol, "manga":self.__manga})
				sub_e = e
				while sub_e.find(srtChp) >= 0:
					ini = sub_e.find(srtChp)+len(srtChp)+7
					n_chp = sub_e[ini:sub_e.find('">',ini)]
					sub_e = sub_e[sub_e.find('">',ini):]
					name_chp = remove_tags(sub_e[2:sub_e.find('</a>')]).strip(" '") 
					self.__chapters.append({"n_chp":n_chp, "title":name_chp, "volume":n_vol, "script":NOT_AVAILABLE})

	# Obtener la lista de scripts de traducción de la web
	def __get_scripts(self):
		print "\033[1m\nRaspado de scripts:\n\033[0m"
		for c in self.__chapters:
			new = False
			page = c["n_chp"]
			try:
				aux = Chapter.objects.get(volume__manga__name=self.__manga, n_chap=int(page))
				sc = aux.script
				if sc == NOT_AVAILABLE:
					new = True
			except:
				new = True
			finally:
				if new:
					url = "http://pirateking.es/esp_scripts_f"+str(page)+".html"
					res = requests.get(url)
					if ("200" in str(res)):
						soup = bs4.BeautifulSoup(res.text, "lxml")
						elems = soup.select('.script-contenido')
						if len(elems) == 1:
							self.__chapters[int(page)]["script"] = remove_aux(str(elems[0].encode('ISO-8859-1')))
							print "\033[1m"+str(page)+": "+self.__chapters[int(page)]["title"]+" → "+str(len(elems[0].encode('ISO-8859-1')))+" caracteres\033[0m"
						else:
							print "\033[1m\033[33m"+str(page)+": "+self.__chapters[int(page)]["title"]+" → No disponible\033[0m"
						time.sleep(1)

	# Actualizar la base de datos con la información obtenida en la Web
	def __update_db(self):
		print "\033[1m\nActualización de la base de datos:\n\033[0m"
		try:
			if self.__first:
				print "\033[1m\033[32mManga → ("+self.__manga+", "+self.__author+")\033[0m"
			else:
				print "\033[1m\033[31mManga → ("+self.__manga+", "+self.__author+")\033[0m"
			for vol in self.__volumes:
				try:
					self.__dbObj.volume_set.create(n_vol=vol['n_vol'], title=vol['title'], user=SCRAP_USER)
					print "\033[1m\033[32mVolume → ("+self.__manga+", "+str(vol['n_vol'])+", "+vol['title']+")\033[0m"
				except:
					print "\033[1m\033[31mVolume → ("+self.__manga+", "+str(vol['n_vol'])+", "+vol['title']+")\033[0m"
					if debug:
						raise
			m = Manga.objects.get(name=self.__manga)
			for chap in self.__chapters:
				try:
					v = Volume.objects.get(manga__name=self.__manga, n_vol=chap["volume"])
					try:
						if chap["script"] == NOT_AVAILABLE:
							v.chapter_set.create(manga=m, n_chap=chap["n_chp"], title=chap["title"], script=chap["script"], translated=False, user=SCRAP_USER)
						else:
							v.chapter_set.create(manga=m, n_chap=chap["n_chp"], title=chap["title"], script=chap["script"], translated=True, user=SCRAP_USER)
					except:
						c = Chapter.objects.get(volume__manga__name=self.__manga, n_chap=chap["n_chp"])
						if not c.protected and c.script == NOT_AVAILABLE and chap["script"] != NOT_AVAILABLE:
							c.delete()
							v.chapter_set.create(manga=m, n_chap=chap["n_chp"], title=chap["title"], script=chap["script"], translated=True, user=SCRAP_USER)
						else:
							raise
					print "\033[1m\033[32mChapter → ("+str(m)+", "+str(chap["volume"])+", "+str(chap['n_chp'])+", "+chap['title']+", "+str(len(chap["script"]))+" characters)\033[0m"
				except:
					print "\033[1m\033[31mChapter → ("+str(m)+", "+str(chap["volume"])+", "+str(chap['n_chp'])+", "+chap['title']+", 0 characters)\033[0m"
					if debug:
						raise
		except:
			print "\033[1m\033[31m\nOcurrio un error inesperado.\n\033[0m"
			if debug:
				raise
		finally:
			print "\033[1m\nLa base de datos ha sido actualizada.\n\033[0m"

#Comando
class Command(BaseCommand):
	help = 'Busca y puebla con scripts de traducción la base de datos de mangas'

	def add_arguments(self, parser):
		parser.add_argument('manga', nargs='+', type=str)

	def handle(self, *args, **options):
		for manga in options['manga']:
			if manga == "One Piece":
				ScrapOP()
			else:
				print "\n\033[1m\033[34mEl manga " + manga + " no esta soportado en esta versión\n\033[0m"
