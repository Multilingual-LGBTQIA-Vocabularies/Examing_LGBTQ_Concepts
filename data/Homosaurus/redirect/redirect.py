# This script evaluates all the entities in Homosaurus v2 and v3 and that in GSSO.
# Note that some terms were not in v3 but referenced in GSSO.

# There are  1800  entities in v2
# There are  3149  entities in v3

# There are  1737  redirected entities in v2
# Among them,  1736 are just redirection from http to https.
# There are  63  redirected entities in v3

# The redirection test was conducted on 30th April, 2024, between 6PM and 8PM.
# We used the LOD server for the test.

import time
import networkx as nx
import sys
import csv
import requests
from requests.exceptions import Timeout
import pickle
from rdflib import Graph

from datetime import datetime

start_time = datetime.now()

sameas = 'http://www.w3.org/2002/07/owl#sameAs'
my_redirect = "https://krr.triply.cc/krr/metalink/def/redirectedTo"  # the redirect relation


from selenium import webdriver

def test_redirect(url):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        # options.addArguments("--disable-web-security"); # disable block of pop up redirection
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        final_url = driver.current_url

        return final_url

    except Exception as e:
        return None
    

# Example usage


# load graph v2 and v3

g_gsso = Graph()
g_gsso.parse('./gsso.owl')

g_homosaurus_v2 = Graph()
g_homosaurus_v2.parse('v2.ttl')

g_homosaurus_v3 = Graph()
g_homosaurus_v3.parse('v3.ttl')


prefix_h2 = 'http://homosaurus.org/v2/'
prefix_h2_https = 'https://homosaurus.org/v2'
prefix_h3 = 'https://homosaurus.org/v3/'


query_v3_subject = """
SELECT DISTINCT ?h
WHERE {
  {
    ?h ?predicate ?object .
    FILTER (CONTAINS(str(?h), "https://homosaurus.org/v3/"))
  }
}
"""

query_v3_object = """
SELECT DISTINCT ?h
WHERE {
  {
    ?subject ?predicate ?h .
    FILTER (CONTAINS(str(?h), "https://homosaurus.org/v3/"))
  }
}
"""

query_v2_subject = """
SELECT DISTINCT ?h
WHERE {
  {
    ?h ?predicate ?object .
    FILTER (CONTAINS(str(?h), "http://homosaurus.org/v2/"))
  }
}
"""

query_v2_object = """
SELECT DISTINCT ?h
WHERE {
  {
    ?subject ?predicate ?h .
    FILTER (CONTAINS(str(?h), "http://homosaurus.org/v2/"))
  }
}
"""

query_v2_subject_https = """
SELECT DISTINCT ?h
WHERE {
  {
    ?h ?predicate ?object .
    FILTER (CONTAINS(str(?h), "https://homosaurus.org/v2/"))
  }
}
"""

query_v2_object_https = """
SELECT DISTINCT ?h
WHERE {
  {
    ?subject ?predicate ?h .
    FILTER (CONTAINS(str(?h), "https://homosaurus.org/v2/"))
  }
}
"""

entities_v2 = set()
entities_v3 = set()

for g in [g_gsso, g_homosaurus_v2, g_homosaurus_v3]:
    for  q in [query_v3_subject, query_v3_object]:
        qres = g.query(q)
        for row in qres:
            entities_v3.add(str(row.h))

    for q in [query_v2_subject, query_v2_object, query_v2_object_https,query_v2_subject_https]:
        qres = g.query(q)
        for row in qres:
            entities_v2.add(str(row.h))

# There are  1800  entities in v2
# There are  3149  entities in v3

print('There are ', len(entities_v2),' entities in v2')
print('There are ', len(entities_v3),' entities in v3')

# redirect
# <https://homosaurus.org/v3/
# https://homosaurus.org/v3/homoit0000107 -> https://homosaurus.org/v3/homoit0000894
pair_redirected_v2 = []
count_v2 = 0
count_v2_http_https =0
for e in list(entities_v2):
    count_v2 += 1
    if count_v2 %100 ==0:
        print (count_v2, flush=True)
    result = test_redirect(e)
    # print (e, '->', result )
    if result !=e and result !=None:
        # print (e, ' was redirected to ', result)
        if  e[e.index('//'):] ==  result[result.index('//'):]: # we give http->https an exemption
            count_v2_http_https += 1
        pair_redirected_v2.append((e, result))

pair_redirected_v3 = []
count_v3 = 0
for e in list(entities_v3):
    count_v3 += 1
    if count_v3 %100 ==0:
        print (count_v3, flush=True)
    result = test_redirect(e)
    # print (e, '->', result )
    if result !=e and result !=None:
        print (e, ' -> ', result)
        pair_redirected_v3.append((e, result))

print('There are ', len(pair_redirected_v2),' redirected entities in v2')
print ('Among them, ', count_v2_http_https, 'are just redirection from http to https.')
print('There are ', len(pair_redirected_v3),' redirected entities in v3')

dir = './redirect/'
summary_file_v2 =  open (dir+'redirected_entities_v2.csv', mode='w', newline='')
summary_writer_v2 = csv.writer(summary_file_v2)
summary_writer_v2.writerow(['Source', 'Redirected'])
for (e, r) in pair_redirected_v2:
    summary_writer_v2.writerow([e, r])
summary_file_v2.close()

summary_file_v3 =  open (dir+'redirected_entities_v3.csv', mode='w', newline='')
summary_writer_v3 = csv.writer(summary_file_v3)
summary_writer_v3.writerow(['Source', 'Redirected'])
for (e, r) in pair_redirected_v3:
    summary_writer_v3.writerow([e, r])
summary_file_v3.close()

time_elapsed = datetime.now() - start_time
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
