# this file tests the longest path of replacement in Homosaurus v3
# The two relations under examination are:
# http://purl.org/dc/terms/isReplacedBy
# http://purl.org/dc/terms/replaces


# The longest path =  ['http://purl.obolibrary.org/obo/GSSO_008172', 'http://homosaurus.org/v2/homomonuments', 'https://homosaurus.org/v3/homoit0000642', 'https://homosaurus.org/v3/homoit0000901']
# count_loaded_redirect =  63
# http://purl.obolibrary.org/obo/GSSO_002025
# #gsso entities involved in this replacement:  1104
# 	Among them, how many reached v3: 1068
# 	How many of them has exactly one match with v3:  966
# 	How many of them diverged (one gsso entity mapped to multiple Homosaurus v3 entities)? :  102
# total nodes in v3: 1206

from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx

G = nx.DiGraph()

g_gsso_to_v2 = Graph()
g_gsso_to_v2.parse ("./mappings_gsso-homosaurus/mapping_to_v2.nt")

g_gsso_to_v3 = Graph()
g_gsso_to_v3.parse ("./mappings_gsso-homosaurus/mapping_to_v3.nt")



g_homosaurus_v2_replaces = Graph()
g_homosaurus_v2_replaces.parse ("./replace_relations_homosaurus/v2_replace_links.nt")


g_homosaurus_v3_replaces = Graph()
g_homosaurus_v3_replaces.parse ("./replace_relations_homosaurus/v3_replace_links.nt")

gsso_entities = set()


for subj_gsso, _, obj_h_v2 in g_gsso_to_v2.triples ((None, None, None)):
    if ('homosaurus.org/v2/' in str(obj_h_v2)):
        G.add_edge(str(subj_gsso), str(obj_h_v2))
        gsso_entities.add(str(subj_gsso))


for subj_gsso, _, obj_h_v3 in g_gsso_to_v3.triples ((None, None, None)):
    if ('homosaurus.org/v3/' in str(obj_h_v3)):
        G.add_edge(str(subj_gsso), str(obj_h_v3))
        gsso_entities.add(str(subj_gsso))


for s, p, o in g_homosaurus_v2_replaces.triples((None, URIRef('http://purl.org/dc/terms/replaces'), None)):
    G.add_edge(str(o), str(s)) # the direction represents "isreplacedBy"


for s, p, o in g_homosaurus_v2_replaces.triples((None, URIRef('http://purl.org/dc/terms/isReplacedBy'), None)):
    G.add_edge(str(s), str(o)) # the direction represents "isreplacedBy"


for s, p, o in g_homosaurus_v3_replaces.triples((None, URIRef('http://purl.org/dc/terms/replaces'), None)):
    G.add_edge(str(o), str(s)) # the direction represents "isreplacedBy"


for s, p, o in g_homosaurus_v3_replaces.triples((None, URIRef('http://purl.org/dc/terms/isReplacedBy'), None)):
    G.add_edge(str(s), str(o)) # the direction represents "isreplacedBy"


print('The longest path = ', nx.dag_longest_path(G))

# The longest path =  ['http://homosaurus.org/v2/homomonuments', 'https://homosaurus.org/v3/homoit0000642', 'https://homosaurus.org/v3/homoit0000901']

# G.remove_edge ('https://homosaurus.org/v3/homoit0000642', 'https://homosaurus.org/v3/homoit0000901')

# print('After removall of that one, the longest path = ', nx.dag_longest_path(G))
count_v3 = 0
v3_exactly_one=0
gsso_to_v3_diverged = 0
collect_all_nodes_reached_v3 = set()

# load redirected_mapping from the directory ./redirect. The two files are redirected_entities_v3.csv
# column names: Source,Redirected

redirected_mapping = {}

