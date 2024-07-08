# this short srcript tests how outdated are the links to Homosaurus.

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx

export_dir = './'

raw_wikidata_to_v2 = Graph()
raw_wikidata_to_v2.parse ("./wikidata-homosaurus-v2-links.ttl")

wikidata_to_v2 = Graph()
for s, p, o in raw_wikidata_to_v2:
    # if 'https://schema.org/identifier' in pred:
    #     print ('sdo:identifier: ',subj, pred, obj)

    subj = str(s)
    obj = 'http://homosaurus.org/v2/'+ str(o)
    pred = str(p)
    wikidata_to_v2.add((s, p, URIRef(obj)))


wikidata_to_v2.serialize(export_dir + 'wikidata-homosaurus-v2-links-with-prefix.nt', format = 'nt') # export_dir
wikidata_to_v2.close()


raw_wikidata_to_v3 = Graph()
raw_wikidata_to_v3.parse ("./wikidata-homosaurus-v3-links.ttl")

wikidata_to_v3 = Graph()
for s, p, o in raw_wikidata_to_v3:
    # if 'https://schema.org/identifier' in pred:
    #     print ('sdo:identifier: ',subj, pred, obj)

    subj = str(s)
    obj = str(o)
    pred = str(p)
    wikidata_to_v3.add((s, p, URIRef(obj)))

wikidata_to_v3.serialize(export_dir + 'wikidata-homosaurus-v3-links-with-prefix.ttl', format = 'ttl') # export_dir
wikidata_to_v3.close()

g_homosaurus_v3 = Graph()
g_homosaurus_v3.parse('v3.ttl')

redirected_mapping = {}

with open('../redirect/redirected_entities_v3.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count_loaded_redirect = 0
    for row in reader:
        redirected_mapping[row['Source']] = row['Redirected']
        count_loaded_redirect += 1
# print ('count_loaded_redirect (v3)= ', count_loaded_redirect)

outdated_replaced = set()
outdated_redirected = set()
not_in_h3 = set()
# next, test how many obj in wikidata_to_v3 are outdated:
for s, p, o in wikidata_to_v3:
    #  if o was replaced in v3:
    # print ('testing ', str(o))
    if (None, URIRef('http://purl.org/dc/terms/replaces'), o) in g_homosaurus_v3:
        outdated_replaced.add(str(o))
    elif (o, URIRef('http://purl.org/dc/terms/isReplacedBy'), None) in g_homosaurus_v3:
        outdated_replaced.add(str(o))
    #if not in h3 at all
    if (None, None, o) not in g_homosaurus_v3:
        if (o, None, None) not in g_homosaurus_v3:
            not_in_h3.add(str(o))

    # if o was redirected:

    if str(o) in redirected_mapping.keys():
        outdated_redirected.add(str(o))
        print (str(s), str(o), '->', redirected_mapping[str(o)])

print ('# oudated replaced = ', len(outdated_replaced))
print ('# oudated redirected = ', len(outdated_redirected))
print ('# overall outdated = ', len(outdated_replaced.union(outdated_redirected)))
print ('\n\n# entities not in v3 at all: ', len(not_in_h3))
print ('overlap of entities replaced: ', len(not_in_h3.intersection(outdated_replaced)))
print ('overlap of entities redirected: ', len(not_in_h3.intersection(outdated_redirected)))
