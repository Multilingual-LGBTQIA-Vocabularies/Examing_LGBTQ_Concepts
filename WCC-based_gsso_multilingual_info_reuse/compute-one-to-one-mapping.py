# This is a simple script that computes the one-to-one mapping from GSSO to Homosaurus.
# A pair of entity from GSSO and Homosaurus should be in the same WCC and they
# are the only one of its kind in the WCC.

from collections import Counter
from rdflib import Graph, URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt

# Load all the GSSO entities

GSSO_entities = set()

GSSO_entity_filename = '../data/GSSO/GSSO_entities.csv'
entity_file = open(GSSO_entity_filename, 'r')
for l in entity_file.readlines():
    e = l.strip()
    GSSO_entities.add(e)


print ('loaded ', len (GSSO_entities), ' GSSO entities')


mapping_id_GSSO = {}
mapping_id_GSSO_v3 = {}

wcc_dir = '../integrated_data/weakly_connected_components/'

# for each WCC, we compute the mapping from GSSO to its coresponding ID
# of WCC.


for id in range (6406):
    collect_GSSO_entity = set()
    # print ('processing ', id )
    node_file_name = wcc_dir + str(id) +'_entities.csv'
    entity_file = open(node_file_name, 'r')
    for l in entity_file.readlines():
        # print (l.strip())
        if l.strip() in GSSO_entities:
            collect_GSSO_entity.add (l.strip())
    if len(collect_GSSO_entity) == 1:
        mapping_id_GSSO[id] = list(collect_GSSO_entity)[0]

print(' total number of WCC with exactly one GSSO entity =', len(mapping_id_GSSO.keys()))

# find the corresponding entity in Homosaurus v3
for id in list(mapping_id_GSSO.keys()):

    edges_file_name = wcc_dir + str(id) +'_edges.csv'
    edges_file = open(edges_file_name, 'r')

    GSSO_entity = mapping_id_GSSO[id]

    collect_entity_v3 = set()
    for l in edges_file.readlines():
        l = l.strip().split(',')
        if len(l) == 3:
            subj = l[0].strip()
            obj = l[2].strip()
            if subj in GSSO_entities or obj in GSSO_entities:
                if 'homosaurus.org/v3/' in subj:
                    collect_entity_v3.add(subj)

                if 'homosaurus.org/v3/' in obj:
                    collect_entity_v3.add(obj)


    edges_file = open(edges_file_name, 'r')
    for l in edges_file.readlines():
        l = l.strip().split(',')
        if len(l) == 3:
            subj = l[0].strip()
            pred = l[1].strip()
            obj = l[2].strip()

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
        mapping_id_GSSO_v3[id] = (GSSO_entity, list(collect_entity_v3)[0])


print ('Overall cases ', len(mapping_id_GSSO_v3))

mapping_file = open('GSSO-Homosaurus_entities_mapping.csv', 'w')
mapping_file_writer = csv.writer(mapping_file)
mapping_file_writer.writerow(['WCC_ID', 'GSSO_entity', 'Homosaurus_v3_entity'])
GSSO_to_latest_v3 = {}

for id in mapping_id_GSSO_v3.keys():
    (e_wiki, e_v3) = mapping_id_GSSO_v3 [id]
    mapping_file_writer.writerow([id, e_wiki, e_v3])
    GSSO_to_latest_v3 [e_wiki] = e_v3

mapping_file.close()

print ('exported the mapping')
