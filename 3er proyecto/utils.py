# -*- encoding: utf-8 -*-

'''
Python module containing our util functions for general pourposes
to be used in the 'Introducción a los Compiladores' classes
'''
import re


def get_file_path():
    '''
	(None) -> StringPath

	Función que abre un dialogo para seleccionar un archivo y devuelve el 
	path del archivo

	NOTA: Si el usuario pulsa "Cancelar", el valor devuelto será cadena vacía ("")
	'''
    from Tkinter import Tk
    from tkFileDialog import askopenfilename

    Tk().withdraw()  # no queremos una GUI completa, asi que se oculta el resto de la GUI
    Tk().update()  # Actualizar la GUI
    filename = askopenfilename()  # Mostramos un Dialogo para abrir ficheros y se regresa el path

    return filename


def limpia_comas(str):
    '''
	String -> String sin comas (',')

	Quita las comas únicamente del fichero con el AFD. Esta función no se
	ha programado para que se aplique sobre la cadena de entrada
	'''
    return str.replace(",", "")  # Quitar comas



def remover_comments(t):
    t = open('ej_comm.html').read().decode('utf-8')
    t = re.sub(r"(<!--.*?-->)", '', t)
    
    return t