with open('redirect/redirected_entities_v3.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count_loaded_redirect = 0
    for row in reader:
        redirected_mapping[row['Source']] = row['Redirected']
        count_loaded_redirect += 1
print ('count_loaded_redirect = ', count_loaded_redirect)

count_redirected = 0

collect_all = []
for x in gsso_entities:
    flag = False
    if x == 'http://purl.obolibrary.org/obo/GSSO_006601':
        print(x)
        flag = True
    # print (x)
    if flag  and len(list(G.neighbors(x))) != 1:
        print (x, ' has ', len(list(G.neighbors(x))), ' neighbors')
        print ('\t:', list(G.neighbors(x)))
    nodes_in_path_v2 = set()
    nodes_in_path_v3 = set()
    latest_nodes_v3 = set()
    redirected_latest_nodes_v3 = set()
    for y in list(G.neighbors(x)):
        if flag:
            print ('y: ',y)
        if 'homosaurus.org/v2/' in y:
            nodes_in_path_v2.add(y)
        elif  'homosaurus.org/v3/' in y:
            nodes_in_path_v3.add(y)
            latest_nodes_v3.add(y)
        for z in list(G.neighbors(y)):
            if flag:
                print('z: ',z)
            if 'homosaurus.org/v2/' in z:
                nodes_in_path_v2.add(z)
            elif 'homosaurus.org/v3/' in z:
                nodes_in_path_v3.add(z)
                if y in latest_nodes_v3:
                    latest_nodes_v3.remove(y)
                latest_nodes_v3.add(z)
                if flag == True:
                    print ('--nodes_in_path_v3: ', nodes_in_path_v3)
                    print ('--latest_nodes_v3: ', latest_nodes_v3)
            for w in list(G.neighbors(z)):

                if 'homosaurus.org/v2/' in w:
                    nodes_in_path_v2.add(w)
                elif  'homosaurus.org/v3/' in w:
                    nodes_in_path_v3.add(w)
                    if z in latest_nodes_v3:
                        latest_nodes_v3.remove(z)

                    latest_nodes_v3.add(w)
                if flag == True:
                    print ('w: ', w)
                    print ('===nodes_in_path_v3: ', nodes_in_path_v3)
                    print ('===latest_nodes_v3: ', latest_nodes_v3)

    for l in latest_nodes_v3:
        if l in redirected_mapping:
            print ('redirect happens here: ',l ,' -> ', redirected_mapping[l])
            redirected_latest_nodes_v3.add(redirected_mapping[l])
            nodes_in_path_v3.add(redirected_mapping[l])
            count_redirected += 1
            if flag == True:
                print ('<<<nodes_in_path_v3: ', nodes_in_path_v3)
                print ('<<<latest_nodes_v3: ', latest_nodes_v3)
                print ('<<<after redirection: ', redirected_latest_nodes_v3)

        else:
            redirected_latest_nodes_v3.add(l)

    if flag == True:
        print ('Final: nodes_in_path_v3: ', nodes_in_path_v3)
        print ('Final: latest_nodes_v3: ', latest_nodes_v3)

    collect_all_nodes_reached_v3 = collect_all_nodes_reached_v3.union (nodes_in_path_v3)

    if len(nodes_in_path_v3) != 0:
        count_v3 += 1
    if len(latest_nodes_v3) == 1:
        v3_exactly_one += 1
    elif len (latest_nodes_v3) > 1:
        gsso_to_v3_diverged +=1
        # print ('diverged', x, nodes_in_path_v3)
    collect_all.append((x, nodes_in_path_v2, nodes_in_path_v3, latest_nodes_v3, redirected_latest_nodes_v3))

summary_file =  open ('replace_summary.csv', mode='w', newline='')
summary_writer = csv.writer(summary_file)
summary_writer.writerow(['GSSO Entity', 'All Entities in Homosaurus V2', 'All Entities in Homosaurus V3', 'Latest Entities in Homosaurus V3', 'Latest (Redirected) Entities in Homosaurus V3'])
for (x, entities_v2, entities_v3, latest, redi_latest) in collect_all:
    summary_writer.writerow([x, list(entities_v2), list(entities_v3), list(latest), list(redi_latest)])


print('#gsso entities involved in this replacement: ', len(gsso_entities))
print('\tAmong them, how many reached v3:', count_v3)
print ('\tHow many of them has exactly one match with v3: ', v3_exactly_one)
print ('\tHow many of them diverged (one gsso entity mapped to multiple Homosaurus v3 entities)? : ', gsso_to_v3_diverged)
print('total nodes in v3:', len(collect_all_nodes_reached_v3)) # 1206
print ('[NEW]redirected ', count_redirected) # 28

# The longest path =  ['http://purl.obolibrary.org/obo/GSSO_008172', 'http://homosaurus.org/v2/homomonuments', 'https://homosaurus.org/v3/homoit0000642', 'https://homosaurus.org/v3/homoit0000901']
# http://purl.obolibrary.org/obo/GSSO_008172 and v2:  {'http://homosaurus.org/v2/homomonuments'}  and v3:  {'https://homosaurus.org/v3/homoit0000642', 'https://homosaurus.org/v3/homoit0000901'}
# http://purl.obolibrary.org/obo/GSSO_008170 and v2:  {'http://homosaurus.org/v2/LGBTQMemorials'}  and v3:  {'https://homosaurus.org/v3/homoit0000901'}


# below are the redirects that happened after identifier and replace relations:
# redirect happens here:  https://homosaurus.org/v3/homoit0000586  ->  https://homosaurus.org/v3/homoit0000442
# redirect happens here:  https://homosaurus.org/v3/homoit0001524  ->  https://homosaurus.org/v3/homoit0001523
# redirect happens here:  https://homosaurus.org/v3/homoit0000291  ->  https://homosaurus.org/v3/homoit0000380
# redirect happens here:  https://homosaurus.org/v3/homoit0000388  ->  https://homosaurus.org/v3/homoit0000380
# redirect happens here:  https://homosaurus.org/v3/homoit0000251  ->  https://homosaurus.org/v3/homoit0002226
# redirect happens here:  https://homosaurus.org/v3/homoit0000378  ->  https://homosaurus.org/v3/homoit0002226
# redirect happens here:  https://homosaurus.org/v3/homoit0001490  ->  https://homosaurus.org/v3/homoit0001851
# redirect happens here:  https://homosaurus.org/v3/homoit0000320  ->  https://homosaurus.org/v3/homoit0000380
# redirect happens here:  https://homosaurus.org/v3/homoit0000495  ->  https://homosaurus.org/v3/homoit0000949
# redirect happens here:  https://homosaurus.org/v3/homoit0000290  ->  https://homosaurus.org/v3/homoit0001235
# redirect happens here:  https://homosaurus.org/v3/homoit0000397  ->  https://homosaurus.org/v3/homoit0000442
# redirect happens here:  https://homosaurus.org/v3/homoit0000615  ->  https://homosaurus.org/v3/homoit0000442
# redirect happens here:  https://homosaurus.org/v3/homoit0001530  ->  https://homosaurus.org/v3/homoit0001540
# redirect happens here:  https://homosaurus.org/v3/homoit0000679  ->  https://homosaurus.org/v3/homoit0001658
# redirect happens here:  https://homosaurus.org/v3/homoit0000468  ->  https://homosaurus.org/v3/homoit0000544
# redirect happens here:  https://homosaurus.org/v3/homoit0001528  ->  https://homosaurus.org/v3/homoit0001540
# redirect happens here:  https://homosaurus.org/v3/homoit0001355  ->  https://homosaurus.org/v3/homoit0000861
# redirect happens here:  https://homosaurus.org/v3/homoit0000907  ->  https://homosaurus.org/v3/homoit0001030
# redirect happens here:  https://homosaurus.org/v3/homoit0000102  ->  https://homosaurus.org/v3/homoit0000442
# redirect happens here:  https://homosaurus.org/v3/homoit0000468  ->  https://homosaurus.org/v3/homoit0000544
# redirect happens here:  https://homosaurus.org/v3/homoit0001455  ->  https://homosaurus.org/v3/homoit0001218
# redirect happens here:  https://homosaurus.org/v3/homoit0000195  ->  https://homosaurus.org/v3/homoit0001218
# redirect happens here:  https://homosaurus.org/v3/homoit0001364  ->  https://homosaurus.org/v3/homoit0001218
# redirect happens here:  https://homosaurus.org/v3/homoit0000548  ->  https://homosaurus.org/v3/homoit0001218
# redirect happens here:  https://homosaurus.org/v3/homoit0000790  ->  https://homosaurus.org/v3/homoit0001218
# redirect happens here:  https://homosaurus.org/v3/homoit0001647  ->  https://homosaurus.org/v3/homoit0001658
# redirect happens here:  https://homosaurus.org/v3/homoit0000107  ->  https://homosaurus.org/v3/homoit0000894
# redirect happens here:  https://homosaurus.org/v3/homoit0001003  ->  https://homosaurus.org/v3/homoit0000530
