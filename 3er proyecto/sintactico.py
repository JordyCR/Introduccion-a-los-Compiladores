# -*- encoding: utf-8 -*-
from lexico import Lexico
import sys

str_error = '\nError sintactico: Esperaba '
token = ""
mLex = None


def analisis_sintactico():
	global token
	global mLex
	mLex = Lexico('./afd_final.txt', './mas_simple.html')
	token = mLex.getToken()[0].lower()

	S()
	print "La compilación tuvo éxito"


def error(predicts):
	sys.exit(str_error + str(predicts))


def empalme(terminal):
	global token
	global mLex

	print "EMPALME\tToken:", token, type(token), "\tTerminal:", terminal, type(terminal), "\tLinea:", mLex.numlinea
	if terminal == token:
		token = mLex.getToken()[0].lower()
	else:
		error(terminal)


def S():
	global token
	predicts = ['menor']



	if token in predicts:
		AbreHtml()
		Todo()
		CierraHtml()
	else:
		error(predicts)

	 			
def AbreHtml():
	global token
	predicts = ['menor']

	if token in predicts:
		empalme('menor') 
		empalme('prhtml')
		empalme('mayor')
	else:
		error(predicts)

	 	
def CierraHtml():
	global token
	predicts = ['menor']

	if token in predicts:
		empalme('menor') 
		empalme('diagonal')
		empalme('prhtml')
		empalme('mayor')
	else:
		error(predicts)


def Todo():
	global token
	predicts = ['menor']

	if token in predicts:
		BlkHead()
		BlkBody()  
	else:
		error(predicts)

	 		
def BlkHead():
	global token
	predicts = ['menor']

	if token in predicts:
		if token == 'menor':
			AbreHead()
			ElemHead()
			CierraHead()
		else:
			error(predicts)
	else:
		error(predicts)

	 	
def AbreHead():
	global token
	predicts = ['menor']

	if token in predicts:
		empalme('menor') 
		empalme('prhead')
		empalme('mayor')
	else:
		error(predicts)


	 	
def CierraHead():
	global token
	predicts = ['menor']

	if token in predicts:
		empalme('menor') 
		empalme('diagonal')
		empalme('prhead')
		empalme('mayor')
	else:
		error(predicts)

	 	
def BlkBody():
	global token
	predicts = ['menor']

	if token in predicts:
		if token == 'menor':
			AbreBody()
			# ElemBody()  # TODO
			CierraBody()
		else:
			error(predicts)
	else:
		error(predicts)

	 	
def AbreBody():
	global token
	predicts = ['menor']

	if token in predicts:
		empalme('menor') 
		empalme('prbody')
		empalme('mayor')
	else:
		error(predicts)

	 	
def CierraBody():
	global token
	predicts = ['menor']

	if token in predicts:
		empalme('menor') 
		empalme('diagonal') 
		empalme('prbody')
		empalme('mayor')
	else:
		error(predicts)

	 	
def ElemHead():
	global token
	predicts = ['menor']

	if token in predicts:
		if token == 'menor':
			empalme('menor')
			TagH()
			empalme('mayor')
		else:
			error(predicts)
	else:
		error(predicts)

	 	
def TagH():
	global token
	predicts_uno = ['prtitle']
	predicts_dos = ['prstyle']
	predicts_tres = ['prmeta']
	

	if token in predicts_uno:
		empalme('prtitle')
		empalme('mayor')
		# Bloque()  # TODO
		empalme('menor')
		empalme('diagonal')
		empalme('prtitle')

	elif token in predicts_dos:
		empalme('prstyle')
		StyleAttr()
		empalme('mayor')
		# Bloque()  # TODO
		empalme('menor')
		empalme('diagonal')
		empalme('prstyle')

	elif token in predicts_tres:
		empalme('prmeta')
		MetaAttrs()

	else:
		e = [predicts_uno, predicts_dos, predicts_tres]
		error(e)

	 		
def StyleAttr():
	global token
	predicts_uno = ['mayor']
	predicts_dos = ['prtype']

	if token in predicts_uno:
		return  # Epsilon
	elif token in predicts_dos:
		empalme('prtype')
		empalme('igual')
		empalme('string')
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 		
def MetaAttrs():
	global token
	predicts = ['prcontent' , 'prhttp-equiv']

	if token in predicts:
		MAttr()
		OtroMetaAtt()
	else:
		error(predicts)

	 	
def OtroMetaAtt():
	global token
	predicts_uno = ['prcontent' , 'prhttp-equiv']
	predicts_dos = ['mayor']

	if token in predicts_uno:
		MetaAttrs()
	elif token in predicts_dos:
		return  # Epsilon
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 
def MAttr():
	global token
	predicts_uno = ['prcontent']
	predicts_dos = ['prhttp-equiv']

	if token in predicts_uno:
		empalme('prcontent')
		empalme('igual')
		empalme('string')
	elif token in predicts_dos:
		empalme('prhttp-equiv')
		empalme('igual')
		empalme('string')
	else:
		e = [predicts_uno, predicts_dos]
		error(e)	


# TODO
def Bloque():
	global token
	pass

	 
##############################################
#											 #
#	########   #####	######      #####	 #
#	   ##	  ##   ##   ##   ##    ##   ##	 #
#	   ##	  ##   ##   ##    ##   ##   ##	 #
# 	   ##     ##   ##   ##   ##    ##   ##	 #
#      ##      #####    ######      #####	 #
#											 #
##############################################
def ElemBody():
	pass

	 	
def ElemBodyPrima():
	pass

	 	
def Contenido():
	pass

	 	
def ContenidoPrima():
	pass

	  
def Textform():
	pass

	 	
def Imagen():
	pass

	 		
def IAtrib():
	pass

	 		
def Tabla():
	pass

	 		
def Rows():
	pass

	 		
def RowsPrima():
	pass

	 		
def Data():
	pass

	 		
def DataPrima():
	pass

	 		
def TAtrib():
	pass

	 		
def TAtribPrima():
	pass

	 	
def DAtrib():
	pass

	 		
def DAtribPrima():
	pass

	 	
def HAtrib():
	pass

	 		
def HAtribPrima():
	pass

	 	
def Salto():
	pass

			
def Contenedor():
	pass

	 	
def ContenedorPrima():
	pass

	 
def ConAtrib():
	pass

	 	
def Asig():
	pass

	 		


if __name__ == '__main__':
	analisis_sintactico()