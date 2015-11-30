# -*- coding: utf-8 -*-
from pattern.en import parse
import re
import string
from collections import Counter
from itertools import islice, izip

p = parse(open("ingles.txt").read().lower().translate(string.maketrans(" "," "), string.punctuation))
l = p.split()

toks = [ i[1] for i in l[0] ]
# wrds = [ i[0] for i in l[0] ]

res = Counter(izip(toks, islice(toks, 1, None)))

for ng in res:
	print "%-10s %s   %s" % (' '.join(ng), "\t:", res[ng])