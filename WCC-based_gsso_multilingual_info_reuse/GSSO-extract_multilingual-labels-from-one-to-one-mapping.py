# This file takes advantage of the one-to-one mapping computed
# using the file compute-one-to-one-mapping.py.
# We first load the file and extract the labels of each predicate from Wikidata.
# The extracted labels are stored in the folder ./extracted_multilingual_labels.
# Please note that the extracted labels are for each predicate, each language.
# So there are a lot of files exported.

from collections import Counter
from rdflib import Graph, URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt



g = Graph()

# Parse the OWL file into the Graph
g.parse("../data/GSSO/gsso.owl")


# load the mapping obtained in the previous step
mapping_GSSO_hv3 = {}

mapping_file = open('GSSO-Homosaurus_entities_mapping.csv', 'r')
mapping_file_reader = csv.DictReader(mapping_file, delimiter = ',')
for row in mapping_file_reader:
    e_wiki = row['GSSO_entity']
    e_hv3 = row['Homosaurus_v3_entity']
    mapping_GSSO_hv3[e_wiki] = e_hv3


print ('Overall entities that has a one-to-one mapping with that of Homosaurus.', len(mapping_GSSO_hv3))

print ('Next, we bring the labels of these entities')

# we study the following predicates.
# the narroSynonym was removed in this paper but can be easily added back in the future

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
'http://purl.org/dc/terms/replaces': 'dct:replaces',
'https://www.wikidata.org/wiki/Property:P5191':'wiki:P5191',
'https://www.wikidata.org/wiki/Property:P1813':'wiki:P1813',
'https://schema.org/alternateName':'sdo:alternateName',
'http://www.w3.org/2002/07/owl#annotatedTarget':'owl:annotatedTarget'
}

q_languages_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX wiki: <https://www.wikidata.org/wiki/Property:>
PREFIX sdo: <https://schema.org/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?lang
WHERE {
  ?resource <predicate> ?label .
  FILTER (LANG(?label) != "")
  BIND(LANG(?label) AS ?lang)
}
'''
languages = set()

for p in predicates:

    query = q_languages_template.replace('predicate', p)
    q_result = g.query(query)
    for row in q_result:
        languages.add(row.lang)


print ('there are in total ', len(languages), ' languages regarding the selected predicates for GSSO.')
#
dir = './extracted_multilingual_labels/'
summary_file =  open ('summary_multilingual_labels.csv', mode='w', newline='')
summary_writer = csv.writer(summary_file)
summary_writer.writerow(['Language'] + predicates +['total']+ ['number_of_entities'] + ['labels_per_entity'])
triples_lan = {}

# all the langauges.
for l in languages:
    entities_of_this_language = set()
    print ('processing language: ', l)
    triples_lan[l] = {}
    size = []
    for p in predicates:
        triples_lan[l][p] = set()

        print ('\tFor predicate: ', p)

        query = """
        SELECT ?s ?label
            WHERE {
                ?subj owl:annotatedSource ?s;
                     <predicate> ?label
                FILTER langMatches( lang(?label), "language_code" )
            }
            """
        query = query.replace("language_code", l)
        # print(query)
        query = query.replace ('predicate', p)

        qres = g.query(query)

        for row in qres:

            subj = str(row.s)
            subject = subj
            predicate = p

            label = str(row.label)
            if subject[0] == 'N': # and len (subject) == len('Ndf5533f58cce4ae390f9c0115f514c7c'): # and p == 'http://www.w3.org/2002/07/owl#annotatedTarget':
                pass
            elif subject in mapping_GSSO_hv3.keys():
                triples_lan[l][p].add((subject, predicate, label))
                entities_of_this_language.add(subject)
            else:
                pass

        # print (triples_lan[l][p])

        query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?s ?label
            WHERE {
                ?s <predicate> ?label
                FILTER langMatches( lang(?label), "language_code" )
            }
            """
        query = query.replace("language_code", l)
        query = query.replace ('predicate', p)

        qres = g.query(query)

        for row in qres:

            subj = str(row.s)
            subject = subj


            predicate = p

            label = str(row.label)

            if subject[0] == 'N':
                pass
            elif subject in mapping_GSSO_hv3.keys():
                triples_lan[l][p].add((subject, predicate, label))
                entities_of_this_language.add(subject)
            else:
                pass

        print('\t\t\tfound ', len(triples_lan[l][p]), ' triples')
        size.append(len(triples_lan[l][p]))
    sum_size = sum(size)
    num_entities = len(entities_of_this_language)
    label_per_entity = 0
    if num_entities != 0:
        label_per_entity = sum_size/num_entities

    summary_writer.writerow([l] + size + [sum_size] + [num_entities] + ['%.2f'%label_per_entity])


    # write all these triples out
    for p in predicates:
        h = Graph()
        print ('\tpredicate = ', p)
        for (subject, predicate, label) in triples_lan[l][p]:
            subject = URIRef(subject)
            predicate = URIRef(predicate)
            object_with_lang = Literal(label, lang=l)

            h.add((subject, predicate, object_with_lang))
        p_string = predicates_to_string[p]
        # Serialize the graph to a file
        h.serialize(dir + l + '_'+ p_string + ".nt", format="nt")
        h.close()
