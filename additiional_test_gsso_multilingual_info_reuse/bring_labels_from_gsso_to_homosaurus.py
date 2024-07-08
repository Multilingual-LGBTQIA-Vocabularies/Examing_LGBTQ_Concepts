# Here we bring the labels from outdated mapping from GSSO -> v2 of Homosaurus
# to v3 of Homosaurus. We do this with a focus on the following languages:
# English: a total of 54,273 label information about GSSO terms was found.
# Turkish: a total of 103 label information about GSSO terms was found.
# Spanish: a total of 207 label information about GSSO terms was found.
# French: a total of 292 label information about GSSO terms was found.
# Danish: a total of 593 label information about GSSO terms was found.
# Latin: a total of 593 label information about GSSO terms was found.

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv

predicates = ['http://www.w3.org/2000/01/rdf-schema#label',
'http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym',
# 'http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym',
'http://purl.org/dc/terms/replaces',
'https://www.wikidata.org/wiki/Property:P5191',
'https://www.wikidata.org/wiki/Property:P1813',
'https://schema.org/alternateName',
'http://www.w3.org/2002/07/owl#annotatedTarget'
]

predicates_to_string = {'http://www.w3.org/2000/01/rdf-schema#label':'rdfs:label',
'http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym': 'oboInOwl:hasRelatedSynonym',
# 'http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym':'oboInOwl:hasNarrowSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasSynonym':'oboInOwl:hasSynonym',
'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym':'oboInOwl:hasExactSynonym',
'http://purl.org/dc/terms/replaces': 'dc:replaces',
'https://www.wikidata.org/wiki/Property:P5191':'wiki:P5191',
'https://www.wikidata.org/wiki/Property:P1813':'wiki:P1813',
'https://schema.org/alternateName':'sdo:alternateName',
'http://www.w3.org/2002/07/owl#annotatedTarget':'owl:annotatedTarget'
}

# First, we load the two mapping files
g_gsso_to_v2 = Graph()
g_gsso_to_v2.parse ("../data/GSSO/mapping_to_v2.nt")

g_gsso_to_v3 = Graph()
g_gsso_to_v3.parse ("../data/GSSO/mapping_to_v3.nt")


# find the longest path of identifier
# <http://purl.org/dc/elements/1.1/identifier>
# <https://schema.org/identifier>


g_homosaurus_v2_replaces = Graph()
g_homosaurus_v2_replaces.parse ("../data/Homosaurus/replace_relations_homosaurus/v2_replace_links.nt")

g_homosaurus_v3_replaces = Graph()
g_homosaurus_v3_replaces.parse ("../data/Homosaurus/replace_relations_homosaurus/v3_replace_links.nt")


# load info from replace_summary.csv

collect_all =[] # .append((x, nodes_in_path_v2, nodes_in_path_v3, latest_nodes_v3))
# ['GSSO Entity', 'Entities in Homosaurus V2', 'Entities in Homosaurus V3', 'Latest Entities in Homosaurus V3'])

gsso_to_latest_v3 = {}
with open('replace_summary.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print('\n\t', row['GSSO Entity'], row['Latest Entities in Homosaurus V3'])
        # latest_entities_v3 =  row['Latest Entities in Homosaurus V3'][1:-1].split(',')
        latest_entities_v3 =  row['Latest (Redirected) Entities in Homosaurus V3'][1:-1].split(',')

        latest_entities_v3 = [ n.strip()[1:-1] for n in  latest_entities_v3]
        # print (latest_entities_v3)
        gsso_to_latest_v3[row['GSSO Entity']] = latest_entities_v3

print('number of entities in GSSO in this mapping = ', len(gsso_to_latest_v3.keys()))

# print (list(gsso_to_latest_v3.keys())[:5])

languages = ['en', 'tr', 'es', 'fr', 'da', 'la']

dir = './extracted_multilingual_labels/'
export_dir = './suggesting_information/'

homosaurus_v3 = Graph()
homosaurus_v3.parse('../data/Homosaurus/v3.ttl')

homosaurus_v2 = Graph()
homosaurus_v2.parse('../data/Homosaurus/v2.ttl')


for l in languages:

    summary_file =  open (export_dir + 'suggesting_info_summary_from_GSSO_to_Homosaurus_'+ l + '.csv', mode='w', newline='')
    summary_writer = csv.writer(summary_file)
    summary_writer.writerow(['GSSO_Entity'] + list(predicates_to_string.values()) + ['Entities_in_Homosaurus_V3'] + ['prefLabel_in_English_in_Homosaurus_v3', 'altLabel_in_English_in_Homosaurus_v3'])

    print ('\nprocessing langauge ', l)
    g_l = Graph()
    # store the resulting pred, label for each replaced gsso/homosaurus term
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
    for g in gsso_to_latest_v3.keys():
        if (len(gsso_to_latest_v3[g])) == 1:
            h = list(gsso_to_latest_v3[g])[0]
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
    print ('There are in total ', count_overall_labels, ' labels exported for language ', l)
    print ('for language ', l, ' there are ', count_exported_lines, ' entities with labels exported')
    print ('average suggested label per entity: ', count_overall_labels/count_exported_lines)

# python bring_labels_from_gsso_to_homosaurus.py
# number of entities in GSSO in this mapping =  1104
#
# processing langauge  en
# in total there are  51931  triples about labels
# for language  en  there are  1006  exported
# average suggested label per entity:  5.526838966202783
#
# processing langauge  tr
# in total there are  103  triples about labels
# for language  tr  there are  23  exported
# average suggested label per entity:  3.0
#
# processing langauge  es
# in total there are  205  triples about labels
# for language  es  there are  43  exported
# average suggested label per entity:  2.116279069767442
#
# processing langauge  fr
# in total there are  277  triples about labels
# for language  fr  there are  47  exported
# average suggested label per entity:  2.1914893617021276
#
# processing langauge  da
# in total there are  592  triples about labels
# for language  da  there are  115  exported
# average suggested label per entity:  2.2695652173913046
#
# processing langauge  la
# in total there are  105  triples about labels
# for language  la  there are  9  exported
# average suggested label per entity:  1.0
