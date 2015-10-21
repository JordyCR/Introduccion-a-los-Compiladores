# -*- encoding: utf-8 -*-
import sys
import utils

class Lexico:
    """
    Lexico class, this class implements all lexic analizer methods and variables
    (String path) To be used to open the AFD file
    """
    def __init__(self, path):
        # Check if the user picked a file instead "Cancel"
        if path == "":
            self.isPathSet = False
            return
        self.isPathSet = True # Se Proporcionó un path real
        self.open_AFD(path) # Abrimos el fichero
        self.numlinea = 1
        

    def open_AFD(self, path):
        '''
        (StringPath) -> AFD
        '''

        # TODO: Validar 'path' que no sea cadena vacía ("")

        # Abrimos el fichero que contiene el AFD
        fich = open(path, 'r') # Ruta del fichero, solo lectura

        # Empezamos leyendo el alfabeto
        alfabeto = utils.limpia_comas(fich.readline()).split()

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
            tokens = utils.limpia_comas(linea).split()

            # Validamos que el fichero no se haya pasado de parametros por renglon
            #if (len(tokens) - 2 > len(alfabeto)):
            #   sys.exit("\nERROR: Se encontraron más parametros de los esperados.\nSe esperaban no mas de " + str((len(alfabeto) + 2)) + " elementos\n")

            # Si nos indica que es el primero 
            '''if (tokens[0] == 'i'):
                if (len(edoini) > 1):
                    sys.exit("\nERROR: Se encontró más de un estado inicial.\n")
                edoini.append(tokens[1])
            estados.append(tokens[1])
            tokens = tokens[2:]'''
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
        #   transhash[edoactual][letra_de_la_cadena_introducida_actual]
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
        # return alfabeto, edosfin, transhash
        self.alfabeto = alfabeto
        self.edoini = estados[0]
        self.edosfin = edosfin
        self.transhash = transhash



    # TODO: Ahora este metodo debe manejar errores, devolver un objeto, no solo un bool
    # def validar_cadena(path, cadena):
    def validar_cadena(self, cadena):
        '''
    	(str) -> List[Tipo(token), valor(token)]

    	Se valida si la cadena proporcionada es una palabra valida para el autómata
    	'''
        # Abrimos el archivo y creamos nuestras estructuras de datos
        # alfabeto, edoini, edosfin, transhash = open_AFD("./p2.txt")
        # alfabeto, edoini, edosfin, transhash = open_AFD(pick_file())
        # alfabeto, edoini, edosfin, transhash = open_AFD(path)

        # Verificamos que haya un path setteado con anterioridad
        if not self.isPathSet:
            # TODO: Manejor de error
            print "No hay un AFD definido aún. Invoque open_AFD(path) primero"
            return [[]]

        # TODO: ¿Solo necesitamos estos?
        alfabeto = self.alfabeto
        # edoini = self.edoini
        edosfin = self.edosfin
        transhash = self.transhash


        # Verificación previa
        if self.esPalabraResevada(cadena):
            return [["PR" + cadena, cadena]]
        

        # Inicia validación en el AFD
        edoactual = self.edoini
        char = cadena[0]
        n = len(cadena)
        i = 0

        ll = []
        ant = 0

        while (i != n):
            if (not (char in alfabeto)):
                if char.isalpha():
                    edoactual = transhash[edoactual]['let']
                elif char.isdigit():
                    edoactual = transhash[edoactual]['dig']
                else:
                    sys.exit("\nERROR: Se encontró un elemento no valido.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")

            elif (transhash[edoactual][char] == '-'):
                sys.exit("\nERROR: Lenguaje no aceptado.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")

            else:
                edoactual = transhash[edoactual][char]
            
            i += 1
            if (len(cadena) == i):
                if edoactual in edosfin:
                    ll.append([transhash[edoactual]['token'] , cadena[ant:i]])                    
                elif transhash[edoactual]['otro'] != '-': # No error , valido
                    edoactual = transhash[edoactual]['otro']
                    ll.append([transhash[edoactual]['token'] , cadena[ant:i]])
                else:
                    sys.exit("\nERROR: Lenguaje no aceptado.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")
                break
            char = cadena[i]

            if edoactual in edosfin:
                # Retroceso y añadimos el token
                i -= int(transhash[edoactual]['retroceso'])
                char = cadena[i]
                print "cadena[ant:i] -->", cadena[ant:i], " AND ", self.esPalabraResevada(cadena[ant:i])
                if transhash[edoactual]['token'] == 'id' and self.esPalabraResevada(cadena[ant:i]):
                    ll.append(["PR" + cadena[ant:i] , cadena[ant:i]])
                    #print ["PR" + cadena[ant:i] , cadena[ant:i]]
                else:
                    ll.append([transhash[edoactual]['token'] , cadena[ant:i]])
                    #print [transhash[edoactual]['token'] , cadena[ant:i]]
                ant = i
                edoactual = self.edoini


        return ll   # Terminó en un estado NO FINAL


    def esPalabraResevada(self, palabra):
        # Como definirlas?
        words = ['for', 'while', 'if', 'else', 'do']

        # El caso base es que ambas esten iguales
        if palabra in words: 
            return True

        # Puede pasar que la cadena dada sea 'for(' así que:
         
        # ... Aparentemente, según la maestra, los tokens que ella quiere
        # por ahora son: Identificador, <, <=, >, =>, Entero positivo, Entero negativo
        # y 'for', 'while', 'if', 'else', 'do'
        # Esperemos que así sea, mientras tanto...
        return False
        # De no ser así, tendríamos que validar si cada palabra en la lista 'words'
        # es un sub-string de 'palabra' y verificar que lo que le sigue a 'palabra'
        # no sea una 'letra' o 'digito'

    def getToken(self, linea):
        # Valida cadena

        self.listlinea = linea.split()
        listlinea = self.listlinea

        listatokes = []

        for elemento in listlinea:
            ll = self.validar_cadena(elemento)
            for l in ll:
                listatokes.append(l)

        self.numlinea += 1

        return listatokes # TODO: Que devuelva de uno en uno

        # return <:> Con cadena validada



if __name__ == '__main__':
    # path = utils.get_file_path()
    # mLex = Lexico(path)
    mLex = Lexico('./pp.txt')

    # Leer archivo e ir pasando linea por linea
    # f = open(utils.get_file_path(), 'r')
    f = open('./codigo.txt', 'r')

    print
    for line in f:
        print line
        ll = mLex.getToken(line)

        for l in ll:
            print '<', l[0]+ '\t, "'+ l[1]+ '" >'
        print '\n'
