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
	Tk().update() # Actualizar la GUI
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
	edoini = []
	edosfin = []

	transiciones = []

	# Leemos todos los estados
	linea = fich.readline()
	while linea:
		linea = linea.replace("\n", "")
		tokens = limpia_comas(linea).split()

		# Validamos que el fichero no se haya pasado de parametros por renglon
		if (len(tokens) - 2 > len(alfabeto)):
			sys.exit("\nERROR: Se encontraron más parametros de los esperados.\nSe esperaban no mas de " + str((len(alfabeto) + 2)) + " elementos\n")

		# Si nos indica que es el primero 
		if (tokens[0] == 'i'):
			if (len(edoini) > 1):
				sys.exit("\nERROR: Se encontró más de un estado inicial.\n")
			edoini.append(tokens[1])
			estados.append(tokens[1])
			tokens = tokens[2:]
		# Si nos indica que es un estado final
		elif (tokens[0] == 'f'):
			edosfin.append(tokens[1])
			estados.append(tokens[1])
			tokens = tokens[2:]
		# Los que no entran en los casos anteriores
		else:
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
	return alfabeto, edoini[0], edosfin, transhash


def validar_cadena(path, cadena):
	'''
	(str) -> bool

	Se valida si la cadena proporcionada es una palabra valida para el autómata
	'''
	# Abrimos el archivo y creamos nuestras estructuras de datos
	# alfabeto, edoini, edosfin, transhash = open_AFD("./p2.txt")
	# alfabeto, edoini, edosfin, transhash = open_AFD(pick_file())
	alfabeto, edoini, edosfin, transhash = open_AFD(path)

	edoactual = edoini
	char = cadena[0]
	n = len(cadena)
	i = 0
	while (i != n):
		if (not (char in alfabeto)):
			return False  # Se dió una cadena que no está dentro del alfabeto valido
		if (transhash[edoactual][char] == '-'):
			return False  # Se encontró que no es valido y no pertenece al lenguaje aceptado por el automata

		edoactual = transhash[edoactual][char]
		i += 1
		if (len(cadena) == i):
			break
		char = cadena[i]

	if edoactual in edosfin:
		return True  # Terminó bien el recorrido y en un estado final

	return False  # Terminó en un estado NO FINAL


def __main__():
	path = pick_file()
	op = 'c'
	while (op == 'c'):
		if validar_cadena(path, raw_input("\nIntroduce la cadena a validar\n>>> ")):
			print "La cadena es válida :D"
		else:
			print "La cadena NO ES VALIDA"
		op = raw_input("\nDesea introducir otra cadena? (Inserte 'C' para continuar)\n>>> ").lower()


__main__()

## *** Con el fichero 'p2.txt'
## Cadenas Validas:
## abbbbbc
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