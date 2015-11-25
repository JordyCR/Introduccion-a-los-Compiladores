# -*- encoding: utf-8 -*-
from lexico import Lexico
import sys
import utils

str_error = '\nError sintactico: Esperaba '
token = ""
mLex = None


def analisis_sintactico():
	global token
	global mLex
	#arch = utils.get_file_path()
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
		# print "ACTUAL", token
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
		ElemBody()  # TODO
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
	predicts = ['diagonal']

	if token in predicts:
		#empalme('menor') 
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
	global token
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
		Texto()
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
		Texto()
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


def Texto():
	global token
	predicts_uno = ['menor', 'diagonal']
	predicts_dos = ['bloque']

	if token in predicts_uno:
		return  # Epsilon
	elif token in predicts_dos:
		empalme('bloque')
		Texto()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 
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
	global token
	predicts_uno = ['menor']
	predicts_dos = ['bloque']

	if token in predicts_uno:
		empalme('menor')
		ElemBodyPrima()
		
	elif token in predicts_dos:
		Texto()
		#empalme('menor')
		ElemBody()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 	
def ElemBodyPrima():
	global token
	predicts_uno = ['prb','prp', 'prtable', 'primg', 'prbr']
	predicts_dos = ['prdiv']
	predicts_tres = ['diagonal', 'menor']

	if token in predicts_uno:
		Contenido()
	elif token in predicts_dos:
		Contenedor()
	elif token in predicts_tres:
		return
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 	
def Contenido():
	global token
	predicts = ['prb', 'prp', 'prtable', 'primg', 'prbr']

	if token in predicts:
		ContenidoPrima()
		ElemBody()
	else:
		error(predicts)

	 	
def ContenidoPrima():
	global token
	predicts_uno = ['prb', 'prp']
	predicts_dos = ['primg']
	predicts_tres = ['prtable']
	predicts_cuatro = ['prbr']

	if token in predicts_uno:
		Textform()

	elif token in predicts_dos:
		Imagen()

	elif token in predicts_tres:
		Tabla()

	elif token in predicts_cuatro:
		Salto()

	else:
		e = [predicts_uno, predicts_dos, predicts_tres, predicts_cuatro]
		error(e)

	  
def Textform():
	global token
	predicts_uno = ['prb']
	predicts_dos = ['prp']

	if token in predicts_uno:
		empalme('prb')
		empalme('mayor')
		Texto()
		empalme('menor')
		empalme('diagonal')
		empalme('prb')
		empalme('mayor')
	elif token in predicts_dos:
		empalme('prp')
		empalme('mayor')
		Texto()
		empalme('menor')
		empalme('diagonal')
		empalme('prp')
		empalme('mayor')
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 	
def Imagen():
	global token
	predicts = ['primg']

	if token in predicts:
		empalme('primg')
		IAtrib()
		empalme('mayor')
	else:
		error(predicts)

	 		
def IAtrib():
	global token
	predicts_uno = ['prsrc']
	predicts_dos = ['prwidth']
	predicts_tres = ['prheight']
	predicts_cuatro = ['mayor']

	if token in predicts_uno:
		empalme('prsrc')
		Asig()
		IAtrib()

	elif token in predicts_dos:
		empalme('prwidth')
		Asig()
		IAtrib()

	elif token in predicts_tres:
		empalme('prheight')
		Asig()
		IAtrib()

	elif token in predicts_cuatro:
		return  # Epsilon

	else:
		e = [predicts_uno, predicts_dos, predicts_tres, predicts_cuatro]
		error(e)

	 		
def Tabla():
	global token
	predicts = ['prtable']
	if token in predicts:
		empalme('prtable')
		TAtrib()
		empalme('mayor')
		empalme('menor')
		#TablaPrima()
		ElemTabla() 
		empalme('diagonal')
		empalme('prtable')
		empalme('mayor')
	else:
		e = [predicts]
		error(e)

def ElemTabla():
	global token
	predicts_uno = ['prtr', 'prtbody']
	predicts_dos = ['diagonal']

	if token in predicts_uno:
		Rows()
		ElemTabla()
	elif token in predicts_dos:
		return
	else:
		e = [predicts_uno, predicts_dos]
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
		empalme('diagonal')
		empalme('prtr')
		empalme('mayor')
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
		#TablaPrima()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)
	 		
