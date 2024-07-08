# This file contains the SPARQL queries we used for the retrivial of
# entities of Homosaurus, QLIT, and GSSO from the SPRAQL endpoint of
# Wikidata.

# The following files about the links from Wikidata and others were exported:
# 'wikidata-homosaurus-v2-links.nt'
# 'wikidata-homosaurus-v3-links.nt'
# 'wikidata-gsso-links.nt'
# 'wikidata-qlit-links.nt'
# 'wikidata-lcsh-links-all.nt'

# Please note that the links from Wikidata to LCSH are huge. There is an extra
# step to restrict it only to the entities within the scope of this paper.

# The Wikidata SPARQL endpoint is
# https://query.wikidata.org/

# Wikidata - GSSO:          http://www.wikidata.org/prop/direct/P9827
# Wikidata - Homosaurus 2:  http://www.wikidata.org/prop/direct/P6417
# Wikidata - Homosaurus 3:  http://www.wikidata.org/prop/direct/P10192
# Wikidata - LCSH:          http://www.wikidata.org/prop/direct/P244



# PART 1: extracting links of Wikidata-Homosaurus

# Additional test: count the number of Homosaurus entities in Wikidata
# PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#
# SELECT (COUNT(*) AS ?count)
# SELECT ?s ?o
# WHERE {
#  ?s wdt:P6417 ?o. # version 2
#  ?s wdt:P10192 ?o. # version 3
# }


from SPARQLWrapper import SPARQLWrapper, JSON
import validators


sparql = SPARQLWrapper(
    "https://query.wikidata.org/sparql"
    # "http://vocabs.ardc.edu.au/repository/api/sparql/"
    # "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020"
)
sparql.setReturnFormat(JSON)

# gets the first 3 geological ages
# from a Geological Timescale database,
# via a SPARQL endpoint

dir = './'

# extra_filename_v2 = 'wikidata-homosaurus-v2-links.nt'
# extra_ttl_file_v2 = open(extra_filename_v2, 'w', newline='')
#
# extra_filename_v3 = 'wikidata-homosaurus-v3-links.nt'
# extra_ttl_file_v3 = open(extra_filename_v3, 'w', newline='')
#
extra_filename_gsso = 'wikidata-gsso-links.nt'
extra_ttl_file_gsso = open(extra_filename_gsso, 'w', newline='')

# extra_filename_qlit = 'wikidata-qlit-links.nt'
# extra_ttl_file_qlit = open(extra_filename_qlit, 'w', newline='')

# extra_filename_lcsh = 'wikidata-lcsh-links-all.nt'
# extra_ttl_file_lcsh = open(extra_filename_lcsh, 'w', newline='')
#

#
# query_v2 = """
#     PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#
#     SELECT ?s ?o ?lang
#     WHERE {
#      ?s wdt:P6417 ?o. # version 2
#      BIND(LANG(?o) AS ?lang)
#     }
#     """
#
# sparql.setQuery(query_v2)
#
# try:
#     ret = sparql.queryAndConvert()
#
#     for r in ret["results"]["bindings"]:
#         s = r['s']['value']
#         o = r['o']['value']
#         lang = r['lang']['value']
#         print(s, o, lang)
#         if lang =='':
#             extra_ttl_file_v2.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P6417> \""+ o + "\" .\n")
#         else:
#             extra_ttl_file_v2.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P6417> \""+ o+ "\"\@" + lang + ' .\n')
#             # extra_ttl_file.write('<'+ s+ "> <http://dbpedia.org/ontology/wikiPageDisambiguates> <"+ o+ '> .\n')
#
# except Exception as e:
#     # print('encountered a problem for ', offset_index) #
#     print('I encountered this error: ',e)
#
#
#
#
# query_v3 = """
#     PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#
#     SELECT ?s ?o ?lang
#     WHERE {
#      ?s wdt:P10192 ?o. # version 3
#      BIND(LANG(?o) AS ?lang)
#     }
#     """
#
# sparql.setQuery(query_v3)
#
# try:
#     ret = sparql.queryAndConvert()
#
#     for r in ret["results"]["bindings"]:
#         s = r['s']['value']
#         o = r['o']['value']
#         lang = r['lang']['value']
#         print(s, o, lang)
#         if lang =='':
#             extra_ttl_file_v3.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P10192> \""+ o + "\" .\n")
#         else:
#             extra_ttl_file_v3.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P10192> \""+ o+ "\"\@" + lang + ' .\n')
#             # extra_ttl_file.write('<'+ s+ "> <http://dbpedia.org/ontology/wikiPageDisambiguates> <"+ o+ '> .\n')
#
# except Exception as e:
#     # print('encountered a problem for ', offset_index) #
#     print('I encountered this error: ',e)
#
#
#
#
#

