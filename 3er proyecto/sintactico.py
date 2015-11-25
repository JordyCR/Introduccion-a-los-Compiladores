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
	print "\n\nERROR: Token encontrado:", token
	sys.exit(str_error + str(predicts))


def empalme(terminal):
	global token
	global mLex

	print "EMPALME\tToken-Encontrado:", token, "\tTerminal-Esperado:", terminal, "\tLinea:", mLex.numlinea-1
	if terminal == token:
		token = mLex.getToken()
		if token != None:
			token = token[0].lower()
		else:
			print "\n\nSe terminarón los tokens"
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
		AbreHead()
		empalme('menor')
		ElemHead()
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
	predicts = ['diagonal']

	if token in predicts:
		empalme('diagonal')
		empalme('prhead')
		empalme('mayor')
	else:
		error(predicts)

	 	
def BlkBody():
	global token
	predicts = ['menor']

	if token in predicts:
		AbreBody()
		# ElemBody()  # TODO
		CierraBody()
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
	predicts_uno = ['prtitle', 'prstyle', 'prmeta']
	predicts_dos = ['diagonal']

	if token in predicts_uno:
		TagsHead()
	elif token in predicts_dos:
		CierraHead()
	else:
		error(predicts)


def TagsHead():
	predicts_uno = ['prtitle']
	predicts_dos = ['prstyle']
	predicts_tres = ['prmeta']

	if token in predicts_uno:
		TagHT()
		empalme('mayor')
		empalme('menor')
		ElemHead()

	elif token in predicts_dos:
		TagHS()
		empalme('mayor')
		empalme('menor')
		ElemHead()

	elif token in predicts_tres:
		TagHM()
		empalme('mayor')
		empalme('menor')
		ElemHead()

	else:
		e = [predicts_uno, predicts_dos, predicts_tres]
		error(e)


def TagHT():
	global token
	predicts = ['prtitle']

	if token in predicts:
		empalme('prtitle')
		empalme('mayor')
		Texto()  # TODO
		empalme('menor')
		empalme('diagonal')
		empalme('prtitle')

	else:
		error(predicts)


def TagHS():
	global token
	predicts = ['prstyle']

	if token in predicts:
		empalme('prstyle')
		StyleAttr()
		empalme('mayor')
		Texto()  # TODO
		empalme('menor')
		empalme('diagonal')
		empalme('prstyle')

	else:
		error(predicts)

	 	
def TagHM():
	global token
	predicts = ['prmeta']

	if token in predicts:
		empalme('prmeta')
		MetaAttrs()

	else:
		error(predicts)

	 		
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
def Texto():
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
	global token
	predicts = ['prtable']
	if token in predicts:
		empalme('prtable')
		TAtrib()
		empalme('mayor')
		empalme('menor')
		TablaPrima()
	else:
		e = [predicts]
		error(e)

def TablaPrima():
	global token
	predicts_uno = ['prtr', 'prtbody']
	predicts_dos = ['diagonal']

	if token in predicts_uno:
		Rows()
	elif token in predicts_dos:
		empalme('diagonal')
		empalme('prtable')
		empalme('mayor')
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 		
def Rows():
	global token
	predicts_uno =['prtr']
	predicts_dos = ['prtbody']

	if token in predicts_uno:
		empalme('prtr')
		empalme('mayor')
		empalme('menor')
		RowsPrima()
	elif token in predicts_dos:
		empalme('prtbody')
		empalme('mayor')
		empalme('menor')
		Rows()
		empalme('menor')
		empalme('diagonal')
		empalme('prtbody')
		empalme('mayor')
		empalme('menor')
		TablaPrima()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)
	 		
def RowsPrima():
	global token
	predicts_uno = ['prtd']
	predicts_dos = ['diagonal']

	if token in predicts_uno:
		Data()
	elif token in predicts_dos:
		empalme('diagonal')
		empalme('prtr')
		empalme('mayor')
		empalme('menor')
		TablaPrima()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)
	 		
