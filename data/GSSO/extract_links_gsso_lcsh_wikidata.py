# This is a simple script that extracts the links between GSSO and Wikidata.
# The exported file is gsso_wikidata_corrected.nt.
# Note that we corrected the following.
# - https://www.wikidata.org/wiki/Q1823134 should not be used as a relation. We have replaced it with http://www.wikidata.org/prop/direct/P244.
# - Instead of referring to the page, we refer to the entity. We use http://www.wikidata.org/entity/* instead of https://www.wikidata.org/wiki/*


from rdflib import Graph, BNode, URIRef
from collections import Counter
from rdflib import URIRef, Literal
import csv


GSSO = Graph()
GSSO.parse("./gsso.owl")

# extract links from GSSO to LCSH

gsso_lcsh = Graph()
#
relation = 'https://www.wikidata.org/wiki/Q1823134'
replaced_relation = 'http://www.wikidata.org/prop/direct/P244'

count = 0
for (s, p, o) in GSSO.triples((None, URIRef(relation), None)):
    if 'http://id.loc.gov/authorities/subjects/' in str(o):
        if str(o).split('.')[-1] == 'html':
            o = URIRef(''.join(str(o).split('.')[:-1]))
        if isinstance(s, BNode):
            for (_, _, so) in GSSO.triples((s, URIRef('http://www.w3.org/2002/07/owl#annotatedSource'), None)):

                gsso_lcsh.add((so, URIRef(replaced_relation), o))
        else:
            gsso_lcsh.add((s,URIRef(replaced_relation),o))
            count += 1

gsso_lcsh.serialize('./gsso_lcsh_corrected.nt', format = 'nt') # export_dir
gsso_lcsh.close()

print ('# links between GSSO and LCSH =  ', count )

# extract links from GSSO to Wikidata
# oboInOwl:hasDbXref
# http://www.geneontology.org/formats/oboInOwl#hasDbXref

gsso_wiki = Graph()
#
relation = 'http://www.geneontology.org/formats/oboInOwl#hasDbXref'

count = 0
for (s, p, o) in GSSO.triples((None, URIRef(relation), None)):
    if 'www.wikidata.org' in str(s) and 'www.wikidata.org' in str(o):
        pass
    else:
        corrected_o = 'http://www.wikidata.org/entity/'+ str(o).split('/')[-1]
        if 'https://www.wikidata.org/wiki/' in str(o):
            if isinstance(s, BNode):
                # print ('Empty Node', s)
                # for (ss, sp, _) in GSSO.triples((None, None, s)):
                #     print ('FOUND!', ss, sp, s)
                for (_, _, so) in GSSO.triples((s, URIRef('http://www.w3.org/2002/07/owl#annotatedSource'), None)):
                    # print ('FOUND!', so, p, o)
                    gsso_wiki.add((so, p, URIRef(corrected_o)))
            else:
                gsso_wiki.add((s,p,URIRef(corrected_o)))
                count += 1

gsso_wiki.serialize('./gsso_wikidata_corrected.nt', format = 'nt') # export_dir
gsso_wiki.close()

print ('# links between GSSO and Wikidata =  ', count )
