# this file exports the mappings between QLIT and homosaurus

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx


qlit = Graph()
qlit.parse ("./Qlit-v1.ttl")

g = Graph()
count = 0
count_exactMatch = 0
count_closeMatch = 0

for s, p, o in qlit.triples ((None, None, None)):
    if  'queerlit.dh.gu.se/qlit/' in str(s):
        if  'http://id.loc.gov/authorities/subjects/sh' in str(o):
            g.add ((URIRef(s), URIRef(p), URIRef(o)))
            count += 1
            if 'exactMatch'in str(p):
                count_exactMatch +=1
            if 'closeMatch'in str(p):
                count_closeMatch +=1

g.serialize('qlit-lcsh.nt', format = 'nt') # export_dir
g.close()

print ('# triples ', count)
print ('# triples exactMatch = ', count_exactMatch)
print ('# triples closeMatch = ', count_closeMatch)
