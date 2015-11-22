# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import os, json, types
from urlparse import urlparse
import re

import collections




cdatos = {}



def scraping_buap():
	urlbase = u"http://www.buap.mx"

	# Conjunto con todas las URL's visitadas
	visitados = [urlbase]
	ap = 0

	# global cdatos = {}


	# Un while para el recorrido a lo ancho
	# Este es el ciclo que indexa toda la buap
	while ap < len(visitados):
		print "\n",len(visitados)
		actual = visitados[ap]
		print ap, actual


		# Simulamos un navegador
		request = urllib2.Request(actual, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
		
		# Efectuamos el Query
		try:
			page = urllib2.urlopen(request, timeout=4) # 4 Segundos para recibir respuesta del server	
		except Exception:
			ap += 1
			continue


		# Es un link válido, así que lo procesamos

		# Parseamos todo el HTML
		soup = BeautifulSoup(page.read(), "html5lib")


		# Si el body es vacío no nos sirve en el diccionario, así que validamos
		if type(soup.body) != types.NoneType:
			
			# Procesamos body
			to_extract = soup.find_all('script')
			for item in to_extract:
				item.extract()

			to_extract = soup.find_all('noscript')
			for item in to_extract:
				item.extract()

			to_extract = soup.find_all('style')
			for item in to_extract:
				item.extract()

			# Eliminar tags internos de body
			reg = re.compile(r'<[^>]+>')
			
			# Lo introducimos en nuestro conjunto de datos
			cbody = str(soup.body)
			cbody = reg.sub('', cbody).strip()

			cdatos[actual] = ' '.join(cbody.split()) # Eliminamos múltiples espacios y se añade



		print "Repetidos:", [item for item, count in collections.Counter(visitados).items() if count > 1]

		## TODO -> Prueba: dejamos de añadir despues de cierto límite
		if len(visitados) > 20:
			ap += 1
			continue

		# Frames
		for frame in soup.find_all("frame"):
			try:
				aniadirSiguiente( frame['src'] , actual , visitados )	
			except Exception:
				continue
			

		# iFrames
		for frame in soup.find_all("iframe"):
			try:
				aniadirSiguiente( frame['src'] , actual , visitados)				
			except Exception:
				continue


		# <a>
		for link in soup.find_all('a'):
			try:
				aniadirSiguiente( link['href'] , actual , visitados)
			except Exception:
				continue
				

		ap += 1


	# Finalizó el scraping y la recolección de bodys
	open('buap.json', 'w').write(json.dumps(cdatos, indent=4))


def aniadirSiguiente(elem, actual, v):
	if not esAbsoluto(elem): # Es Relativo

		# Es autoreferenciado a la misma página
		if elem[0] == '#':
			# no nos sirve
			return

		elif elem[0] == '/': # Relativo a raiz
			# Necesitamos extraer el dominio principal de cada url
			parsed_uri = urlparse( actual )
			dom = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
			nn = os.path.join(dom, elem[1:])
			if nn not in v and 'javascript:' not in nn and not nn.endswith('.pdf'):
				v.append(nn)


		# Relativo a directorio
		elif 'buap' in actual.lower() and not esRedSocial(actual.lower()):
			elem = os.path.join(actual, elem)
			if elem not in v and 'javascript:' not in elem and not elem.endswith('.pdf'):
				v.append(elem)

	
	else: # Es absoluto
		if 'buap' in elem.lower() and not esRedSocial(elem.lower()):
			if elem not in v and 'javascript:' not in elem and not elem.endswith('.pdf'):
				v.append(elem)


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



def indexa_buap():
	print "\n\n"
	for pag in cdatos.keys():
		print pag


if __name__ == '__main__':
	if raw_input('\n¿Desea realizar el proceso de indexado ahora? Se usará un archivo de una indexación previa (si la hay) si no desea indexar ahora\n>>> ') == 's':
		scraping_buap()
	else:
		try:
			cdatos = json.loads(open('./buap.json').read())	
		except Exception:
			print "Fichero no encontrado, se procede a indexar"
			scraping_buap()
		if len(cdatos.keys()) == 0:
			print "Fichero vacío o corrupto, se procede a indexar"
			scraping_buap()
		
	indexa_buap()



