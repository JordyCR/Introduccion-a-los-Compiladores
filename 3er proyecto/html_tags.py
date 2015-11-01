# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("master.html"), "html5lib")

tags = []


# Se hace dos veces el recorrido (se puede evitar, está así por legibilidad)
# El primero para encontrar todos los TAGS
master = soup.find_all(True)
for hijo in master:
    #print hijo.name
    tags.append(hijo.name)

unicos = set(tags)

# print len(unicos)
# print
# for u in unicos:
#     print u

# Pero antes creamos un hash con 'unicos' (será un dict de sets)
ntags = {}
for u in unicos:
	ntags[u] = set()

# El segundo para llenar cada TAG con sus attrs
for hijo in master:
	for llave in hijo.attrs.keys():
		ntags[hijo.name].add(llave)


# Ahora solo lo imprimimos bonito
for llave in ntags.keys():
	print llave
	for att in ntags[llave]:
		print '\t', att
	if len(ntags[llave]) > 0: print