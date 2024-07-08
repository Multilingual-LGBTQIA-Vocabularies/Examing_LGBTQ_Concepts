# this file finds the missing links between Homosaurus and LCSH
# the missing links are in found_new_links_h3_lcsh.csv


from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx

# load the links between Homosaurus v3 and LCSH


G = Graph()
G.parse('../data/Homosaurus/mapping_homosaurus_lcsh/Homosaurus_links_to_LCSH.nt')
link_v3_lcsh = {}
for (s, p, o) in G:
    subj = str(s)
    obj = str(o)
    if 'https://homosaurus.org/v3/homoit' in subj and 'http://id.loc.gov/authorities/subjects/' in obj:
        link_v3_lcsh[subj]= obj
    if 'https://homosaurus.org/v3/homoit' in obj and 'http://id.loc.gov/authorities/subjects/' in subj:
        link_v3_lcsh[obj]= subj

# for s in link_v3_lcsh:
#     print ('s = ', s, ' -> ', link_v3_lcsh[s])

# load the redirection between Homosaurus v3

redirected = Graph()
redirected.parse('../data/Homosaurus/redirect/homosaurus-redirect.nt')

redirected_pairs = {}

for (s, p, o) in redirected:
    subj = str(s)
    obj = str(o)
    if ((subj,obj)) not in redirected_pairs:
        redirected_pairs[subj] = obj
    else:
        print ('error: already existing: ', subj, obj)
print('# redirected pairs ', len(redirected_pairs))



replaced = Graph()
replaced.parse('../data/Homosaurus/replace_relations_homosaurus/v3_replace_links.nt')

replaced_pairs = {}

for (s, p, o) in replaced:
    subj = str(s)
    obj = str(o)
    if 'https://homosaurus.org/v3/homoit' in subj and 'https://homosaurus.org/v3/homoit' in obj:
        if 'http://purl.org/dc/terms/replaces' in str(p):
            print(subj, 'replaces', obj)
            replaced_pairsp[obj] = subj
        elif 'http://purl.org/dc/terms/isReplacedBy' in str(p) :
            replaced_pairs[subj]= obj
            print(subj, 'isReplacedBy', obj)


# load entities in Homosaurus V3 that are no longer maintained (not found in the latest version)
no_longer_maintained = set()
with open('../analysis_integrated_graph/entities_in_integrated_but_not_in_v3.csv', newline='') as csvfile:
    for l in csvfile.readlines():
        e = l.strip()
        no_longer_maintained.add(e)

print('loaded #entities no longer maintained in v3: ', len(no_longer_maintained))

#
# # load all the entities in V3
# collect_entities_v3 = set()
# count_v3 = 0
# for (s, p, o) in v3:
#     count_v3 += 1
#     subj = str(s)
#     obj = str(o)
#     if 'https://homosaurus.org/v3/homoit' in subj:
#         collect_entities_v3.add(subj)
#     if 'https://homosaurus.org/v3/homoit' in obj:
#         collect_entities_v3.add(obj)
#
#

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

    count_v3 = 0
    count_lcsh = 0
    e_v3 = None
    e_lsch = None
    collect_redirected = set()
    collect_replaced = set()

    for e in entities:
        if 'https://homosaurus.org/v3/homoit' in e:
            if e in redirected_pairs.keys(): # no_longer_maintained:
                collect_redirected.add(redirected_pairs[e])
            elif e in replaced_pairs.keys():
                collect_replaced.add(replaced_pairs[e])
            else:
                count_v3 += 1
                e_v3 = e

        if 'http://id.loc.gov/authorities/subjects/' in e:
            count_lcsh += 1
            e_lsch = e

    if count_lcsh == 1:
        if count_v3 == 1 and len(collect_redirected.union(collect_replaced)) == 0:
            found.add((e_v3, e_lsch))
        elif e_v3 != None:
            if len(collect_redirected.union(collect_replaced)) == 1:
                if e_v3 == list(collect_redirected.union(collect_replaced))[0]:
                    found.add((e_v3, e_lsch))
        elif len(collect_redirected.union(collect_replaced)) == 1:
            e_v3 = list(collect_redirected.union(collect_replaced))[0]
            found.add((e_v3, e_lsch))

print ('total entities found ', len(found))
print ('total exisitng links', len(link_v3_lcsh))

# print ('not covered by existing links ', len(found.difference(link_v3_lcsh)))

# for (e, f) in list(found.difference(link_v3_lcsh))[:10]:
#     if e in link_v3_lcsh.keys():
#         print ('found', e, f)
#         print ('already linked', e, link_v3_lcsh[e])
#         print (f == link_v3_lcsh[e])

found_filtered = set()

for (e, f) in found:
    if e in link_v3_lcsh.keys():
        g = link_v3_lcsh[e]
        if f == g:
            # found_filtered.add((e,f))
            pass
            # already existing
        else:
            print (e, 'but differnt', f, g)
    else:
        found_filtered.add((e,f))

print('# links after filtering: ', len(found_filtered))

for (e, f) in list(found_filtered)[:10]:
    print (e, f)

# export these links
mapping_file = open('found_new_links_h3_lcsh.csv', 'w')
mapping_csvwriter = csv.writer(mapping_file)
mapping_csvwriter.writerow(['Entity_H3', 'Entity_LCSH'])

for (e, f) in list(found_filtered):
    mapping_csvwriter.writerow([e, f])

mapping_file.close()
