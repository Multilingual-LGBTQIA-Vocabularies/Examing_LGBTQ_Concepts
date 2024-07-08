# this file exports outdated mappings between QLIT and homosaurus
# There is only one found.

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx


qlit = Graph()
qlit.parse ("../data/QLIT/Qlit-v1.ttl")

G2 = Graph()
G3 = Graph()
h2_entities = set()
h3_entities = set()

count_v2 = 0
count_v3 = 0

count_exactMatch_v3 = 0
count_closeMatch_v3 = 0

qlit_entities_mapping_to_homosaurus = {}
outdated_qlit_entities_mapping_to_homosaurus = {}
qlit_entities_all = set()

for s, p, o in qlit.triples ((None, None, None)):
    if  'queerlit.dh.gu.se/qlit/' in str(s):
        qlit_entities_all.add(str(s))
    if  'queerlit.dh.gu.se/qlit/' in str(o):
        qlit_entities_all.add(str(o))


for subj_qlit, p, obj_h_v3 in qlit.triples ((None, None, None)):
    if ('homosaurus.org/v3/' in str(obj_h_v3)):
        if str(subj_qlit) in qlit_entities_all:
            count_v3 += 1
            G3.add((URIRef(subj_qlit), URIRef(p), URIRef(obj_h_v3)))
            qlit_entities_mapping_to_homosaurus[str(subj_qlit)] = str(obj_h_v3)

            h3_entities.add(str(subj_qlit))

            if 'exactMatch' in p:
                count_exactMatch_v3 += 1
            if 'closeMatch' in p:
                count_closeMatch_v3 += 1

redirected_mapping = {}

with open('../data/Homosaurus/redirect/redirected_entities_v3.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count_loaded_redirect = 0
    for row in reader:
        redirected_mapping[row['Source']] = row['Redirected']

print('# redirect = ',len(redirected_mapping))

g_homosaurus_v3_replaces = Graph()
g_homosaurus_v3_replaces.parse ("../data/Homosaurus/replace_relations_homosaurus/v3_replace_links.nt")

replace_mapping = {}
for s, p, o in g_homosaurus_v3_replaces.triples((None, URIRef('http://purl.org/dc/terms/isReplacedBy'), None)):

    if 'https://homosaurus.org/v3/' in s and 'https://homosaurus.org/v3/' in o:
        replace_mapping[s] = o

for s, p, o in g_homosaurus_v3_replaces.triples((None, URIRef('http://purl.org/dc/terms/replaces'), None)):
    if 'https://homosaurus.org/v3/' in s and 'https://homosaurus.org/v3/' in o:
        replace_mapping[o] = s

print('# replace = ',len(replace_mapping))

# add to outdated_qlit_entities_mapping_to_homosaurus
flag = True

for s in qlit_entities_mapping_to_homosaurus.keys():
    t = qlit_entities_mapping_to_homosaurus[s]
    if t in replace_mapping.keys():
        outdated_qlit_entities_mapping_to_homosaurus[s] = replace_mapping[t]
    if t in redirected_mapping.keys():
        outdated_qlit_entities_mapping_to_homosaurus[s] = redirected_mapping[t]

print('first round detected outdated = ', len(outdated_qlit_entities_mapping_to_homosaurus))

while flag == True:
    flag = False
    for s in outdated_qlit_entities_mapping_to_homosaurus.keys():
        t = outdated_qlit_entities_mapping_to_homosaurus[s]
        if t in replace_mapping.keys():
            outdated_qlit_entities_mapping_to_homosaurus[s] = replace_mapping[t]
            flag = True
        if t in redirected_mapping.keys():
            outdated_qlit_entities_mapping_to_homosaurus[s] = redirected_mapping[t]
            flag = True


# print outdated_qlit_entities_mapping_to_homosaurus
print('#pairs of outdated QLIT to Homosaurus v3: ', len(outdated_qlit_entities_mapping_to_homosaurus))
print(outdated_qlit_entities_mapping_to_homosaurus)
