# -*- coding: utf-8 -*-
import re
from itertools import islice, izip
import string
from collections import Counter


words = re.findall("\w+", open("ingles.txt").read().lower().translate(string.maketrans(" "," "), string.punctuation))

# print words[100:110]
# print Counter(izip(words, islice(words, 1, None)))
res = Counter(izip(words, islice(words, 1, None)))

for ng in res:
	print "%-30s %s   %s" % (' '.join(ng), "\t:", res[ng])