def Data():
	global token
	predicts_uno = ['prtd']
	predicts_dos = ['prth']

	if token in predicts_uno:
		empalme('prtd')
		DAtrib()
		empalme('mayor')
		Texto()
		empalme('menor')
		empalme('diagonal')
		empalme('prtd')
		empalme('mayor')
		empalme('menor')
		RowsPrima()
	elif token in predicts_dos:
		empalme('prth')
		HAtrib()
		empalme('mayor')
		Texto()
		empalme('menor')
		empalme('diagonal')
		empalme('prth')
		empalme('mayor')
		empalme('menor')
		RowsPrima()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)
	 		
def TAtrib():
	global token
	predicts_uno = ['prcellpading', 'prwidth', 'prheight']
	predicts_dos = ['mayor']

	if token in predicts_uno:
		TAtribPrima()
		Asig()
		TAtrib()
	elif token in predicts_dos:
		return
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 		
def TAtribPrima():
	global token
	predicts_uno = ['prcellpading']
	predicts_dos = ['prwidth']
	predicts_tres = ['prheight']

	if token in predicts_uno:
		empalme('prcellpading')
	elif token in predicts_dos:
		empalme('prwidth')
	elif token in predicts_tres:
		empalme ('prheight')
	else:
		e = [predicts_uno, predicts_dos, predicts_tres]
		error(e)

	 	
def DAtrib():
	global token
	predicts_uno = ['praling', 'prwidth', 'praling']
	predicts_dos = ['mayor']

	if token in predicts_uno:
		DAtribPrima()
		Asig()
		DAtrib()
	elif token in predicts_dos:
		return
	else:
		e = [predicts_uno, predicts_dos]
		error(e)



	 		
def DAtribPrima():
	global token
	predicts_uno = ['praling']
	predicts_dos = ['prwidth']
	predicts_tres = ['praling']

	if token in predicts_uno:
		empalme('praling')
	elif token in predicts_dos:
		empalme('prwidth')
	elif token in predicts_tres:
		empalme('praling')
	else:
		e = [predicts_uno, predicts_dos, predicts_tres]
		error(e)


	 	
def HAtrib():
	global token
	predicts_uno = ['prcolspan', 'prstyle', 'praling', 'prclass']
	predicts_dos = ['mayor']

	if token in predicts_uno:
		HAtribPrima()
		Asig()
		HAtrib()
	elif token in predicts_dos:
		return
	e = [predicts_uno, predicts_dos]
		error(e)

	 		
def HAtribPrima():
	global token
	predicts_uno = ['prcolspan']
	predicts_dos = ['prstyle']
	predicts_tres = ['praling']
	predicts_cuatro = []

	if token in predicts_uno:
		empalme('prcolspan')
	elif token in predicts_dos:
		empalme('prstyle')
	elif token in predicts_tres:
		empalme('praling')
	elif token in predicts_cuatro:
		empalme('prclass')
	e = [predicts_uno, predicts_dos, predicts_tres, predicts_cuatro]
		error(e)
	 	
def Salto():
	global token
	predicts = ['prbr']

	if token in predicts:
		empalme('prbr')
		empalme('mayor')
	else:
		e = [predicts]
		error(e)

			
def Contenedor():
	global token
	predicts = ['prdiv']

	if token in predicts:
		empalme('prdiv')
		ConAtrib()
		empalme('mayor')
		ContenedorPrima()
	else:
		e = [predicts]
		error(e)


	 	
def ContenedorPrima():
	global token
	predicts = ['menor', 'bloque']

	if token in predicts:
		ElemBody()
		empalme('menor')
		empalme('diagonal')
		empalme('prdiv')
		empalme('mayor')
	else:
		e = [predicts]
		error(e)

	 
def ConAtrib():
	global token
	predicts_uno = ['praling']
	predicts_dos =['mayor']

	if token in predicts_uno:
		empalme('praling')
		Asig()
	elif token in predicts_dos:
		return 
	e = [predicts_uno, predicts_dos]
		error(e)


	 	
def Asig():
	global token
	predicts = ['igual']

	if token in predicts:
		empalme('igual')
		empalme('string')
	else:
		e = [predicts]
		error(e)


	 		


if __name__ == '__main__':
	analisis_sintactico()