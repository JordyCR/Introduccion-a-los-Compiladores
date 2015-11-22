# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import os, json, types, sys, codecs
from urlparse import urlparse
import re
import string

import collections



# { pagina : contenido<body> }
cdatos = {}

# { palabra : documento }
diccionario = {}



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

			page = page.read()
			soup = BeautifulSoup(page, "html5lib")	
		except Exception:
			ap += 1
			continue


		# Es un link válido, así que lo procesamos

		# Parseamos todo el HTML
		# page = page.read()
		# soup = BeautifulSoup(page, "html5lib")


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
			cbody = soup.body
			try:
				cbody = str(cbody)	
			except Exception:
				ap += 1
				continue
			
			cbody = reg.sub('', cbody).strip()

			cbody = cbody.lower().translate(string.maketrans(" "," "), string.punctuation)
			cbody = ' '.join(cbody.split()) # Eliminamos múltiples espacios

			cdatos[actual] = cbody



		# print "Repetidos:", [item for item, count in collections.Counter(visitados).items() if count > 1]

		## TODO -> Prueba: dejamos de añadir despues de cierto límite
		# if len(visitados) > 30000:
		# 	ap += 1
		# 	continue

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


	# Finalizó el scraping y la recolección de bodys. Se guarda un json
	rb = codecs.open('./readable-buap.json', 'w', "utf-8-sig")
	rb.write(json.dumps(cdatos, indent=4, ensure_ascii=False, encoding='utf8'))
	rb.close()

	b = open('./buap.json', 'w')
	b.write(json.dumps(cdatos, indent=4))
	b.close()



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
			if esDocumentoUtil(nn) and nn not in v: # ...Y si el url no ha sido visitado
				v.append(nn)


		# Relativo a directorio
		elif 'buap' in actual.lower() and not esRedSocial(actual.lower()):
			elem = os.path.join(actual, elem)
			if esDocumentoUtil(elem) and elem not in v: # ...Y si el url no ha sido visitado
				v.append(elem)

	
	else: # Es absoluto
		if 'buap' in elem.lower() and not esRedSocial(elem.lower()):
			if esDocumentoUtil(elem) and elem not in v: # ...Y si el url no ha sido visitado
				v.append(elem)


def esDocumentoUtil(url):
	return 'javascript:' not in url and not '.pdf' in url and not '.jpg' in url and not '.doc' in url and not '.pps' in url and not '.rar' in url and not '.zip' in url and not '.eps' in url


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
	buap_to_diccionario()
	consultas()


def consultas():
	while True:
		op = raw_input("\nIntroduce tu busqueda:\n>>> ")
		op = op.translate(string.maketrans("",""), string.punctuation)

		busq = op.split()

		# Un solo elemento
		if len(busq) == 1:
			# op = lemma(op.decode('utf-8'))

			if op in diccionario:
				for res in diccionario[op]:
					print res
				print
				print ">>> Resultados:" , len(diccionario[op]), "<<<\n"
			else:
				print ">>> No hubo resultados para esta búsqueda <<<\n"

		# Mas de un elemento
		elif len(busq) > 1:
			tipo = raw_input("\nQue tipo de busqueda desea realizar:\n" + 
							"A) AND\n" + 
							"B) OR\n" + 
							"C) RESTA\n" + 
							">>> ").lower()

			conjb = []
			for i in xrange(len(busq)):
				r = set() if busq[i] not in diccionario else diccionario[busq[i]]
				conjb.append(r)

			resultado = conjb[0]

			for i in range(1, len(busq)):
				if tipo == 'a':
					resultado = resultado & conjb[i]
				elif tipo == 'b':
					resultado = resultado | conjb[i]
				elif tipo == 'c':
					resultado = resultado - conjb[i]


			# Mostramos los resultados
			for res in resultado:
				print res
			print
			print ">>> Resultados:" , len(resultado), "<<<\n"



def buap_to_diccionario():
	for pag in cdatos.keys():
		# Conseguimos el contenido de cada pag, pasamos a minusculas
		t = cdatos[pag]

		pals = t.split()

		for p in pals:
			if not p in diccionario:
				diccionario[p] = set()
			diccionario[p].add(pag)

	# Mostramos resultados
	# for k in diccionario.keys()[10:30]:
	# 	print "PALABRA:", k, "\t"
	# 	for e in diccionario[k]:
	# 		print "\t", e
	# 	print "\n"


if __name__ == '__main__':
	if raw_input('\n¿Desea realizar el proceso de indexado ahora? Se usará un archivo de una indexación previa (si la hay) si no desea indexar ahora\n>>> ') == 's':
		scraping_buap()

	if raw_input('\n¿Desea realizar una consulta?\n>>> ') == 's':
		try:
			cdatos = json.loads(open('./buap.json').read().decode("utf-8-sig"))	
		except Exception:
		 	scraping_buap()

		# if len(cdatos.keys()) == 0:
		# 	print "\nNo hay indexación previa, espere mientras se realiza"
		# 	scraping_buap()



		indexa_buap()



