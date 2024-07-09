
# Examining LGBTQ+-related Concepts in the Semantic Web

## Introduction

Welcome to the project. We study the links between LGBTQ+ ontologies and structured
vocabularies. More spcifically, we focus on GSSO, Homosaurus, QLIT, and Wikidata.
The code is free for use with the license CC-BY 4.0. You can resue/extend the code
for free as long as you give credits to us in your publication/data. Citation
information will be added after the corresponding paper gets accepted. If you are
citing this dataset, please use the DOI: 10.5281/zenodo.12684869. The paper is
under submission and will be added after being accepted.

## This repository is organised as follows:

- ./data/ consists of datasets retrieved from the websites of GSSO, Homosaurus, QLIT,
LCSH, Wikidata, etc. In the directories of each folder, you can also find also the scripts
for pre-processing and the resulting data in different formats. Files about redirection of
entities in Homosaurus can also be found here.

- ./integrated_data/ is the repository where the integrated data supposed to be located if
you follow the steps below. Due to the strict CC-BY-NC-ND license of GSSO and Homosaurus,
the integrated data is NOT included. However, it can be easily reproduced for reproduction
of the results. The integrated data is also available upon request from the authors as well
as the members of QLIT, IHLIA, and GSSO (see the Contact and Acknowledgement section below).

-./analysis_integrated_graph/ consists of Python scripts for analyzing the integrated graph.

- ./discover_missing_links/ consists of the scripts for the discovery of missing links using
Weakly Connected Components. The missing links were revised by Swedish-speaking experts in
the QLIT team. See below for more details.

- ./SPARQL/ is the directory where all the SPARQL queries can be found.

- There are three folders for the analysis of multilingual information reuse: ./WCC-based_gsso_multilingual_info_reuse, ./WCC-based_wikidata_multilingual_info_reuse/ ./WCC-based-QLIT-info-reuse-from-Wikidata. Additionally, there is some tests for GSSO in the folder ./additional_test_gsso_multilingual_info_reuse. You can find more detials below.


Although we cannot include the integrated data and some intermediate data due to the strict
license of GSSO and Homosaurus, below is a step-by-step guide for the reproduction of the results.
It is easy to generate all the results presented in the paper. So far, the discovered
links have been revised by experts from QLIT. The other discovered links and reported mistaken links
are being revised by the LGBTQ+ structured vocabulary community. It can take some time for the community
to decide what to remove and what to add. All the scripts are free to be used for examination and
evaluation of future versions of GSSO, Homosaurus, Wikidata, QLIT, and others.

If you would like to help evaluate the newly discovered labels for entities for a language you
can speak fluently (native speaker or confident with professional use), please let us know.



## Step 1: Preparing the data

In this project, the following datasets were used:

- QLIT: version 1.0
- Homosaurus: version 3.5 and version 2.3
- Wikidata: retrieved from the SPARQL Endpoint (https://query.wikidata.org/sparql) and processed between 5th May and 8th May, 2024.
- GSSO: we used gsso.owl (version 2.0.10) obtained from its Github (https://github.com/Superraptor/GSSO).
- LCSH was obtained from the official website: https://id.loc.gov/authorities/subjects.html on 9th May, 2024. The LCSH data was converted to its HDT format.

Please put the corresponding files in the following folders (and change its names where necessary) to make sure that the Python scripts can find your code.

- ./data/GSSO/gsso.owl
- ./data/Homosaurus/v2.ttl and ./data/Homosaurus/v3.ttl
- ./data/LCSH/lcsh.hdt (we used its HDT format for fast query and analysis). The original file is also attached: subjects.skosrdf.nt.
- ./data/QLIT/Qlit-v1.ttl

The case of Wikidata is more complicated. The following scripts were used for the retrival of data. These scripts are all in the folder ./data/wikidata/

- We used the Wikidata SPARQL endpoint:
https://query.wikidata.org/

The following relations from Wikidata were used while extracting triples.
- Wikidata - GSSO:          http://www.wikidata.org/prop/direct/P9827
- Wikidata - Homosaurus 2:  http://www.wikidata.org/prop/direct/P6417
- Wikidata - Homosaurus 3:  http://www.wikidata.org/prop/direct/P10192
- Wikidata - LCSH:          http://www.wikidata.org/prop/direct/P244

The generated files are:
- 'wikidata-homosaurus-v2-links.nt'
- 'wikidata-homosaurus-v3-links.nt'
- 'wikidata-gsso-links.nt'
- 'wikidata-qlit-links.nt'
- 'wikidata-lcsh-links-all.nt'

Please note that the case of Wikdiata-LCSH is more complicated: there are so many links that are nothing to do with the entities in our scope. We restrict it to only entities in the scope of this paper. See below for more details.


You can find all the scripts in the corresponding folder in the data folder.

All the SPARQL queries used can be found in the folder ./SPARQL/

Note! For GSSO, the following two mistakes were corrected while preprocessing:

- https://www.wikidata.org/wiki/Q1823134 should not be used as a relation. We have replaced it with http://www.wikidata.org/prop/direct/P244.
- Instead of referring to the page, we refer to the entity. We use http://www.wikidata.org/entity/* instead of https://www.wikidata.org/wiki/*

The redirection test was conducted on 30th April, 2024, between 6PM and 8PM. The files can be found in the folder of ./data/Homosaurus/redirect/.

## Integrating the data

In the folder ./integrated_data/, you can find all the scripts related to the integrated data. Unfortunately, due to the CC-BY-NC-ND license of GSSO and Homosaurus, the integrated data will not be made available. But you can generate it with the instructions above and by using the following scripts.

The script ./integrated_data/integrate.py takes advantage of the data generated. It first integrates a list of files of links. Then we go through the links between Wikidata and LCSH. Only those that are in the scope of the study are included.

- If your steps are correct and using the same version as we did, you should be able to get four files:
- a) the integrated file as integrated.nt
- b) the links that are relevant for this study: wikidata-lcsh-links-selected.nt.
- c) a plot of the distribution of the size of WCCs
- d) a mapping of entities and their corresponding ID of WCCs.


