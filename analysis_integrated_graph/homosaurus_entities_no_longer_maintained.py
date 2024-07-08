
# This file lists the entiteis that are no longer maintained in Homosaurus v3
# We find those entities that were mentioned in other conceptual models but not in
# the latest version of Homosaurus v3

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx


# load Homosaurus v3

v3 = Graph()
v3.parse('../data/Homosaurus/v3.ttl')


# in the integrated file, find all the entities

collect_entities_v3 = set()
count_v3 = 0
for (s, p, o) in v3:
    count_v3 += 1
    subj = str(s)
    obj = str(o)
    if 'https://homosaurus.org/v3/homoit' in subj:
        collect_entities_v3.add(subj)
    if 'https://homosaurus.org/v3/homoit' in obj:
        collect_entities_v3.add(obj)

print ('after processing ', count_v3 , ' triples')
print ('There are ', len (collect_entities_v3), ' in Homosaurus v3')

# load the integrated file
integrated = Graph()
integrated.parse('../integrated_data/integrated.nt')

count_integrated = 0
collect_entities_integrated = set()
for (s, p, o) in integrated:
    count_integrated += 1
    subj = str(s)
    obj = str(o)
    if 'https://homosaurus.org/v3/homoit' in subj:
        collect_entities_integrated.add(subj)
    if 'https://homosaurus.org/v3/homoit' in obj:
        collect_entities_integrated.add(obj)

print ('after processing ', count_integrated, ' triples')
print ('There are ', len (collect_entities_integrated), ' in the integrated file ')


print (len(collect_entities_v3.intersection(collect_entities_integrated)), ' entities are in the intersection')
print (len(collect_entities_v3.difference(collect_entities_v3)), ' entities are not in v3')

in_integrated_not_in_v3 = collect_entities_integrated.difference(collect_entities_v3)

entity_file = open('entities_in_integrated_but_not_in_v3.csv', 'w')
entity_csvwriter = csv.writer(entity_file)
for e in in_integrated_not_in_v3:
    entity_csvwriter.writerow([e])
entity_file.close()

# load the replaced file
replaced = Graph()
replaced.parse('../data/Homosaurus/replace_relations_homosaurus/v3_replace_links.nt')

replaced_pairs = set()

for (s, p, o) in replaced:
    subj = str(s)
    obj = str(o)

    if 'https://homosaurus.org/v3/homoit' in subj and 'https://homosaurus.org/v3/homoit' in obj:
        if 'http://purl.org/dc/terms/replaces' in str(p):
            print(subj, 'replaces', obj)
            replaced_pairs.add((obj, subj))
        elif 'http://purl.org/dc/terms/isReplacedBy' in str(p) :
            replaced_pairs.add((subj, obj))
            print(subj, 'isReplacedBy', obj)

print('# replaced pairs ', len(replaced_pairs))

# load the redirect file
redirected = Graph()
redirected.parse('../data/Homosaurus/redirect/homosaurus-redirect.nt')

redirected_pairs = set()

for (s, p, o) in redirected:
    subj = str(s)
    obj = str(o)
    if ((subj,obj)) not in redirected_pairs:
        redirected_pairs.add((subj, obj))
    else:
        print ('already existing: ', subj, obj)
print('# redirected pairs ', len(redirected_pairs))


# how are the replace and redirect overlapping in v3?
print ('\n',len(redirected_pairs.intersection(replaced_pairs)), ' pairs overlapping')

count_from_outside_homosaurus_to_within_v3 = 0
count_others = 0
# test if the redirect is always from integrated to overlapping
for (s, t) in redirected_pairs:
    if s not in collect_entities_v3 and t in collect_entities_v3:
        count_from_outside_homosaurus_to_within_v3 +=1

    else:
        count_others += 1
        print ('other: ', s, t)
        if s in collect_entities_v3:
            print ('s in v3')
        if t not in collect_entities_v3:
            print ('t not in v3')
        if t in collect_entities_v3:
            print ('t in v3')

print ('in total , # redirected pairs ', len(redirected_pairs))
print ('count from outside to v3', count_from_outside_homosaurus_to_within_v3)
print ('both within v3', count_others)
