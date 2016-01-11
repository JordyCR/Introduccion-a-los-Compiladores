import re 

def remover_comments(t):
	t = open('ej_comm.html').read().decode('utf-8')
	t = re.sub(r"(<!--.*?-->)", '', t)

	return t