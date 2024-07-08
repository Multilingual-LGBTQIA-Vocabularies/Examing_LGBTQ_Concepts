# this file export multilingual labels
# there are 64 languages under examination. These
# langauges are with labels in GSSO.
# However, our examination shows that not all of
# them are labels with respect to our selected predicates
# the result is summarized in the file summary_multilingual.csv

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv

g = Graph()

# Parse the OWL file into the Graph
g.parse("../data/GSSO/gsso.owl")

q_languages = g.query(
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?lang
WHERE {
  ?resource rdfs:label ?label .
  FILTER (LANG(?label) != "")
  BIND(LANG(?label) AS ?lang)
}
''')

languages = []
for  l in q_languages:
    # print (l[0])
    # print (str(l[0]))
    languages.append(str(l[0]))

print ('There are', len(languages), 'languages. They are: ', languages)

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


predicates_to_ignore = [
'http://purl.org/dc/elements/1.1/title',
'http://purl.org/dc/elements/1.1/publisher'
]

triples_lan = {}

# <https://web.archive.org/web/20190216221625/http://transhealth.ucsf.edu/pdf/Transgender-PGACG-6-17-16.pdf> <https://schema.org/datePublished> "2016-06-17T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
# <http://purl.obolibrary.org/obo/GSSO_010998> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .
dir = './extracted_multilingual_labels/'
summary_file =  open ('summary_multilingual.csv', mode='w', newline='')
summary_writer = csv.writer(summary_file)
summary_writer.writerow(['Language'] + predicates +['total'])

for l in languages:
    print ('processing language: ', l)
    triples_lan[l] = {}
    size = []
    for p in predicates:
        triples_lan[l][p] = set()

        print ('\tFor predicate: ', p)

        query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX wiki: <https://www.wikidata.org/wiki/>

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
            else:
                triples_lan[l][p].add((subject, predicate, label))

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

            if subject[0] == 'N': # and len (subject) == len('Ndf5533f58cce4ae390f9c0115f514c7c'): # and p == 'http://www.w3.org/2002/07/owl#annotatedTarget':
                pass
            else:
                triples_lan[l][p].add((subject, predicate, label))
        # print ('\n******\n',triples_lan[l][p])
        print('\t\t\tfound ', len(triples_lan[l][p]), ' triples')
        size.append(len(triples_lan[l][p]))
    sum_size = sum(size)
    summary_writer.writerow([l] + size + [sum_size])

# write all these triples out
for l in languages:
    print ('language = ', l)
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
        # f = open(dir + l + '_'+ p_string + ".nt", 'w')
        # f.close()
        h.serialize(dir + l + '_'+ p_string + ".nt", format="nt")
        h.close()
        # write triples_lan[l][p]

#
# # Missed:  Ndf5533f58cce4ae390f9c0115f514c7c http://www.geneontology.org/formats/oboInOwl#hasExactSynonym etre dans le placard
# # Missed:  Na536e759b4cd4a52830bacfb72992acb http://www.w3.org/2002/07/owl#annotatedTarget minorités sexuelles et de genre
# # Missed:  Nc146d44b8e11415b9049cb137b83770d https://schema.org/alternateName bardaches
#
# french_label = set()
# french_RelatedSynonym = set()
# french_NarrowSynonym = set()
# french_hasSynonym = set() # http://www.geneontology.org/formats/oboInOwl#hasSynonym
# french_hasExactSynonym = set() # http://www.geneontology.org/formats/oboInOwl#hasExactSynonym
# french_replaces = set() # http://purl.org/dc/terms/replaces
# french_derivedFromLexeme = set()# https://www.wikidata.org/wiki/Property:P5191
# french_shortName = set() # https://www.wikidata.org/wiki/Property:P1813
# french_alternateName = set() # https://schema.org/alternateName
#
# # for s, p ,o in g:
# #     if 'Ndf5533f58cce4ae390f9c0115f514c7c' in s:
# #         print (s, p, o)
#
# for row in qres:
#
#
#     subj = str(row.s)
#     subject = subj
#
#     pred = str(row.p)
#     predicate = pred
#
#     label = str(row.label)
#
#     try:
#         if 'http://www.w3.org/2002/07/owl#annotatedTarget' in row.p:
#             if subj in map_sub_subject.keys():
#                 subject = map_sub_subject[subj]
#                 if subj in map_sub_pred.keys():
#                     predicate = map_sub_pred[subj]
#
#
#     except Exception as e:
#         print ('this triple has problem: ', subj, pred, obj)
#         print (e)
#
#
#     # if str(row.s) in all_subjects:
#
#     if 'http://www.w3.org/2000/01/rdf-schema#label' in predicate:
#         french_label.add ((subject, predicate, label))
#     elif 'http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym' in predicate:
#         french_RelatedSynonym.add((subject, predicate, label))
#     elif 'http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym' in predicate:
#         french_NarrowSynonym.add((subject, predicate, label))
#     elif 'http://www.geneontology.org/formats/oboInOwl#hasSynonym' in predicate:
#         french_hasSynonym.add((subject, predicate, label))
#     elif 'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym' in predicate:
#         french_hasExactSynonym.add((subject, predicate, label))
#     elif 'http://purl.org/dc/terms/replaces' in predicate:
#         french_replaces.add((subject, predicate, label))
#     elif 'https://www.wikidata.org/wiki/Property:P5191' in predicate:
#         french_derivedFromLexeme.add((subject, predicate, label))
#     elif 'https://www.wikidata.org/wiki/Property:P1813' in predicate:
#         french_shortName.add((subject, predicate, label))
#     elif 'https://schema.org/alternateName' in predicate:
#         french_alternateName.add((subject, predicate, object))
#     elif 'http://purl.org/dc/elements/1.1/title' in predicate or 'http://purl.org/dc/elements/1.1/publisher' in predicate: # usually a publication. Nothing to do with terms
#         pass
#     else:
#         print('Missed: ', row.s, row.p, row.label)
#
# print ('There are ', len(french_label), ' rdf:labels in French')
# print ('There are ', len(french_alternateName), ' sdo:alternateName in French')
# print ('There are ', len(french_RelatedSynonym), ' oboInOwl:RelatedSynonym in French')
# print ('There are ', len(french_NarrowSynonym), ' oboInOwl:NarrowSynonym in French')
# print ('There are ', len(french_hasSynonym), ' oboInOwl:hasSynonym in French')
# print ('There are ', len(french_hasExactSynonym), ' oboInOwl:french_hasExactSynonym in French')
# print ('There are ', len(french_replaces), ' dc:replaces in French')
# print ('There are ', len(french_derivedFromLexeme), ' wikidata:derivedFromLexeme in French')
# print ('There are ', len(french_shortName), ' wikidata:shortName in French')
#
# french_all = set()
# french_all = french_all.union(french_label)
# french_all = french_all.union(french_RelatedSynonym)
# french_all = french_all.union(french_NarrowSynonym)
# french_all = french_all.union(french_hasSynonym) # http://www.geneontology.org/formats/oboInOwl#hasSynonym
# french_all = french_all.union(french_hasExactSynonym) # http://www.geneontology.org/formats/oboInOwl#hasExactSynonym
# french_all = french_all.union(french_replaces) # http://purl.org/dc/terms/replaces
# french_all = french_all.union(french_derivedFromLexeme)# https://www.wikidata.org/wiki/Property:P5191
# french_all = french_all.union(french_shortName) # https://www.wikidata.org/wiki/Property:P1813
# french_all = french_all.union(french_alternateName) # https://schema.org/alternateName
# print('There are in total ', len (french_all), ' triples about Fench')
#
#
# for (s, p ,o) in french_all:
#     print(s,p,o)
#
# # N67bc7f3f26a1465f9d9bb07b68fbb5e4 https://www.wikidata.org/wiki/Property:P1813 DSPG
# # N56a1493990c74255ad98fa132bcab859 https://www.wikidata.org/wiki/Property:P5191 cacher
# # N56a1493990c74255ad98fa132bcab859 https://www.wikidata.org/wiki/Property:P5191 sexe
# # N746685b2e05e441cb7e2989e0d9943e5 https://www.wikidata.org/wiki/Property:P5191 insurrection
