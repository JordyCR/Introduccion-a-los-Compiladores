from lexico import Lexico
import sys

str_error = 'Error sintactico en'

def analisis_sintactico():
	mLex = Lexico('./afd_final.txt', './simple.html')

	token = mLex.getToken()

	Init(token)


def Init(token):
	if token[0] == 'Menor':
		S(token)
	else:
		sys.error(str_error + " Init " + "Esperaba: " + "<< Predictivos >>")


def S(token):
	if token[0] == 'Menor':
		()


	 			
def AbreHtml():
	pass

	 	
def CierraHtml():
	pass

	 	
def Todo():
	pass

	 		
def BlkHead():
	pass

	 	
def AbreHead():
	pass

	 	
def CierraHead():
	pass

	 	
def BlkBody():
	pass

	 	
def AbreBody():
	pass

	 	
def CierraBody():
	pass

	 	
def ElemHead():
	pass

	 	
def TagH():
	pass

	 		
def TagH():
	pass

	 		
def StyleAttr():
	pass

	 	
def TagH():
	pass

	 		
def MetaAttrs():
	pass

	 	
def OtroMetaAtt():
	pass

	 
def MAttr():
	pass


def Bloque():
	pass

	 		

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