def RowsPrima():
	global token
	predicts_uno = ['prtd' , 'prth']
	predicts_dos = ['diagonal']

	if token in predicts_uno:
		Data()
	elif token in predicts_dos:
		return
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
		AbreData()
		empalme('diagonal')
		empalme('prtd')
		empalme('mayor')
		empalme('menor')
		RowsPrima()
	elif token in predicts_dos:
		empalme('prth')
		HAtrib()
		empalme('mayor')
		AbreData()
		empalme('diagonal')
		empalme('prth')
		empalme('mayor')
		empalme('menor')
		RowsPrima()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)
	 		
def AbreData():
	global token
	predicts_uno = ['menor']
	
	predicts_dos = ['bloque']

	if token in predicts_uno:
		empalme('menor')
		ElemData()
	elif token in predicts_dos:
		empalme('bloque')
		AbreData()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

def ElemData():
	global token
	predicts_uno = ['prb', 'prp', 'prtable', 'primg', 'prbr', 'prdiv']
	predicts_dos = ['diagonal']
	if token in predicts_uno:
		ElemDataPrima()
		AbreData()
	elif token in predicts_dos:
		return
	else: 
		e = [predicts_uno, predicts_dos]
		error(e)
def ElemDataPrima():
	global token
	predicts_uno = ['prb', 'prp', 'prtable', 'primg', 'prbr']
	predicts_dos = ['prdiv']

	if token in predicts_uno:
		ContenidoPrima()
	elif token in predicts_dos:
		Contenedor()
	else:
		e = [predicts_uno, predicts_dos]
		error(e)


def TAtrib():
	global token
	predicts_uno = ['prcellpading', 'prwidth', 'pralign', 'prborder']
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
	predicts_tres = ['pralign']
	predicts_cuatro = ['prborder']

	if token in predicts_uno:
		empalme('prcellpading')
	elif token in predicts_dos:
		empalme('prwidth')
	elif token in predicts_tres:
		empalme ('pralign')
	elif token in predicts_cuatro:
		empalme('prborder')
	else:
		e = [predicts_uno, predicts_dos, predicts_tres, predicts_cuatro]
		error(e)

	 	
def DAtrib():
	global token
	predicts_uno = ['pralign', 'prwidth', 'prstyle', 'prrowspan', 'prcolspan', 'prvalign']
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
	predicts_uno = ['pralign']
	predicts_dos = ['prwidth']
	predicts_tres = ['prstyle']
	predicts_cuatro = ['prrowspan']
	predicts_cinco = ['prcolspan']
	predicts_seis = ['prvalign']

	if token in predicts_uno:
		empalme('pralign')
	elif token in predicts_dos:
		empalme('prwidth')
	elif token in predicts_tres:
		empalme('prstyle')
	elif token in predicts_cuatro:
		empalme('prrowspan')
	elif token in predicts_cinco:
		empalme('prcolspan')
	elif token in predicts_seis:
		empalme('prvalign')
	else:
		e = [predicts_uno, predicts_dos, predicts_tres, predicts_cuatro, predicts_cinco, predicts_seis]
		error(e)

	 	
def HAtrib():
	global token
	predicts_uno = ['prcolspan', 'prstyle', 'pralign', 'prclass']
	predicts_dos = ['mayor']

	if token in predicts_uno:
		HAtribPrima()
		Asig()
		HAtrib()
	elif token in predicts_dos:
		return
	else:
		e = [predicts_uno, predicts_dos]
		error(e)

	 		
def HAtribPrima():
	global token
	predicts_uno = ['prcolspan']
	predicts_dos = ['prstyle']
	predicts_tres = ['pralign']
	predicts_cuatro = ['prclass']

	if token in predicts_uno:
		empalme('prcolspan')
	elif token in predicts_dos:
		empalme('prstyle')
	elif token in predicts_tres:
		empalme('pralign')
	elif token in predicts_cuatro:
		empalme('prclass')
	else:
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
		#empalme('menor')
		empalme('diagonal')
		empalme('prdiv')
		empalme('mayor')
		ElemBody()
	else:
		e = [predicts]
		error(e)

	 
def ConAtrib():
	global token
	predicts_uno = ['pralign']
	predicts_dos =['mayor']

	if token in predicts_uno:
		empalme('pralign')
		Asig()
	elif token in predicts_dos:
		return 
	else:
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