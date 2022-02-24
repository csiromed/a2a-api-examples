#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:26:50 2021

@author: ryb003
"""

import requests
import numpy as np

## A method to convert json results to TREC output format
def to_trec(results, run_id='ranking', id_index=0, score_index=1, save_to_disk=True):
    trec_vals=[]
    for topic_id in results:
        j=1
        for row in results[topic_id]:
            new_row=[topic_id, 'Q0', row[id_index], j, row[score_index], run_id]
            trec_vals.append(np.array(new_row))    
            j+=1
    trec_vals=np.array(trec_vals)
    if save_to_disk:
        np.savetxt(str(run_id)+'.results', trec_vals, delimiter="\t", fmt='%s')
    return trec_vals

###
## Calls for getting result sets

# 1 - DFR baseline for 'genomics2004' experiment (C=1)
x = requests.get('http://130.155.193.111:5001/api/dfr/genomics2004')
d1=x.json()

# 2 - DFR baseline for 'ct2017' experiment (C=2) with alternative topic term boosts
x = requests.get('http://130.155.193.111:5001/api/dfr/ct2017?c=2&t=($gene)^2 ($disease)^3')
d2=x.json()

# 2 with rm3 - DFR+RM3 baseline for 'ct2017' experiment (C=2; RM3 parameters: m=10, miu=100, alpha=0.4, k=5)
## note this also works for bm25 (needs substituting dfr->bm25 and c for bm25 params, b and k1, in the call)
x = requests.get('http://130.155.193.111:5001/api/dfr_rm3/ct2017?c=2&m=10&miu=100&alpha=0.4&k=5')
d2_rm3=x.json()

# 2 - DFR baseline for 'ct2017' experiment (C=2)
x = requests.get('http://130.155.193.111:5001/api/dfr/ct2017')
d2_1=x.json()

# 3 - bm25 baseline for 'ct2021_eligible' experiment (b=1, k1=1)
x = requests.get('http://130.155.193.111:5001/api/bm25/ct2021_eligible?b=1&k1=1')
d3=x.json()

# 3_1 - bm25 baseline for 'ct2021' experiment; default parameters
x = requests.get('http://130.155.193.111:5001/api/bm25/ct2021')
d4=x.json()


###
## Handling results dict

# Aggregated metrics:
scores=d3['all']
print (scores)

# Per-topic metrics (e.g., for a boxplot):
scores_per_topic=d3['per_topic']
# Score for the 5th topic:
print(scores_per_topic['5'])
# Get the ranked lists of documents
rankings=d3['rankings']
# This is a dictionary (topic_id -> ranked list of lists; row represents a document)
# Top 10 documents for topic 1
print(rankings['1'][:10])
# Top row doc_id and score (the other rows are gender, max age (days), min age (days)):
print(rankings['1'][0][:2])

# Save this output as TREC results file (ct21_test.results file will be created in current folder):
trec_format=to_trec(rankings, run_id='ct21_test')    

###
## Get a document json (document contents)
doc_id=rankings['1'][0][0]
x = requests.get('http://130.155.193.111:5001/api/doc/ct2021/'+doc_id)
doc=x.json()
# print(doc)

###
## Get topics (queries) for a given task (here ct2021)
x = requests.get('http://130.155.193.111:5001/api/topics/ct2021')
topics=x.json()

### 
## Get qrels (topic-document human judgments) for a specific task
## Row format is: [topic_id, #, doc_id, relevance_score]
x = requests.get('http://130.155.193.111:5001/api/qrels/ct2021')
qrels=x.json()

### 
## Convenience method to get all document IDs (topic-document human judgments) for a specific task
# x = requests.get('http://130.155.193.111:5001/api/all_doc_ids/ct2017')
# all_ids=x.json()


###
## Sending a ranking file for evaluation. We're using ct21_test.results file created earlier. 
## In real usage this could be a re-ranked results sent for evaluation 
## The results object is just like the one for the baseline run, but without the 'rankings' content
files = {'file': open('ct21_test.results','rb')}
x = requests.post('http://130.155.193.111:5001/api/eval/ct2021_eligible', files=files)
results=x.json()
## these two should be the same
print(results['all'])
print(d3['all'])

###
## Post request to get a document dictionary (fields of the documents) for the top k (k=10).
## The request includes a valid results file, for which the documents are fetched.
##
files = {'file': open('ct21_test.results','rb')}
x = requests.post('http://130.155.193.111:5001/api/result_docs/ct2021_eligible?k=10', files=files)
result_docs=x.json()


###
## Call for all documents (all fields) from a given qrel-set. Convenience method for
## compiling an LTR training set directly from historical qrels.
x = requests.get('http://130.155.193.111:5001/api/qrel_docs/sigir_ct')
qrels_docs=x.json()


###
## Any experiment call (BM25/DFR with/without RM3) can be made with a POST request 
## specifying a custom topic XML file, e.g., here is a DFR call for the first two topics
## a 'user_query' topic field can be used as a template (see the file for reference)
files = {'file': open('two_topics_2017.xml','rb')}
x = requests.post('http://130.155.193.111:5001/api/dfr/ct2017?t=$user_query', files=files)
d_custom_topics=x.json()
