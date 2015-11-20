# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import os
from urlparse import urlparse


def indexar_buap():
	urlbase = u"http://www.buap.mx"
	# urlbase = "http://cmas.siu.buap.mx/portal_pprd/wb/BBUAP/inicio"


	# Conjunto con todas las URL's visitadas
	# visitados = set()
	# visitados.add(urlbase)
	visitados = [urlbase]
	ap = 0

	# Siguientes. URL's que se visitaran
	# siguientes = [urlbase]


	# Un while para el recorrido a lo ancho
	# Este es el ciclo que indexa toda la buap
	while ap < len(visitados):
		print len(visitados)
	 	actual = visitados[ap]
	 	
	 	# if actual in visitados:
	 	# 	continue

		# Simulamos un navegador
		request = urllib2.Request(actual, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
		
		# Efectuamos el Query
		try:
			page = urllib2.urlopen(request)	
		except Exception:
			continue


		# Es un link válido, así que lo procesamos
		

		#visitados.add(actual)
		
		# Parseamos todo el HTML
		soup = BeautifulSoup(page.read(), "html5lib")


		# Frames
		for frame in soup.find_all("frame"):
			aniadirSiguiente( frame['src'] , actual , visitados )
			

		# iFrames
		for frame in soup.find_all("iframe"):
			aniadirSiguiente( frame['src'] , actual , visitados)


		# <a>
		for link in soup.find_all('a'):
			aniadirSiguiente( link['href'] , actual , visitados)

		ap += 1


	# print "\n\n"
	# siguientes = set(siguientes)
	# for s in siguientes:
	# 	print s
	# print len(siguientes)


def aniadirSiguiente(elem, actual, v):
	if not esAbsoluto(elem): # Es Relativo

		if elem[0] == '/': # Relativo a raiz
			# Necesitamos extraer el dominio principal de cada url
			parsed_uri = urlparse( actual )
			dom = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			nn = os.path.join(dom, elem[1:])
			if nn not in v:
				v.append(nn)
			else:
				print "Repetido:", nn


		# Relativo a directorio
		elif 'buap' in actual.lower() and not esRedSocial(actual.lower()):
			elem = os.path.join(actual, elem)
			if elem not in v:
				v.append(elem)
			else:
				print "Repetido:", elem

	
	else: # Es absoluto
		if 'buap' in elem.lower() and not esRedSocial(elem.lower()):
			if elem not in v:
				v.append(elem)
			else:
				print "Repetido:", elem


def esRedSocial(url):
	'''
	String -> Bool
	'''
	return "facebook" in url or "twitter" in url or "google" in url or "youtube" in url


def esAbsoluto(url):
	'''
	String -> Bool
	'''
	return "http://" in url or "https://" in url or "www." in url


if __name__ == '__main__':
	indexar_buap()
