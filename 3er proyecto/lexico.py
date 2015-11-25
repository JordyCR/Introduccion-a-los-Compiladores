# -*- encoding: utf-8 -*-
import sys
import utils

class Lexico:
    """
    Lexico class, this class implements all lexic analizer methods and variables
    (String path) To be used to open the AFD file
    """
    def __init__(self, path, comp):
        # Check if the user picked a file instead "Cancel"
        self.reservadas = open("PRs.txt").read().split()
        # print self.reservadas
        if path == "":
            self.isPathSet = False
            return
        self.isPathSet = True # Se Proporcionó un path real
        self.open_AFD(path) # Abrimos el fichero
        self.numlinea = 1
        self.listatokens = []
        self.setArchivoComp(comp)


    def setArchivoComp(self, arch):
        f = open(arch, 'r').read()
        if f.strip() == '':
            sys.error("Archivo vacío")
        c = open('./cache.txt', 'w')
        c.write(utils.remover_comments(f))
        c.close()
        self.archivo = open('./cache.txt').readlines()


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


            # Si nos indica que es un estado final
            if (tokens[-1] != '-'):
                edosfin.append(tokens[0])
            
            estados.append(tokens[0])
            tokens = tokens[1:]

            transiciones.append(tokens)

            # Actualizamos
            linea = fich.readline()

        # print "El archivo se ha cargado correctamente"

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
        # print "Se ha creado la tabla de transiciones con exito"
        # print "El alfabeto válido es el siguiente:"
        # print alfabeto, "\n"
        
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
        edoini = self.edoini
        edosfin = self.edosfin
        transhash = self.transhash
        

        # Inicia validación en el AFD
        edoactual = edoini
        char = cadena[0]
        n = len(cadena)
        i = 0

        ll = []
        ant = 0

        while (i < n):  # Mientras no se rebase el num de caracteres por linea
            if (char == ' ' and edoactual == self.edoini) :
                while (char == ' ' ):
                    i += 1 
                    char = cadena[i]
                    ant = i

            if (not (char in alfabeto)):
                if char.isalpha() and transhash[edoactual]['let'] != '-':
                    edoactual = transhash[edoactual]['let']
                elif char.isdigit() and transhash[edoactual]['dig'] != '-':
                    edoactual = transhash[edoactual]['dig']
                elif char == ' ':
                    edoactual = transhash[edoactual]['esp']


                else:
                    # sys.exit("\nERROR: Se encontró un elemento no valido.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")
                    edoactual = transhash[edoactual]['otro']

            elif (transhash[edoactual][char] == '-'):
                sys.exit("\nERROR: Lenguaje no aceptado.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")

            else:
                edoactual = transhash[edoactual][char]
            
            i += 1
            if (len(cadena) == i): # Esto indica que estamos leyendo el último caracter
                if transhash[edoactual]['retroceso'] != '-':
                    i -= int(transhash[edoactual]['retroceso'])
                # char = cadena[i]
                if edoactual in edosfin:
                    if transhash[edoactual]['token'] == 'Bloque' and self.esPalabraResevada(cadena[ant:i]):
                        ll.append(["PR" + cadena[ant:i] , cadena[ant:i]])
                    else:
                        ll.append([transhash[edoactual]['token'] , cadena[ant:i]])
                elif transhash[edoactual]['fin'] != '-': # No error , valido
                    edoactual = transhash[edoactual]['fin']
                    ll.append([transhash[edoactual]['token'] , cadena[ant:i]])
                else:
                    sys.exit("\nERROR: Lenguaje no aceptado.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")
                ant = i
                edoactual = self.edoini
                continue
            char = cadena[i]

            if edoactual in edosfin:
                # Retroceso y añadimos el token
                i -= int(transhash[edoactual]['retroceso'])
                char = cadena[i]

                if transhash[edoactual]['token'] == 'Bloque' and self.esPalabraResevada(cadena[ant:i]):
                    ll.append(["PR" + cadena[ant:i] , cadena[ant:i]])

                elif transhash[edoactual]['token'] == 'Bloque':
                    
                    ll.append(['Bloque' , cadena[ant:i]])
                    # else:
                    #     sys.exit("\nERROR: Lenguaje no aceptado.\nLinea: " + str(self.numlinea)+"\nCerca de: " + cadena+"\n")
                else:
                    ll.append([transhash[edoactual]['token'] , cadena[ant:i]])

                ant = i
                edoactual = self.edoini


        return ll   # Terminó en un estado NO FINAL


    def esPalabraResevada(self, palabra):
        words = self.reservadas
        return palabra in words

    def getToken(self):
        # Valida cadena

        listatokens = self.listatokens

        if len(listatokens) == 0:
            try:
                linea = utils.remover_espacios(self.archivo.pop(0).strip())
                while linea == '':
                    linea = utils.remover_espacios(self.archivo.pop(0).strip())
                    self.numlinea += 1
            except Exception:
                return None

            self.numlinea += 1

            # print "** Leer", linea
            elemento = linea
            listatokens = []

            listatokens = self.validar_cadena(elemento)

            self.listatokens = listatokens

        # print "** Tokens Len", len(listatokens)
        # print "LINEAS", self.numlinea
        return listatokens.pop(0)




if __name__ == '__main__':
    # path = utils.get_file_path()
    # mLex = Lexico(path)
    mLex = Lexico('./afd_final.txt', './mas_simple.html')

    # Leer archivo e ir pasando linea por linea
    # f = open(utils.get_file_path(), 'r')
    # f = open(, 'r').read()
    # c = open('./cache.txt', 'w')
    # c.write(utils.remover_comments(f))
    # c.close()
    # f = open('./cache.txt')


    print

    l = mLex.getToken()
    while l != None:
        # print "** Token", l, "TYPE", type(l)
        print '<', l[0]+ '\t, "'+ l[1]+ '" >'
        l = mLex.getToken()

    print "\n>>> Acabó el archivo"
    print '\n'
