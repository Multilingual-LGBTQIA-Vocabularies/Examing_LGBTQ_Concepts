# This script prints some simple basic statistics about the replacement relations. 


from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx



g_homosaurus_v2_replaces = Graph()
g_homosaurus_v2_replaces.parse ("./replace_relations_homosaurus/v2_replace_links.nt")


g_homosaurus_v3_replaces = Graph()
g_homosaurus_v3_replaces.parse ("./replace_relations_homosaurus/v3_replace_links.nt")


G = g_homosaurus_v2_replaces  + g_homosaurus_v3_replaces

count_v2_replacedBy_v3 = 0
count_v3_replacedBy_v3 = 0
count_v3_replaces_v3 = 0
count_v3_replaces_v2 = 0

for s, p, o in G.triples((None, URIRef('http://purl.org/dc/terms/isReplacedBy'), None)):
    if 'http://homosaurus.org/v2/' in s and 'https://homosaurus.org/v3/' in o:
        count_v2_replacedBy_v3 += 1
    elif 'https://homosaurus.org/v3/' in s and 'https://homosaurus.org/v3/' in o:
        count_v3_replacedBy_v3 += 1

for s, p, o in G.triples((None, URIRef('http://purl.org/dc/terms/replaces'), None)):
    if 'https://homosaurus.org/v3/' in s and 'https://homosaurus.org/v3/' in o:
        count_v3_replaces_v3 += 1
    elif 'https://homosaurus.org/v3/' in s and 'http://homosaurus.org/v2/' in o:
        count_v3_replaces_v2 += 1

print ('count_v2_replacedBy_v3', count_v2_replacedBy_v3)
print ('count_v3_replacedBy_v3', count_v3_replacedBy_v3)
print ('count_v3_replaces_v3', count_v3_replaces_v3)
print ('count_v3_replaces_v2', count_v3_replaces_v2)

# count_v2_replacedBy_v3 1716
# count_v3_replacedBy_v3 1
# count_v3_replaces_v3 0
# count_v3_replaces_v2 1653