# PART 2: extracting links of Wikidata-GSSO

query_gsso = """
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>

    SELECT ?s ?o ?lang
    WHERE {
     ?s wdt:P9827 ?o. # gsso
     BIND(LANG(?o) AS ?lang)
    }
    """

sparql.setQuery(query_gsso)

try:
    ret = sparql.queryAndConvert()

    for r in ret["results"]["bindings"]:
        s = r['s']['value']
        o = r['o']['value']
        lang = r['lang']['value']
        print(s, o, lang)
        if lang =='':
            extra_ttl_file_gsso.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P9827> \""+ o + "\" .\n")
        else:
            extra_ttl_file_gsso.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P9827> \""+ o+ "\"\@" + lang + ' .\n')
            # extra_ttl_file.write('<'+ s+ "> <http://dbpedia.org/ontology/wikiPageDisambiguates> <"+ o+ '> .\n')

except Exception as e:
    # print('encountered a problem for ', offset_index) #
    print('I encountered this error: ',e)
#
#
#
#

# PART 3: extracting links of Wikidata-QLIT

# query_qlit = """
#     PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#
#     SELECT ?s ?o ?lang
#     WHERE {
#      ?s wdt:P11852 ?o. # gsso
#      BIND(LANG(?o) AS ?lang)
#     }
#     """
#
# sparql.setQuery(query_qlit)
#
# try:
#     ret = sparql.queryAndConvert()
#
#     for r in ret["results"]["bindings"]:
#         s = r['s']['value']
#         o = r['o']['value']
#         lang = r['lang']['value']
#         print(s, o, lang)
#         if lang =='':
#             extra_ttl_file_qlit.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P11852> \""+ o + "\" .\n")
#         else:
#             extra_ttl_file_qlit.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P11852> \""+ o+ "\"\@" + lang + ' .\n')
#             # extra_ttl_file.write('<'+ s+ "> <http://dbpedia.org/ontology/wikiPageDisambiguates> <"+ o+ '> .\n')
#
# except Exception as e:
#     # print('encountered a problem for ', offset_index) #
#     print('I encountered this error: ',e)


# extra_filename_lcsh = 'wikidata-lcsh-links.ttl'
# extra_ttl_file_lcsh = open(extra_filename_lcsh, 'w', newline='')
#

# https://www.wikidata.org/wiki/Property:P244
#
# query_lcsh = """
#     PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#
#     SELECT ?s ?o ?lang
#     WHERE {
#      ?s wdt:P244 ?o. # gsso
#      BIND(LANG(?o) AS ?lang)
#      FILTER (isLiteral(?o) && STRSTARTS(STR(?o), "sh"))
#     }
#     """
#
# sparql.setQuery(query_lcsh)
#
# try:
#     ret = sparql.queryAndConvert()
#
#     for r in ret["results"]["bindings"]:
#         s = r['s']['value']
#         o = r['o']['value']
#         lang = r['lang']['value']
#         # print(s, o, lang)
#         if lang =='':
#             extra_ttl_file_lcsh.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P244> \""+ o + "\" .\n")
#         else:
#             extra_ttl_file_lcsh.write('<'+ s+ "> <http://www.wikidata.org/prop/direct/P244> \""+ o+ "\"\@" + lang + ' .\n')
#             # extra_ttl_file.write('<'+ s+ "> <http://dbpedia.org/ontology/wikiPageDisambiguates> <"+ o+ '> .\n')
#
# except Exception as e:
#     # print('encountered a problem for ', offset_index) #
#     print('I encountered this error: ',e)


# query_lcsh = """
#     PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#
#     SELECT (COUNT (*) as ?ct)
#     WHERE {
#      ?s wdt:P244 ?o. # gsso
#      BIND(LANG(?o) AS ?lang)
#      FILTER (isLiteral(?o) && STRSTARTS(STR(?o), "sh"))
#     }
#     """

# https://www.wikidata.org/wiki/Q1823134
# query_lcsh = """
#     PREFIX wiki: <https://www.wikidata.org/wiki/>
#
#     SELECT (COUNT (*) as ?ct)
#     WHERE {
#      ?s wiki:Q1823134 ?o. # gsso
#      BIND(LANG(?o) AS ?lang)
#      FILTER (isLiteral(?o) && STRSTARTS(STR(?o), "sh"))
#     }
#     """
#
#
# sparql.setQuery(query_lcsh)
#
# try:
#     ret = sparql.queryAndConvert()
#
#     for r in ret["results"]["bindings"]:
#         ct = r['ct']['value']
#         print(ct)
# except Exception as e:
#     # print('encountered a problem for ', offset_index) #
#     print('I encountered this error: ',e)
