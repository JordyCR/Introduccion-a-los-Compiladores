# -*- coding: utf-8 -*-
import string, math


text = open("ingles.txt").read().lower().translate(string.maketrans(" "," "), string.punctuation)
t = text.split()
NN = len(t)

# Tamaño del NGrama
tam_NGram = 6

# Creación simple de NGramas
grams = [t[i:i+tam_NGram] for i in xrange(len(t)-tam_NGram+1)]


# print grams
suma = 0
n = 0
q = raw_input("Dame dos palabras a evaluar con t-test\n>>> ").lower().translate(string.maketrans(" "," "), string.punctuation).split()
di = []

# Calculamos la media buscando en todos los elementos =/
for ng in grams:
	if q[0] in ng and q[1] in ng:
		dis = ng.index(q[1]) - ng.index(q[0])
		# Esta impresión solo tiene fines de debugeo
		# print "Encontrado con distancia:", dis
		if dis > 0:
			n += 1
			suma += dis
			di.append(dis) # Arreglo para el calculo de varianza

# Media
u = suma / float(n)
print "\nMedia:",u


# Calculo de la varianza
mm = n - 1
v = [ math.pow(d , 2) for d in di ]
s = math.sqrt(math.fsum(v) / float(mm))
s2 = math.fsum(v) / float(mm)

print "Varianza:", s


t = (len(di) - u) / math.sqrt(s2 / float(NN)) 
print "\nt-test resultado:", t, "\n"

u = text.count(q[0]) / float(NN) * text.count(q[1]) / float(NN)
s2 = x_ = len(di) / float(NN)
t = (x_ - u) / math.sqrt( s2 / float(NN) )
print "t-test 2? resultado:", t, "\n"
