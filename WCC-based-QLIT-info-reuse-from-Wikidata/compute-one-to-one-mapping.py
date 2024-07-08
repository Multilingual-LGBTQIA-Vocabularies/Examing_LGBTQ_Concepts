# This is a simple script that computes the one-to-one mapping from Wikidata to QLIT.
# A pair of entity from Wikidata and QLIT should be in the same WCC and they
# are the only one of its kind in the WCC.

from collections import Counter
from rdflib import Graph, URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt


# load all the Wikidata entities.
Wikidata_entities = set()

Wikidata_entity_filename = '../data/wikidata/Wikidata_entities.csv'
entity_file = open(Wikidata_entity_filename, 'r')
for l in entity_file.readlines():
    e = l.strip()
    Wikidata_entities.add(e)


print ('loaded ', len (Wikidata_entities), ' Wikidata entities')


# load the WCC
mapping_id_Wikidata = {}
mapping_id_Wikidata_qlit = {}

wcc_dir = '../integrated_data/weakly_connected_components/'

# for each WCC, we compute the mapping from Wikidata to its coresponding ID
# of WCC.

for id in range (6406):
    collect_Wikidata_entity = set()
    # print ('processing ', id )
    node_file_name = wcc_dir + str(id) +'_entities.csv'
    entity_file = open(node_file_name, 'r')
    for l in entity_file.readlines():
        # print (l.strip())
        if 'www.wikidata.org/entity/' in l.strip():
            collect_Wikidata_entity.add (l.strip())# += 1
    if len(collect_Wikidata_entity) == 1:
        mapping_id_Wikidata[id] = list(collect_Wikidata_entity)[0]

print(' total number of WCC with exactly one Wikidata entity =', len(mapping_id_Wikidata.keys()))

# for id in mapping_id_Wikidata.keys():
#     wiki_e =  mapping_id_Wikidata[id]
#     print (id, ': ', wiki_e)


# find the corresponding entity in QLIT
for id in list(mapping_id_Wikidata.keys()):

    edges_file_name = wcc_dir + str(id) +'_edges.csv'
    edges_file = open(edges_file_name, 'r')

    Wikidata_entity = mapping_id_Wikidata[id]

    collect_entity_qlit = set()
    for l in edges_file.readlines():
        if 'http://www.wikidata.org/entity/' in l.strip():
            l = l.strip().split(',')
            if len(l) == 3:
                subj = l[0]
                if 'https://queerlit.dh.gu.se/qlit/v1/' in subj:
                    collect_entity_qlit.add(subj)
                obj = l[2]
                if 'https://queerlit.dh.gu.se/qlit/v1/' in obj:
                    collect_entity_qlit.add(obj)

    # if there is exactly one QLIT in that WCC, then we add them as a pair to the
    # mapping.
    if len(collect_entity_qlit) == 1:
        mapping_id_Wikidata_qlit[id] = (Wikidata_entity, list(collect_entity_qlit)[0])


print ('Overall cases ', len(mapping_id_Wikidata_qlit))

# Finally, we export this mapping for the use in the next step. 
mapping_file = open('Wikidata-QLIT_entities_mapping.csv', 'w')
mapping_file_writer = csv.writer(mapping_file)
mapping_file_writer.writerow(['WCC_ID', 'Wikidata_entity', 'QLIT_entity'])
Wikidata_to_latest_v3 = {}

for id in mapping_id_Wikidata_qlit.keys():
    (e_wiki, e_v3) = mapping_id_Wikidata_qlit [id]
    mapping_file_writer.writerow([id, e_wiki, e_v3])
    Wikidata_to_latest_v3 [e_wiki] = e_v3

mapping_file.close()

print ('exported the mapping')
