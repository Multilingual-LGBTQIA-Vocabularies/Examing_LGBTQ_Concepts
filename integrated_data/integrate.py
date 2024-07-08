# This file integrates all the links extracted
# We export the links with entities in our scope in the file
# wikidata-lcsh-links-selected.nt. The other links between LCSH
# and Wikidata were discarded.
# a mapping from entities to their corresponding WCCs is in file
# mapping.csv. The second column is the ID of the WCC, the third column
# is about the size of the WCC (number of entities in the WCC).

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt

integrated = Graph()

files = [
'../data/GSSO/gsso_lcsh_corrected.nt',
'../data/GSSO/gsso_wikidata_corrected.nt',
'../data/GSSO/mapping_to_v1.nt',
'../data/GSSO/mapping_to_v2.nt',
'../data/GSSO/mapping_to_v3.nt',
'../data/Homosaurus/mapping_homosaurus_lcsh/Homosaurus_links_to_LCSH.nt',
'../data/Homosaurus/redirect/homosaurus-redirect.nt',
'../data/Homosaurus/replace_relations_homosaurus/v2_replace_links.nt',
'../data/Homosaurus/replace_relations_homosaurus/v3_replace_links.nt',
'../data/QLIT/mapping/qlit_mapping_to_v2.nt',
'../data/QLIT/mapping/qlit_mapping_to_v3.nt',
'../data/QLIT/mapping/qlit-lcsh.nt',
'../data/wikidata/wikidata-homosaurus-v2-links-with-prefix.ttl',
'../data/wikidata/wikidata-homosaurus-v3-links-with-prefix.ttl',
'../data/wikidata/wikidata-qlit-with-prefix.nt',
'../data/wikidata/wikidata-gsso-links-with-prefix.nt'
]

wikidata_lcsh_file = '../data/wikidata/wikidata-lcsh-links-all.nt'
h = Graph ()
h.parse(wikidata_lcsh_file)


for file in files :
    g = Graph()
    g.parse(file)
    integrated = integrated + g

nxG = nx.DiGraph()

for (s,p,o) in integrated:
    nxG.add_edge(str(s), str(o), predicate = str(p))

print('# nodes = ', nxG.number_of_nodes())
print('# edges = ', nxG.number_of_nodes())

count_chosen_wikidata_links = 0
selectd_wikidata_links = Graph()
for (s,p,o) in h:
    # debug:
    # if 'http://www.wikidata.org/entity/Q592' == str(s):
    #     print (str(s), p, o)
    #     print (str(s) in nxG.nodes())
    if str(s) in nxG.nodes() and ('http://id.loc.gov/authorities/subjects/'+str(o)) in nxG.nodes():
        q = URIRef('http://id.loc.gov/authorities/subjects/' + str(o))
        integrated.add((s,p, q))
        selectd_wikidata_links.add((s,p, q))
        count_chosen_wikidata_links+=1
        nxG.add_edge(str(s), 'http://id.loc.gov/authorities/subjects/' + str(o), predicate = str(p))

print('after adding ', count_chosen_wikidata_links, ' links')
selectd_wikidata_links.serialize('wikidata-lcsh-links-selected.nt', format = 'nt') # export_dir
selectd_wikidata_links.close()

integrated.serialize('integrated.nt', format = 'nt') # export_dir
integrated.close()


print('Final # nodes = ', nxG.number_of_nodes())
print('Final # edges = ', nxG.number_of_edges())

# nxG_undirected = nx.Graph(nxG)
ccs = nx.weakly_connected_components(nxG)
size_list = [len(c) for c in sorted(ccs, key=len, reverse=True)]

# print ('size list', size_list)
# size list [45, 36, 36, 35, 33, 32, 30, 30, 29, 28, 26, 26, 24, 24, 23, 22, 22, 22, 21, 21, 20, 20, 19, 19, 18, 18, 18, 17, 17, 17, 17, 17, 17, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,

# [(2, 3505), (3, 1611), (4, 597), (5, 227), (6, 155), (7, 136), (8, 67), (9, 35), (11, 20), (12, 14), (15, 13), (13, 13), (10, 12), (14, 9), (17, 6), (22, 3), (18, 3), (16, 3), (36, 2), (30, 2), (26, 2), (24, 2), (21, 2), (20, 2), (19, 2), (45, 1), (35, 1), (33, 1), (32, 1), (29, 1), (28, 1), (23, 1)]


ct = Counter()
for s in size_list:
    ct[s] +=1

print ('counted: ', ct.most_common())


f = plt.figure()

plt.hist(size_list, bins=max(size_list))
plt.gca().set( ylabel='Frequency', xlabel='Size of cluster');
plt.yscale('log')


f.set_figwidth(7)
f.set_figheight(4)

# plt.show()

plt.savefig('frequency.png')

# print singletons
export_dir = './weakly_connected_components/'
id = 0
ccs = nx.weakly_connected_components(nxG)
mapping_entity_id = {}


# export mapping_entity_id
mapping_file = open('mapping.csv', 'w')
mapping_csvwriter = csv.writer(mapping_file)
mapping_csvwriter.writerow(['Entity', 'WCC_ID', 'WCC_Size'])

lcsh_entities_file = open('lcsh_entities_in_integrated_file.csv', 'w')
lcsh_entities_file_csvwriter = csv.writer(lcsh_entities_file)

exported_lcsh_entities =  set()

for k in [c for c in sorted(ccs, key=len, reverse=True)]:

    entities = list(k)
    size_WCC = len(entities)
    for e in entities:
        mapping_entity_id[e] = id
        mapping_csvwriter.writerow([e, mapping_entity_id[e], size_WCC])
        if 'http://id.loc.gov/authorities/subjects/' in e and e not in exported_lcsh_entities:
            lcsh_entities_file_csvwriter.writerow([e])
            exported_lcsh_entities.add(e)
    num_entities = len(entities)
    H = nxG.subgraph(entities)
    edges = list(H.edges)
    num_edges = len(edges)

    # export entities
    entity_file = open(export_dir + str(id) + '_entities.csv', 'w')
    entity_csvwriter = csv.writer(entity_file)
    for e in entities:
        entity_csvwriter.writerow([e])
    entity_file.close()

    # export edges
    edges_file = open(export_dir + str(id) + '_edges.csv', 'w')
    edges_csvwriter = csv.writer(edges_file)
    edges_csvwriter.writerow(['Source', 'Target'])
    for (s, t) in edges:
        edges_csvwriter.writerow([s, nxG.edges[s, t]['predicate'], t])
    edges_file.close()

    id +=1

print(len(exported_lcsh_entities), ' LCSH entities exported for check')
lcsh_entities_file.close()
mapping_file.close()
