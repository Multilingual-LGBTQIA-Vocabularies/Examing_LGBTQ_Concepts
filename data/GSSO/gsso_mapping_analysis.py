# this file exports identity links between GSSO and
# different versions of Homosaurus
# that of both sdo:identifier and dc:identifier were extracted

from rdflib import Graph, URIRef
from collections import Counter
# Create an RDFLib Graph object

def get_name (e):
	name = ''
	prefix = ''
	sign = ''
	if e.rfind('/') == -1 : # the char '/' is not in the iri
		if e.split('#') != [e]: # but the char '#' is in the iri
			name = e.split('#')[-1]
			prefix = '#'.join(e.split('#')[:-1]) + '#'
			sign = '#'
		else:
			name = None
			sign = None
			prefix =  None
	else:
		name = e.split('/')[-1]
		prefix = '/'.join(e.split('/')[:-1]) + '/'
		sign = '/'

	return prefix, sign, name


g = Graph()
export_v1 = Graph()
export_v2 = Graph()
export_v3 = Graph()

# Parse the OWL file into the Graph
g.parse("gsso.owl")

map_sub_subject = {}
map_sub_pred = {}
map_sub_object = {}

triples_v1 = set()
triples_v2 = set()
triples_v3 = set()

prefix_h1 = 'https://homosaurus.org/terms/'
prefix_h2 = 'http://homosaurus.org/v2/'
prefix_h2_https = 'https://homosaurus.org/v2'
prefix_h3 = 'https://homosaurus.org/v3/'
# Iterate over each triple in the graph

for subj, pred, obj in g:
    # if 'https://schema.org/identifier' in pred:
    #     print ('sdo:identifier: ',subj, pred, obj)

    subj = str(subj)
    obj = str(obj)
    pred = str(pred)

    if 'homosaurus.org' in obj:
        if 'http://purl.org/dc/elements/1.1/identifier' in pred:
            if prefix_h1 in obj:
                triples_v1.add((subj, 'http://purl.org/dc/elements/1.1/identifier', obj))
            elif prefix_h2 in obj or prefix_h2_https in obj:
                triples_v2.add((subj, 'http://purl.org/dc/elements/1.1/identifier', obj))
            elif prefix_h3 in obj:
                triples_v3.add((subj, 'http://purl.org/dc/elements/1.1/identifier', obj))
            else:
                print ('error: ', subj, pred, obj)

        elif 'https://schema.org/identifier' in pred:

            if prefix_h1 in obj:
                triples_v1.add((subj, 'https://schema.org/identifier', obj))
            elif prefix_h2 in obj or prefix_h2_https in obj:
                triples_v2.add((subj, 'https://schema.org/identifier', obj))
            elif prefix_h3 in obj:
                triples_v3.add((subj, 'https://schema.org/identifier', obj))
            else:
                print ('error: ', subj, pred, obj)

        elif 'http://purl.org/dc/terms/source' in pred:
            pass

    # prepare that dictionary:
    if 'http://www.w3.org/2002/07/owl#annotatedSource' in pred:
        map_sub_subject[subj] = obj
        # print('record subject as', subj, pred, obj)

    elif 'http://www.w3.org/2002/07/owl#annotatedProperty' in pred:
        map_sub_pred[subj] = obj
        # print('record predicate as', subj, pred, obj)

    elif 'http://www.w3.org/2002/07/owl#annotatedTarget' in pred:
        map_sub_object[subj] = obj


# print ('number of triples for v1 = ', len(triples_v1))
# print ('number of triples for v2 = ', len(triples_v2))
# print ('number of triples for v3 = ', len(triples_v3))

for subj, pred, obj in g:

    subj = str(subj)
    obj = str(obj)
    pred = str(pred)

    if 'http://www.w3.org/2002/07/owl#annotatedTarget' in pred and 'homosaurus.org' in obj:
        if subj in map_sub_subject.keys():
            subject = map_sub_subject[subj]
            if subj in map_sub_pred.keys():
                predicate = map_sub_pred[subj]

                subject =  str(subject)
                predicate =  str(predicate)
                object =  str(obj)

                if prefix_h1 in obj:
                    triples_v1.add((subject, predicate, object))
                elif prefix_h2 in obj or prefix_h2_https in obj:
                    triples_v2.add((subject, predicate, object))
                elif prefix_h3 in obj:
                    triples_v3.add((subject, predicate, object))
                else:
                    print ('not these versions: ', subj, pred, obj)
            else:
                print ('predicate not in map: ', subj)
        else:
            print ('not found subj in map: ', subj, pred, obj)

print ('number of triples for v1 = ', len(triples_v1))
print ('number of triples for v2 = ', len(triples_v2))
print ('number of triples for v3 = ', len(triples_v3))
#
# print ('size  = ', len(map_sub_subject))
# print ('size  = ', len(map_sub_pred))
# print ('size  = ', len(map_sub_object))


all_subjects = set()

for subj, pred, obj in g:
    if 'differentFrom' in pred:
        print ('differentFrom',subj, pred, obj)

counter_p_v1 = Counter()
for (s,p,o) in triples_v1:
    all_subjects.add(s)
    counter_p_v1[p] += 1
    if p =='http://www.geneontology.org/formats/oboInOwl#hasDbXref':
        print ('Found a very special mapping: ',s, p, o)
    else:
        export_v1.add((URIRef(s), URIRef(p), URIRef(o)))

counter_p_v2 = Counter()
for (s,p,o) in triples_v2:
    all_subjects.add(s)
    counter_p_v2[p] += 1
    export_v2.add((URIRef(s), URIRef(p), URIRef(o)))

counter_p_v3 = Counter()
for (s,p,o) in triples_v3:
    all_subjects.add(s)
    counter_p_v3[p] += 1
    if p =='http://purl.obolibrary.org/obo/IAO_0000115':
        print ('Found a very special mapping: ', s, p, o)
    else:
        export_v3.add((URIRef(s), URIRef(p), URIRef(o)))


print ('\nv1\n',counter_p_v1)
print ('\nv2\n',counter_p_v2)
print ('\nv3\n',counter_p_v3)

dir = './mappings_gsso-homosaurus/'
# export_v1
f = open('mapping_to_v1.nt', 'w')
export_v1.serialize(dir +'mapping_to_v1.nt', format="nt")
f.close()

# export_v2
f = open('mapping_to_v2.nt', 'w')
export_v2.serialize(dir + 'mapping_to_v2.nt', format="nt")
f.close()

# export_v3
f = open('mapping_to_v3.nt', 'w')
export_v3.serialize(dir + 'mapping_to_v3.nt', format="nt")
f.close()

print('there are ', len(all_subjects), ' unique subjects in the triples')

count_gsso = 0
ct_namespace = Counter ()
for s in all_subjects:
    if 'http://purl.obolibrary.org/obo/GSSO' not in s:
        n,_,_, = get_name(s)
        ct_namespace[n] += 1
        # print(s)
    else:
        count_gsso +=1

print ('There are in total ', count_gsso, ' GSSO entities in the mapping')
print(ct_namespace)
