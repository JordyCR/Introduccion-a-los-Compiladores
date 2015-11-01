from bs4 import BeautifulSoup

soup = BeautifulSoup(open("master.html"), "html5lib")

tags = []

for hijo in soup.find_all(True):
    #print hijo.name
    tags.append(hijo.name)

unicos = set(tags)

print len(unicos)
print
for u in unicos:
    print u