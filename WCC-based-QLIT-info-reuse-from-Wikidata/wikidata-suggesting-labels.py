# This is the last step to get the suggesting labels from Wikidata.
# It takes the extracted multilingual labels from previous step and outputs
# the labels together with existing labels.
# the output is a csv file that can be easily converted to Excel sheets for
# further manual annotaion.

# The output is a file in the folder sugggestiong_information/
# Given that QLIT is only Swedish (sv), we export only the Swedish labels.

from collections import Counter
from rdflib import Graph, URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt


# load the one-to-one mapping from Wikidata to QLIT.
Wikidata_to_QLIT = {}

# Read the Wikdata-QLIT mapping
f = 'Wikidata-QLIT_entities_mapping.csv'
input_file = csv.DictReader(open(f), delimiter=',')
for row in input_file:
    # print('subject = ', row['subject'])
    # print('label = ', row['label'])
    # print('lang = ', row['lang'])
    w = row['Wikidata_entity']
    e = row['QLIT_entity']
    Wikidata_to_QLIT[w] = e


print ('#pairs loaded ', len(Wikidata_to_QLIT))

# only relations corresponding to two predicates have been extracted from Wikidata.
predicates = ['http://www.w3.org/2000/01/rdf-schema#label',
'http://www.w3.org/2004/02/skos/core#altLabel'
]

predicates_to_string = {'http://www.w3.org/2000/01/rdf-schema#label':'rdfs:label',
'http://www.w3.org/2004/02/skos/core#altLabel': 'skos:altLabel'}


dir = './extracted_multilingual_labels/'

# all the labels are going to be exported in this folder
export_dir = './suggesting_information/'


graph_QLIT = Graph()
graph_QLIT.parse('../data/QLIT/Qlit-v1.ttl')

# Given that only one langauges is going considered, this list contains only
# sv: the ISO 639-1 Language Code for Swedish.
languages = ['sv']

for l in languages:
    # prepare the file and write the first row.
    summary_file =  open (export_dir + 'suggesting_info_summary_from_Wikidata_to_QLIT_'+ l + '.csv', mode='w', newline='')
    summary_writer = csv.writer(summary_file)
    summary_writer.writerow(['Wikidata_Entity'] + list(predicates_to_string.values()) + ['Entities_in_graph_QLIT'] + ['prefLabel_in_English_in_graph_QLIT', 'altLabel_in_English_in_graph_QLIT'])

    print ('\nprocessing langauge ', l)
    g_l = Graph()
    # store the resulting pred, label for each replaced Wikidata/QLIT term
    collect_QLIT_subj = set()

    for p in predicates:
        p_string = predicates_to_string[p]
        filename = dir + l + '_'+ p_string + ".nt"
        g_tmp = Graph()
        g_tmp.parse(filename)
        g_l = g_l + g_tmp
        g_tmp.close()

    num_triples_l = len(g_l)

    print ('in total there are ', num_triples_l, ' triples about labels')

    count_exported_lines = 0
    count_overall_labels = 0

    # go through the entities in the mapping.
    # for each pair, g is the entity of Wikidata
    # and h is the entity for QLIT.
    for g in Wikidata_to_QLIT.keys():
        h = Wikidata_to_QLIT[g]
        collect_QLIT_subj.add(h)
        # the labels are collected in the dictionary
        pred_to_labels = {}
        pred_labels_list = []

        for p in predicates:
            for (_, _, obj_label) in g_l.triples((URIRef(g), URIRef(p), None)):
                label = str(obj_label)
                if p in pred_to_labels.keys():
                    pred_to_labels[p].append(label)
                else:
                    pred_to_labels[p] = [label]
            if p not in pred_to_labels.keys():
                pred_to_labels[p] = []
            pred_labels_list.append(pred_to_labels[p])



        prefL = 'http://www.w3.org/2004/02/skos/core#prefLabel'
        altL = 'http://www.w3.org/2004/02/skos/core#altLabel'

        # collect the prefLabels
        preflabels = []
        flag = False
        for (_, _, label) in graph_QLIT.triples((URIRef(h), URIRef(prefL), None)):
            preflabels.append(str(label))

        # collect the altLabels
        altlabels = []
        for (_, _, label) in graph_QLIT.triples((URIRef(h), URIRef(altL), None)):
            altlabels.append(str(label))

        # count all the collected labels
        flag = False
        for pl in pred_labels_list:
            if pl != []:
                flag = True
                count_overall_labels += len(pl)

        # if there are labels collected, then we write the collected labels in the files.
        if flag :
            summary_writer.writerow([g] + pred_labels_list + [h] + [preflabels] + [altlabels])
            count_exported_lines += 1

    # Finally, we print some statistics about these labels.
    print ('for language ', l, ' there are ', count_exported_lines, ' exported')
    if count_exported_lines != 0:
        print ('average suggested label per entity: ', count_overall_labels/count_exported_lines)
