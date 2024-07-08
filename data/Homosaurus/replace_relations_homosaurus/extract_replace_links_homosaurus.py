# this file extracts links of replacement between versions

# v2: #isReplacedBy:  1716
# v2: #replaces 0
#
# v3: #isReplacedBy:  1
# v3: #replaces 1653

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv


export_dir = './replace_relations_homosaurus/'

gv2_acc_links = Graph()

gv2 = Graph()
gv2.parse("v2.ttl")

# http://purl.org/dc/terms/replaces
# http://purl.org/dc/terms/isReplacedBy
qres_v2 = gv2.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/terms/>

SELECT (COUNT (*) AS ?ct)
WHERE {
  ?s dc:isReplacedBy ?o
}
''')

for row in qres_v2:
    print('v2: #isReplacedBy: ', row.ct)



qres_v2 = gv2.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/terms/>

SELECT (COUNT (*) AS ?ct)
WHERE {
  ?s dc:replaces ?o
}
''')
for row in qres_v2:
    print('v2: #replaces', row.ct)


qres_v2 = gv2.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/terms/>

SELECT ?s ?p ?o
WHERE {
{
  ?s dc:isReplacedBy ?o.
  BIND(dc:isReplacedBy as ?p)
}
UNION
{
    ?s dc:replaces ?o.
    BIND(dc:replaces as ?p)
}
}
''')

for row in qres_v2:
    # print (row.s, row.p, row.o)
    # print('v2: #isReplacedBy: ', row.s, row.o)
    gv2_acc_links.add((URIRef(row.s), URIRef(row.p), URIRef(row.o)))



gv2_acc_links.serialize(export_dir +'v2_replace_links.nt', format = 'nt') # export_dir
gv2_acc_links.close()
#  Version 3 =====


gv3_acc_links = Graph()

gv3 = Graph()
gv3.parse("v3.ttl")

# http://purl.org/dc/terms/replaces
# http://purl.org/dc/terms/isReplacedBy
qres_v3 = gv3.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/terms/>

SELECT (COUNT (*) AS ?ct)
WHERE {
  ?s dc:isReplacedBy ?o
}
''')

for row in qres_v3:
    print('v3: #isReplacedBy: ', row.ct)


qres_v3 = gv3.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/terms/>

SELECT (COUNT (*) AS ?ct)
WHERE {
  ?s dc:replaces ?o
}
''')
for row in qres_v3:
    print('v3: #replaces', row.ct)


qres_v3 = gv3.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/terms/>

SELECT ?s ?p ?o
WHERE {
{
  ?s dc:isReplacedBy ?o.
  BIND(dc:isReplacedBy as ?p)
}
UNION
{
    ?s dc:replaces ?o.
    BIND(dc:replaces as ?p)
}
}
''')

for row in qres_v3:
    # print (row.s, row.p, row.o)
    # print('v2: #isReplacedBy: ', row.s, row.o)
    gv3_acc_links.add((URIRef(row.s), URIRef(row.p), URIRef(row.o)))

gv3_acc_links.serialize(export_dir + 'v3_replace_links.nt', format = 'nt') # export_dir
gv3_acc_links.close()