## Weakly Connected Components

The weakly connected components (WCCs) were computed for the following three purposes:

a) Discovering missing links. See the section below for details.

b) The WCCs can be used for manual examination. These are entities that form clusters about related concepts. The intuition is that the larger they are, the more likely there is concept drift/change, ambiguity, and mistakes.

c) Multilingual information reuse. Smaller WCCs with exactly one entity from each dataset (e.g. Homosaurus and Wikidata) can then be used to suggest labels for the one with fewer labels for some given languages. See below for more details.

As mentioned above, the distribution has been plotted. You can find this plot here: ./integrated_data/frequency.png

In the folder ./integrated_data/weakly_connected_components/, you can find all the WCCs and their links.

Two examples were given in the folder. The largest WCC about sex, gender, fucking, etc. The other is about BDSM and fetish.

## Discovering missing and outdated links

Taking advantage of WCCs, we can further find missing and outdated links. The scripts are in the folder ./discover_missing_links.

Three examples were given. The first two is about discovering missing links. The last one is about finding outdated links.

- The script ./discover_missing_links/discover_H3_LCSH.py and ./discover_missing_links/discover_QLIT_LCSH.py are scripts that outputs links that could be missing in Homosaurus and QLIT respectively. This was computed by looking at the WCCs. If two entities are both involved in the same WCC, there could be a link between them. The csv files in the same folder are the corresponding links found.

- The script ./discover_missing_links/find_qlit_outdated_links/ is used to discover the outdated links between QLIT and Homosaurus v3. There was only one link found.

- The 105 potentially missing links were taken for further review by Swedish-speaking experts from the QLIT team, which showed that 78 (72.38%) suggested links should be included: 38 (36.19%) can be included using skos:exactMatch and another 38 (36.19%) using skos:closeMatch. 28 (26.67%) suggested links are incorrect. The manual annotation are included in the file ./discover_missing_links/Annotated_found_new_links_qlit-lcsh.xlsx.

## Multilingual Information Reuse

You can find two attempts in the folders about the use of GSSO and Wikidata for Homosaurus respectively.
- ./WCC-based-gsso-multilingual_info_reuse/
- ./WCC-based-wikidata-multilingual_info_reuse/

Additionally, we provide also some code for the reuse of Wikidata multilingual info for QLIT. It's in the folder
- ./WCC-based-QLIT-info-reuse-from-Wikidata/

They follow very similar steps:

1. Compute the one-to-one mapping using the WCCs. The script is named compute-one-to-one-mapping.py

2. Extract the multilingual labels from sources. The corresponding file is extract_multilingual_labels_from_one_to_one_mappings.py

3. Provide the extracted multilingual as suggestions for targeting entities. The name of the corresponding files are like "*suggesting-labels.py", where the * is replaced by the actual source/target.


For GSSO, we use the following relations:
- http://www.w3.org/2000/01/rdf-schema#label
- http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym
- http://www.geneontology.org/formats/oboInOwl#hasSynonym
- http://www.geneontology.org/formats/oboInOwl#hasExactSynonym
- http://purl.org/dc/terms/replaces
- https://www.wikidata.org/wiki/Property:P5191
- https://www.wikidata.org/wiki/Property:P1813
- https://schema.org/alternateName
- http://www.w3.org/2002/07/owl#annotatedTarget

Additionally, we found the relation to be studied in the future: http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym

For Wikidata, there are only two:
- http://www.w3.org/2000/01/rdf-schema#label
- http://www.w3.org/2004/02/skos/core#altLabel


## Additional analysis

Additionally, we perform an analysis using only redirection and replacement for GSSO and Homosaurus. The scripts are in the folder ./additional_test_gsso_multilingual_info_reuse. We consider also Homosaurus v2.
This additional analysis shows the following:

- For the Turkish language, in total there are  103  triples about labels about 23 entities. The average suggested labels per entity is 3.0.

- For the Spanish language, in total there are  205  triples about labels about 43 entities. The average suggested labels per entity is 2.12.

- For the French language, in total there are  277  triples about labels about 47 entities. The average suggested labels per entity is 2.19.

- For the Danish language, in total there are  115  triples about labels about 47 entities. The average suggested labels per entity is 2.70.


Some analysis about the replacement relations of Homosaurus is in the folder ./data/Homosaurus/replace_relations_homosaurus/.

Finally, some additional analysis is included in the folder ./analysis_integrated_graph. Currently there is only one that is about outdated entities in Homosaurus v3. Some more analysis will be added in the future.


## Acknowledgement
The authors appreciate the help of the following researchers:
- Siska Humlesjö, QLIT, Göteborgs Universitet (siska.humlesjo@lir.gu.se)
- Olov Kriström, former member of QLIT
- Jack van der Wel, IHLIA (jack@ihlia.nl)
- Clair Kronk, GSSO (clair.kronk@mountsinai.org)

## Contact
- Shuai Wang, Vrije Universiteit Amsterdam (shuai.wang@vu.nl)
- Maria Adamidou, Vrije Universiteit Amsterdam (m.adamidou@student.vu.nl)


The Readme file was generated using [Readme.so](https://readme.so/editor).
