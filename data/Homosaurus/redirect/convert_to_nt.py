# This simple script converts the file to N-Triple file.

import networkx as nx
import sys
import csv
import requests
from requests.exceptions import Timeout
import pickle
from rdflib import Graph, URIRef

my_redirect = "https://krr.triply.cc/krr/metalink/def/redirectedTo"  # a relation

redirected_mapping = {}

with open('redirected_entities_v3.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count_loaded_redirect = 0
    for row in reader:
        redirected_mapping[row['Source']] = row['Redirected']
        count_loaded_redirect += 1

# with open('redirected_entities_v2.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     count_loaded_redirect = 0
#     for row in reader:
#         redirected_mapping[row['Source']] = row['Redirected']
#         count_loaded_redirect += 1
print ('count_loaded_redirect = ', count_loaded_redirect)

g = Graph()

for s in redirected_mapping:
    o = redirected_mapping[s]
    g.add((URIRef(s), URIRef(my_redirect), URIRef(o)))

g.serialize('homosaurus-redirect.nt', format = 'nt') # export_dir
g.close()
