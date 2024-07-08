# This is a simple script that computes the one-to-one mapping from GSSO to Homosaurus.
# A pair of entity from GSSO and Homosaurus should be in the same WCC and they
# are the only one of its kind in the WCC.

from collections import Counter
from rdflib import Graph, URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt




predicates = ['http://www.w3.org/2000/01/rdf-schema#label',
'http://www.w3.org/2004/02/skos/core#altLabel'
]

predicates_to_string = {'http://www.w3.org/2000/01/rdf-schema#label':'rdfs:label',
'http://www.w3.org/2004/02/skos/core#altLabel': 'skos:altLabel'}



# Load all the Wikidata entities

Wikidata_entities = set()

Wikidata_entity_filename = '../data/wikidata/Wikidata_entities.csv'
entity_file = open(Wikidata_entity_filename, 'r')
for l in entity_file.readlines():
    e = l.strip()
    Wikidata_entities.add(e)


print ('loaded ', len (Wikidata_entities), ' Wikidata entities')


mapping_id_Wikidata = {}
mapping_id_Wikidata_v3 = {}

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
            collect_Wikidata_entity.add (l.strip())
    if len(collect_Wikidata_entity) == 1:
        mapping_id_Wikidata[id] = list(collect_Wikidata_entity)[0]

print(' total number of WCC with exactly one Wikidata entity =', len(mapping_id_Wikidata.keys()))

# find the corresponding entity in v3
for id in list(mapping_id_Wikidata.keys()):

    edges_file_name = wcc_dir + str(id) +'_edges.csv'
    edges_file = open(edges_file_name, 'r')

    Wikidata_entity = mapping_id_Wikidata[id]

    collect_entity_v3 = set()
    for l in edges_file.readlines():
        if 'http://www.wikidata.org/entity/' in l.strip():
            l = l.strip().split(',')
            if len(l) == 3:
                subj = l[0]
                if 'homosaurus.org/v3/' in subj:
                    collect_entity_v3.add(subj)
                obj = l[2]
                if 'homosaurus.org/v3/' in obj:
                    collect_entity_v3.add(obj)


    edges_file = open(edges_file_name, 'r')
    for l in edges_file.readlines():
        l = l.strip().split(',')
        if len(l) == 3:
            subj = l[0]
            pred = l[1]
            obj = l[2]

            if 'homosaurus.org/v3/' in subj:
                if 'http://purl.org/dc/terms/isReplacedBy' in pred:
                    # print('-ReplacedBy: ', subj, pred, obj)
                    if subj in collect_entity_v3:
                        collect_entity_v3.remove(subj)
                if 'https://krr.triply.cc/krr/metalink/def/redirectedTo' in pred:
                    # print('-Redirected ', subj, pred, obj)
                    if subj in collect_entity_v3:
                        collect_entity_v3.remove(subj)

            if 'homosaurus.org/v3/' in obj:
                if 'http://purl.org/dc/terms/replaces' in pred:
                    print('-Replaces ', subj, pred, obj)
                    if obj in collect_entity_v3:
                        collect_entity_v3.remove(obj)


    if len(collect_entity_v3) == 1:
        mapping_id_Wikidata_v3[id] = (Wikidata_entity, list(collect_entity_v3)[0])


print ('Overall cases ', len(mapping_id_Wikidata_v3))

# export the mapping.
mapping_file = open('Wikidata-Homosaurus_entities_mapping.csv', 'w')
mapping_file_writer = csv.writer(mapping_file)
mapping_file_writer.writerow(['WCC_ID', 'Wikidata_entity', 'Homosaurus_v3_entity'])
Wikidata_to_latest_v3 = {}

for id in mapping_id_Wikidata_v3.keys():
    (e_wiki, e_v3) = mapping_id_Wikidata_v3 [id]
    mapping_file_writer.writerow([id, e_wiki, e_v3])
    Wikidata_to_latest_v3 [e_wiki] = e_v3

mapping_file.close()

print ('exported the mapping')
