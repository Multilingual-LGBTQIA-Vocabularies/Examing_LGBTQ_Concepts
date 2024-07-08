
from SPARQLWrapper import SPARQLWrapper, JSON
import validators
from rdflib import Graph, URIRef, Literal



# load all Wikidata entities
Wikidata_entities = []

Wikidata_entity_filename = './Wikidata_entities.csv'
entity_file = open(Wikidata_entity_filename, 'r')
for l in entity_file.readlines():
    e = l.strip()
    if len(e) > 1:
        Wikidata_entities.append(e)


print ('loaded ', len (Wikidata_entities), ' Wikidata entities')
print ('last one:', Wikidata_entities[-1])


# The SPARQL endpoint is
# https://query.wikidata.org/

# Wikidata - Wikidata:          http://www.wikidata.org/prop/direct/P9827
# Wikidata - Homosaurus 2:  http://www.wikidata.org/prop/direct/P6417
# Wikidata - Homosaurus 3:  http://www.wikidata.org/prop/direct/P10192
# Wikidata - LCSH:          http://www.wikidata.org/prop/direct/P244

# https://www.wikidata.org/wiki/Property:P8419 Archive of Our Own tag


sparql = SPARQLWrapper(
    "https://query.wikidata.org/sparql"
)
sparql.setReturnFormat(JSON)



dir = './extracted_multilingual_labels/'

query_template = '''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?subject ?label ?lang
WHERE {
Values ?subject {
    <subject_list>
  }
  ?subject <<predicate>> ?label.
  BIND(LANG(?label) AS ?lang)
}
'''

predicates = [
'http://www.w3.org/2000/01/rdf-schema#label', 'http://schema.org/description', 'http://www.w3.org/2004/02/skos/core#altLabel'
]

extra_labels_wikidta_filename = 'wikidata-extracted-labels.nt'

Graph_extracted_labels = Graph()
# mapping_pred_label = {}

for p in predicates:
    query_pred = query_template.replace("<predicate>", p)
    print ('working on predicate: ', p)

    subj_list = ['<' + e + '>' for e in Wikidata_entities]
    subj_list = '\n'.join(list(subj_list))

    query = query_pred.replace('<subject_list>', subj_list)

    print(query)


    sparql.setQuery(query)


    # try:
    #     ret = sparql.queryAndConvert()
    #
    #     for r in ret["results"]["bindings"]:
    #         pred = p
    #         # if 'alternateName' in pred or 'prefLabel' in pred:
    #         #     print (pred)
    #         subject = r['subject']['value']
    #         label = r['label']['value']
    #         lang = r['lang']['value']
    #
    #         subject = URIRef(e)
    #         predicate = URIRef(pred)
    #
    #         if lang != '':
    #             object_with_lang = Literal(label, lang=lang)
    #             Graph_extracted_labels.add((subject, predicate, object_with_lang))
    #         else:
    #             object_with_lang = Literal(label)
    #             Graph_extracted_labels.add((subject, predicate, object_with_lang))
    #
    # except Exception as ex:
    #     # print (e)
    #     print (ex)
    #     raise


Graph_extracted_labels.serialize(extra_labels_wikidta_filename, format="nt")
Graph_extracted_labels.close()














#
