from rdflib import Graph, URIRef
from collections import Counter
import csv

g = Graph()
g.parse("../integrated_data/integrated.nt")


collect_wiki_entities = set()

for (s, p, o) in g:
    if 'http://www.wikidata.org/entity/Q' in s:
        collect_wiki_entities.add(str(s))
    if 'http://www.wikidata.org/entity/Q' in o:
        collect_wiki_entities.add(str(o))


print ('in total, there are ', len (collect_wiki_entities), ' entities')
wikidata_entity_list =  open ('Wikidata_entities.csv', mode='w', newline='')
wikidata_entity_list_writer = csv.writer(wikidata_entity_list)
for e in collect_wiki_entities:
    wikidata_entity_list_writer.writerow([e])
