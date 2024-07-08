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


predicates = ['http://www.w3.org/2000/01/rdf-schema#label',
'http://www.w3.org/2004/02/skos/core#altLabel'
]

predicates_to_string = {'http://www.w3.org/2000/01/rdf-schema#label':'rdfs:label',
'http://www.w3.org/2004/02/skos/core#altLabel': 'skos:altLabel'}

# load the mapping

mapping_wiki_hv3 = {}

mapping_file = open('Wikidata-Homosaurus_entities_mapping.csv', 'r')
mapping_file_reader = csv.DictReader(mapping_file, delimiter = ',')
for row in mapping_file_reader:
    e_wiki = row['Wikidata_entity']
    e_hv3 = row['Homosaurus_v3_entity']
    mapping_wiki_hv3[e_wiki] = e_hv3



g_integrated = Graph()
g_integrated.parse("../data/wikidata/integrated_labels.nt")

q_res = g_integrated.query(
'''
SELECT ?lang (COUNT(?label) AS ?count)
WHERE {
  ?s ?p ?label .
  BIND(LANG(?label) AS ?lang)
}
GROUP BY ?lang
''')


languages_ct = Counter()
for row in q_res:
    l = str(row.asdict()['lang'])
    c = int(str(row.asdict()['count']))
    languages_ct[l] = c

print ('there are in total ', len(languages_ct), ' languages in Wikidata.')
print (languages_ct.most_common(10)) # [('en', 17575), ('es', 12434), ('fr', 10637), ('de', 10431), ('zh', 10183), ('ja', 9308), ('ru', 8877), ('pt', 8023), ('ar', 7766), ('sv', 7392)]
#
dir = './extracted_multilingual_labels/'
summary_file =  open ('summary_multilingual_labels.csv', mode='w', newline='')
summary_writer = csv.writer(summary_file)
summary_writer.writerow(['Language'] + predicates +['total'] + ['number_of_entities'] + ['labels_per_entity'])
triples_lan = {}

languages  = languages_ct.keys()
# languages = ['en', 'zh', 'es', 'fr', 'da', 'tr']

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
                ?s <predicate> ?label
                FILTER langMatches( lang(?label), "language_code" )
            }
            """
        query = query.replace("language_code", l)
        query = query.replace ('predicate', p)

        qres = g_integrated.query(query)

        for row in qres:

            subj = str(row.s)
            subject = subj

            if subject in mapping_wiki_hv3.keys():
                entities_of_this_language.add(subject)

                predicate = p

                label = str(row.label)

                if subject[0] == 'N':
                    pass
                else:
                    triples_lan[l][p].add((subject, predicate, label))
        # print ('\n******\n',triples_lan[l][p])
        print('\t\t\tfound ', len(triples_lan[l][p]), ' triples')
        size.append(len(triples_lan[l][p]))
    sum_size = sum(size)
    num_entities = len(entities_of_this_language)
    label_per_entity = 0
    if num_entities != 0:
        label_per_entity = sum_size/num_entities

    summary_writer.writerow([l] + size + [sum_size] + [num_entities] + ['%.2f'%label_per_entity])

    # Finally, write all these triples out. 

    for p in predicates:
        h = Graph()
        # print ('\tpredicate = ', p)
        for (subject, predicate, label) in triples_lan[l][p]:
            subject = URIRef(subject)
            predicate = URIRef(predicate)
            object_with_lang = Literal(label, lang=l)

            h.add((subject, predicate, object_with_lang))
        p_string = predicates_to_string[p]

        h.serialize(dir + l + '_'+ p_string + ".nt", format="nt")
        h.close()
