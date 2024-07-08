# this is a simple script to collect all the entities in the selected links. 

from rdflib import Graph, URIRef
from collections import Counter
import csv

gsso_lcsh = Graph()
gsso_lcsh.parse("gsso_lcsh_corrected.nt")

gsso_wiki = Graph()
gsso_wiki.parse("gsso_wikidata_corrected.nt")

gsso_v1 = Graph()
gsso_wiki.parse("mapping_to_v1.nt")

gsso_v2 = Graph()
gsso_wiki.parse("mapping_to_v2.nt")

gsso_v3 = Graph()
gsso_wiki.parse("mapping_to_v3.nt")

collect_gsso_entities = set()

for (s, p, o) in gsso_lcsh:
    collect_gsso_entities.add(str(s))


print ('in total, there are ', len (collect_gsso_entities), ' entities')
gsso_entity_list =  open ('GSSO_entities.csv', mode='w', newline='')
gsso_entity_list_writer = csv.writer(gsso_entity_list)
for e in collect_gsso_entities:
    gsso_entity_list_writer.writerow([e])
