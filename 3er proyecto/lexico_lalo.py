# -*- encoding: utf-8 -*-
import sys

def pick_file():
	'''
	(None) -> StringPath
	Función que abre un dialogo para seleccionar un archivo y devuelve el 
	path del archivo
	NOTA: Si el usuario pulsa "Cancelar", el valor devuelto será cadena vacía ("")
	'''
	from Tkinter import Tk
	from tkFileDialog import askopenfilename

	Tk().withdraw() # no queremos una GUI completa, asi que se oculta el resto de la GUI
	filename = askopenfilename() # Mostramos un Dialogo para abrir ficheros y se regresa el path

	return filename


def limpia_comas(str):
	'''
	String -> String sin comas (',')
	'''
	return str.replace(",", "") # Quitar comas


def open_AFD(path):
	'''
	(StringPath) -> AFD
	'''
	# Abrimos el fichero que contiene el AFD
	fich = open(path, 'r') # Ruta del fichero, solo lectura

	# Empezamos leyendo el alfabeto
	alfabeto = limpia_comas(fich.readline()).split()

	# Definimos los estados
	estados = []
	# Ya no existen estados iniciales (creo)
	#edoini = []
	edosfin = []

	transiciones = []

	# Leemos todos los estados
	linea = fich.readline()
	while linea:
		linea = linea.replace("\n", "")
		tokens = limpia_comas(linea).split()


		# Si nos indica que es un estado final
		if (tokens[-1] != '-'):
			edosfin.append(tokens[0])
		
		estados.append(tokens[0])
		tokens = tokens[1:]

		transiciones.append(tokens)

		# Actualizamos
		linea = fich.readline()

	print "El archivo se ha cargado correctamente"

	# Parece ser una buena idea implementar una tabla hash de tablas hash
	# El modo de acceso será:
	#	transhash[edoactual][letra_de_la_cadena_introducida_actual]
	# Lo comentado anteriormente se verá con mas detalle despues
	# Aca se construirá a partir de lo conseguido antes
	i = 0 
	j = 0
	transhash = {}
	for edo in estados:
		transhash[edo] = {}  # Para cada estado en las transiciones, añadimos su dict/hash asociado a la letra
		for letra in alfabeto:
			transhash[edo][letra] = transiciones[i][j]
			j += 1
		i += 1
		j = 0
	print "Se ha creado la tabla de transiciones con exito"
	print "El alfabeto válido es el siguiente:"
	print alfabeto, "\n"
	
	# return alfabeto, estados, edoini[0], edosfin, transiciones, transhash
	return alfabeto, edosfin, transhash


def validar_cadena(cadena):
	'''
	(str) -> bool
	Se valida si la cadena proporcionada es una palabra valida para el autómata
	'''
	# Abrimos el archivo y creamos nuestras estructuras de datos
	alfabeto, edosfin, transhash = open_AFD("./p3.txt")
	# edoini, edosfin, transhash = open_AFD(pick_file())
	print edosfin
	edoactual = '0'
	char = cadena[0]
	print cadena
	n = len(cadena)
	i = 0
	while (i != n):
		#Tenemos el caso de que exista un espacio, ¿Deberiamos eliminarlo? -Solo si es el primer caracter a evaluar
		if (char == "" and edoactual == '0'):
			i += 1;
			char = cadena[i] 
		print "caracter a evaluar  -->  ", char
		print "Existe en el alfabeto? --->", char in alfabeto
		if (not (char in alfabeto) or char == ' '):
			#return False  # Se dió una cadena que no está dentro del alfabeto valido
			if ('let' in alfabeto):
				if (char.isalpha()):
					edoactual = transhash[edoactual]['let']
					print "letra find -->", edoactual
			elif ('dig' in alfabeto):
				if (char.isdigit()):
					edoactual = transhash[edoactual]['dig']
					print "digit find -->", edoactual
			elif (char == ' ' or char == " "):
				print "Espacio en blanco"
			elif ('otro' in alfabeto): # Nunca entra el espacio en blanco
				print "otro find"
				edoactual = transhash[edoactual]['otro']
				
				if (edoactual in edosfin):
					print "estado final -->", edoactual
					print cadena[0:i], '-->', transhash[edoactual]['token']
					# Hacemos retroceso
					if (transhash[edoactual]['retroceso'] != '-'):
						i -= int(transhash[edoactual]['retroceso']) 
					#Actualizamos estado actual a estado inicial
					edoactual = '0'
					#Actualizamos la cadena eliminando los caracteres leidos
					cadena = cadena[i:]
					#Actualizamos i = 0 tomando en cuenta el aumento que se hace al final del while
					i = -1

			else:
				#Esto quiere decir que hay caracteres invalidos
				print "Caracter invalido --->", char
				return False



		#elif (transhash[edoactual][char] == '-'):
		#	return False  # Se encontró que no es valido y no pertenece al lenguaje aceptado por el automata
		else:	
			edoactual = transhash[edoactual][char]
		i += 1

		print "Valor de i",i, ' Estado actual-->', edoactual

		if (len(cadena) == i):
			#Cuando es el ultimo caracter, nos intentamos mover a un estado final
			edoactual = transhash[edoactual]['otro']
			# ¿Y si no existe un estado 'otro'? Deberia siempre existir
			break
		char = cadena[i]


	if edoactual in edosfin:
		print "Comparacion final"
		print cadena[0:i], '-->', transhash[edoactual]['token']
		return True  # Terminó bien el recorrido y en un estado final

	return False  # Terminó en un estado NO FINAL


def abrir_archivo():
	#Con esta funcion abrimos el archivo con el texto a analizar

	#fich = open(pick_file(), 'r') # Ruta del fichero obtenida con picker, solo lectura
	fich = open(ejemplo.txt, 'r') # Ruta del fichero, solo lectura
	#Leemos una linea y la mandamos a validar
	linea = fich.readline()
	while linea:
		validar_cadena(linea)
		#actualizamos
		linea = fich.readline()

if __name__ == '__main__':
	if validar_cadena(raw_input("\nIntroduce la cadena a validar\n>>> ")):
		print "La cadena es válida :D"
	else:
		print "La cadena NO ES VALIDA"



## *** Con el fichero 'p2.txt'
## Cadenas Validas:
## abbbbbc
## abac
## ac
## aac
## aaccc
## aaccccc

## Cadenas no validas
## aaa
## abab
## abbcc
## aacc

