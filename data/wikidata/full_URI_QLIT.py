# add https://queerlit.dh.gu.se/qlit/v1/ to objects


from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx


# raw_wikidata_to_qlit = Graph()
# raw_wikidata_to_qlit.parse ("./wikidata-qlit-links.ttl")
#
# qlit_prefix = 'https://queerlit.dh.gu.se/qlit/v1/'
#
# g = Graph()
#
# for (s, p, o) in raw_wikidata_to_qlit:
#     r = URIRef (qlit_prefix + str(o))
#
#     g.add ((s, p, r))
#
# g.serialize('wikidata-qlit-with-prefix.nt', format = 'nt') # export_dir
# g.close()
#

raw_wikidata_to_gsso = Graph()
raw_wikidata_to_gsso.parse ("./wikidata-gsso-links.nt")

gsso_prefix = 'http://purl.obolibrary.org/obo/GSSO_'

g = Graph()

for (s, p, o) in raw_wikidata_to_gsso:
    if ' ' not in str(o):
        r = URIRef (gsso_prefix + str(o))
        g.add ((s, p, r))

g.serialize('wikidata-gsso-links-with-prefix.nt', format = 'nt') # export_dir
g.close()


#
# gv2 = Graph()
# gv2.parse ("./wikidata-homosaurus-v2-links-with-prefix.ttl")
#
# gv2.serialize('wikidata-homosaurus-v2-links-with-prefix.nt', format = 'nt') # export_dir
# gv2.close()
#
#
# gv3 = Graph()
# gv3.parse ("./wikidata-homosaurus-v3-links-with-prefix.ttl")
#
# gv3.serialize('wikidata-homosaurus-v3-links-with-prefix.nt', format = 'nt') # export_dir
# gv3.close()
