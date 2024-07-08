# this file finds the missing links between Homosaurus and LCSH
# The missing links are exported to the file found_new_links_qlit_lcsh.csv

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx

# load the links between Homosaurus v3 and LCSH


G = Graph()
G.parse('../data/QLIT/mapping/qlit-lcsh.nt')
link_qlit_lcsh = {}
for (s, p, o) in G:
    subj = str(s)
    obj = str(o)
    if 'https://queerlit.dh.gu.se/qlit/v1/' in subj and 'http://id.loc.gov/authorities/subjects/' in obj:
        link_qlit_lcsh[subj]= obj
    if 'https://queerlit.dh.gu.se/qlit/v1/' in obj and 'http://id.loc.gov/authorities/subjects/' in subj:
        link_qlit_lcsh[obj]= subj


# For each WCC 0 - 6405
path = '../integrated_data/weakly_connected_components/'

found = set()
for i in range(6406):
    # load the entities
    entities = set()
    with open(path + str(i) + '_entities.csv', newline='') as csvfile:
        for l in csvfile.readlines():
            e = l.strip()
            entities.add(e)

    count_qlit = 0
    count_lcsh = 0
    e_qlit = None
    e_lsch = None
    collect_redirected = set()
    collect_replaced = set()

    for e in entities:
        if 'https://queerlit.dh.gu.se/qlit/v1/' in e:
            count_qlit += 1
            e_qlit = e

        if 'http://id.loc.gov/authorities/subjects/' in e:
            count_lcsh += 1
            e_lsch = e
        if count_qlit == 1 and count_lcsh == 1:
            found.add((e_qlit, e_lsch))

print ('total entities found ', len(found))
print ('total exisitng links', len(link_qlit_lcsh))

found_filtered = set()
count_found_conflict = 0
for (e, f) in found:
    if e in link_qlit_lcsh.keys():
        g = link_qlit_lcsh[e]
        if f == g:
            # found_filtered.add((e,f))
            pass
            # already existing
        else:
            print (e, 'but differnt', f, ' and ', g)
            count_found_conflict += 1
    else:
        found_filtered.add((e,f))

print ('# links with conflict: ', count_found_conflict)
print ('# links after filtering: ', len(found_filtered))

for (e, f) in list(found_filtered)[:10]:
    print (e, f)

# export these links
mapping_file = open('found_new_links_qlit_lcsh.csv', 'w')
mapping_csvwriter = csv.writer(mapping_file)
mapping_csvwriter.writerow(['Entity_QLIT', 'Entity_LCSH'])

for (e, f) in list(found_filtered):
    mapping_csvwriter.writerow([e, f])

mapping_file.close()
