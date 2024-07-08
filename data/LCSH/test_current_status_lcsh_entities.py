
from rdflib import Graph
from collections import Counter
from rdflib import URIRef, Literal
import csv
import networkx as nx
import matplotlib.pyplot as plt
from hdt import HDTDocument

lcsh_file = 'lcsh.hdt'
# lcsh_file = 'subjects.skosrdf.nt'
hdt_lcsh = HDTDocument(lcsh_file)


def test_in_latest_version (e):
    # print ('testing: ', e)
    triples, cardinality = hdt_lcsh.search_triples(e, "", "")
    for s, _, _ in triples:
        if e == s:
            return True

    triples, cardinality = hdt_lcsh.search_triples("", "", e)
    for _, _, o in triples:
        if e == o:
            return True

    # f = e.replace ('http://', 'https://')
    #
    # triples, cardinality = hdt_lcsh.search_triples(f, "", "")
    # for s, _, _ in triples:
    #     if e == s:
    #         return True
    #
    # triples, cardinality = hdt_lcsh.search_triples("", "", f)
    # for _, _, o in triples:
    #     if e == o:
    #         return True

    return False

count = 0
count_outdated = 0


# load file lcsh_entities_in_integrated_file.csv

lcsh_outdated_entities_file = open('lcsh_entities_outdated.csv', 'w')
lcsh_outdated_entities_writer = csv.writer(lcsh_outdated_entities_file)

processed = set()

for line in open("lcsh_entities_in_integrated_file.csv"):
# for (s, p, o) in triples:

    e = line.strip()
    print (e)
    if e not in processed:
        processed.add(e)

    #
    # if count %10 ==0:
    #     print (count, ' has been processed.', flush = True)

    if 'http://id.loc.gov/authorities/subjects/' in e:

        # print ('processing ', e)
        count += 1
        if not test_in_latest_version(e):
            print (e, ' is not in the latest version' )
            count_outdated += 1
            lcsh_outdated_entities_writer.writerow([e])


print ('count total: ', count)
print ('total processed: ', len(processed))
print ('count outdated (not in the latest version): ', count_outdated)
# count total:  2085
# count outdated (not in the latest version):  0
lcsh_outdated_entities_file.close()
