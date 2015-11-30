# -*- coding: utf-8 -*-
import string
import math


ab = raw_input("Dame dos palabras a calcular con PMI (en Ingles)\n>>> ")
ab = ab.split()

T = open('ingles.txt').read().lower().translate(string.maketrans(" "," "), string.punctuation)
TN = T.split()
N = len(TN)

a = ab[0]
b = ab[1]


# Debemos calcular la frecuencia de cada palabra
palabras = {}
for p in TN:
	if p not in palabras:
		palabras[p] = 1
	else:
		palabras[p] += 1


if a not in palabras and b not in palabras:
	print "Alguna de las palabras dadas no existe en el conjunto de palabras"
else:
	freqAB = T.count(' '.join(ab))
	freqA = palabras[a]
	freqB = palabras[b]

	print N, freqAB, freqA, freqB
	print math.log( N * freqAB / float(freqA * freqB) )
