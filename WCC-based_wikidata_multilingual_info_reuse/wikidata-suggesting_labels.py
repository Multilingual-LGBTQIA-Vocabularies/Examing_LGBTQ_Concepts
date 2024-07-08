# This is the last step to get the suggesting labels from Wikidata.
# It takes the extracted multilingual labels from previous step and outputs
# the labels together with existing labels.
# the output is a csv file that can be easily converted to Excel sheets for
# further manual annotaion.


# The output is a file in the folder sugggestiong_information/

from collections import Counter
from rdflib import Graph, URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt



Wikidata_to_latest_v3 = {}

# Read the Wikdata-Homosaurus v3 mapping
f = 'Wikidata-Homosaurus_entities_mapping.csv'
input_file = csv.DictReader(open(f), delimiter=',')
for row in input_file:
    # print('subject = ', row['subject'])
    # print('label = ', row['label'])
    # print('lang = ', row['lang'])
    w = row['Wikidata_entity']
    e = row['Homosaurus_v3_entity']
    Wikidata_to_latest_v3[w] = e


print ('#pairs loaded ', len(Wikidata_to_latest_v3))

predicates = ['http://www.w3.org/2000/01/rdf-schema#label',
'http://www.w3.org/2004/02/skos/core#altLabel'
]

predicates_to_string = {'http://www.w3.org/2000/01/rdf-schema#label':'rdfs:label',
'http://www.w3.org/2004/02/skos/core#altLabel': 'skos:altLabel'}


dir = './extracted_multilingual_labels/'
export_dir = './suggesting_information/'


homosaurus_v3 = Graph()
homosaurus_v3.parse('../data/Homosaurus/v3.ttl')

homosaurus_v2 = Graph()
homosaurus_v2.parse('../data/Homosaurus/v2.ttl')

languages = ['en', 'fr', 'es', 'da', 'de', 'zh']




for l in languages:

    summary_file =  open (export_dir + 'suggesting_info_summary_from_Wikidata_to_Homosaurus_'+ l + '.csv', mode='w', newline='')
    summary_writer = csv.writer(summary_file)
    summary_writer.writerow(['Wikidata_Entity'] + list(predicates_to_string.values()) + ['Entities_in_Homosaurus_V3'] + ['prefLabel_in_English_in_Homosaurus_v3', 'altLabel_in_English_in_Homosaurus_v3'])

    print ('\nprocessing langauge ', l)
    g_l = Graph()
    # store the resulting pred, label for each replaced Wikidata/homosaurus term
    collect_homo_subj = set()

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
    for g in Wikidata_to_latest_v3.keys():
        h = Wikidata_to_latest_v3[g]
        # print ('Wikidata: ', g)
        # print ('Found Hv3: ', h)
        collect_homo_subj.add(h)
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

        preflabels = []
        flag = False
        # if 'homoit0000107' in h: # https://homosaurus.org/v3/homoit0000107
        #     print ('processing it: ', h)
        #     flag = True

        for (_, _, label) in homosaurus_v3.triples((URIRef(h), URIRef(prefL), None)):
            preflabels.append(str(label))
        # if flag:
        #     print ('prefL: ', preflabels)

        altlabels = []
        for (_, _, label) in homosaurus_v3.triples((URIRef(h), URIRef(altL), None)):
            altlabels.append(str(label))
        # if flag:
        #     print ('altL: ', altlabels)
        flag = False

        for pl in pred_labels_list:
            if pl != []:
                flag = True
                count_overall_labels += len(pl)

        if flag :
            summary_writer.writerow([g] + pred_labels_list + [h] + [preflabels] + [altlabels])
            count_exported_lines += 1

    print ('for language ', l, ' there are ', count_exported_lines, ' exported')
    if count_exported_lines != 0:
        print ('average suggested label per entity: ', count_overall_labels/count_exported_lines)
