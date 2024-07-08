# This file computes the mapping from Homosaurus to LCSH.
# The exported file is Homosaurus_links_to_LCSH.nt

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv



gv2 = Graph()
gv2.parse("../v2.ttl")


gv3 = Graph()
gv3.parse("../v3.ttl")

ex = 'http://www.w3.org/2004/02/skos/core#exactMatch'
cl = 'http://www.w3.org/2004/02/skos/core#closeMatch'

pre_lcsh = 'http://id.loc.gov/authorities/subjects/'

count_exactMatch_LCSH_v2 = 0
count_closeMatch_LCSH_v2 = 0

count_exactMatch_LCSH_v3 = 0
count_closeMatch_LCSH_v3 = 0


g_export = Graph()

for (s, p, o) in gv2.triples((None, URIRef(ex), None)):
    # decide if there is LCSH entities involved
    if pre_lcsh in str(o):
        count_exactMatch_LCSH_v2 += 1
        g_export.add((s,p,o))

for (s, p, o) in gv2.triples((None, URIRef(cl), None)):
    # decide if there is LCSH entities involved
    if pre_lcsh in str(o):
        count_closeMatch_LCSH_v2 += 1
        g_export.add((s,p,o))

print ('There are ', count_exactMatch_LCSH_v2, ' exactMatch in version 2')
print ('There are ', count_closeMatch_LCSH_v2, ' closeMatch in version 2')

for (s, p, o) in gv3.triples((None, URIRef(ex), None)):
    # decide if there is LCSH entities involved
    if pre_lcsh in str(o):
        count_exactMatch_LCSH_v3 += 1
        g_export.add((s,p,o))

for (s, p, o) in gv3.triples((None, URIRef(cl), None)):
    # decide if there is LCSH entities involved
    if pre_lcsh in str(o):
        count_closeMatch_LCSH_v3 += 1
        g_export.add((s,p,o))

print ('There are ', count_exactMatch_LCSH_v3, ' exactMatch in version 3')
print ('There are ', count_closeMatch_LCSH_v3, ' closeMatch in version 3')


g_export.serialize('Homosaurus_links_to_LCSH.nt', format = 'nt') # export_dir
g_export.close()
