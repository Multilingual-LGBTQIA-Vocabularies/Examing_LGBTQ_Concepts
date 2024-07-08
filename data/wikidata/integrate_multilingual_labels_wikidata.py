# load csv files and convert it to a nt file

import csv



from SPARQLWrapper import SPARQLWrapper, JSON
import validators
from rdflib import Graph, URIRef, Literal


G = Graph()

predicates_filename = [
# ('http://www.w3.org/2000/01/rdf-schema#label', 'extracted_multilingual_rdfs:label.tsv'),
# ('http://www.w3.org/2004/02/skos/core#altLabel', 'extracted_multilingual_skos:altLabel.tsv')
('http://schema.org/description', 'extracted_multilingual_schema:description.tsv')
]

for (p, f) in predicates_filename:
    print ('working on predicate ', p)

    input_file = csv.DictReader(open(f), delimiter='\t')
    for row in input_file:
        # print('subject = ', row['subject'])
        # print('label = ', row['label'])
        # print('lang = ', row['lang'])
        subj = row['subject']
        label = row['label']
        lang = row['lang']
        # break
        subject = URIRef(row['subject'])
        predicate = URIRef(p)
        label_with_lang = None

        if lang != '':
            label_with_lang = Literal(label, lang=lang)
        else:
            label_with_lang = Literal(label)
            print ('no language label for ', str(subject))

        G.add((subject, predicate, label_with_lang))

# G.serialize("integrated_labels.nt", format="nt")
G.serialize("integrated_descriptions.nt", format="nt")
G.close()

# subject label   lang
