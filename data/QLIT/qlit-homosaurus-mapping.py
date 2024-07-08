# this file exports the mappings between QLIT and homosaurus

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx


qlit = Graph()
qlit.parse ("./Qlit-v1.ttl")

G2 = Graph()
G3 = Graph()
h2_entities = set()
h3_entities = set()

count_v2 = 0
count_v3 = 0

count_exactMatch_v3 = 0
count_closeMatch_v3 = 0

qlit_entities_has_mapping_homosaurus = set()
qlit_entities_all = set()

for s, p, o in qlit.triples ((None, None, None)):
    if  'queerlit.dh.gu.se/qlit/' in str(s):
        qlit_entities_all.add(str(s))
    if  'queerlit.dh.gu.se/qlit/' in str(o):
        qlit_entities_all.add(str(o))


for subj_qlit, p, obj_h_v2 in qlit.triples ((None, None, None)):
    if ('homosaurus.org/v2/' in str(obj_h_v2)):
        if str(subj_qlit) in qlit_entities_all:
            qlit_entities_has_mapping_homosaurus.add(str(subj_qlit))
            count_v2 += 1
            G2.add((URIRef(subj_qlit), URIRef(p), URIRef(obj_h_v2)))
            h2_entities.add(str(subj_qlit))
    elif ('homosaurus.org/v2/' in str(subj_qlit)):
        print ('subj_qlit = ', subj_qlit)



for subj_qlit, p, obj_h_v3 in qlit.triples ((None, None, None)):
    if ('homosaurus.org/v3/' in str(obj_h_v3)):
        if str(subj_qlit) in qlit_entities_all:
            qlit_entities_has_mapping_homosaurus.add(str(subj_qlit))
            count_v3 += 1
            G3.add((URIRef(subj_qlit), URIRef(p), URIRef(obj_h_v3)))
            h3_entities.add(str(subj_qlit))

            if 'exactMatch' in p:
                count_exactMatch_v3 += 1
            if 'closeMatch' in p:
                count_closeMatch_v3 += 1

# finally, we print those that do have a mapping to homosaurus v2 or v3
# for subj_qlit, p, obj in qlit.triples ((None, None, None)):
#     if str(subj_qlit) not in h3_entities and str(subj_qlit) not in h2_entities:
#         if 'prefLabel' in str(p):
#             print (subj_qlit, str(obj))

print  ('There are in total ', len(qlit_entities_all), ' entities in QLIT')
print ('Num of entities that has mapping to Homosaurus: ', len(qlit_entities_has_mapping_homosaurus))
print ('Num of triples, mapped to v2 ' , count_v2)
print ('Num of triples, mapped to v3 ' , count_v3)
print ('\tNum of exactMatch to v3 ', count_exactMatch_v3)
print ('\tNum of closeMatch to v3 ', count_closeMatch_v3)

print ('# entities in QLIT not mapped to h2 or h3: ', len(qlit_entities_all.difference(qlit_entities_has_mapping_homosaurus)))
#
dir = './mapping/'
# export_v2
f = open(dir+'qlit_mapping_to_v2.nt', 'w')
G2.serialize(dir + 'qlit_mapping_to_v2.nt', format="nt")
f.close()

# export_v3
f = open(dir+'qlit_mapping_to_v3.nt', 'w')
G3.serialize(dir + 'qlit_mapping_to_v3.nt', format="nt")
f.close()
