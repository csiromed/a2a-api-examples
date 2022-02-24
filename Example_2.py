#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 12:11:40 2022

@author: Maciek Rybinski
"""

## A general structure of a workflow supported by A2A-API, illustrated with
## reranker training using TREC PM 2017 clinical trials task and evaluation
## on TREC PM 2018 clinical trials task
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

def unzip_and_read_json(response):
    return {}

def prepare_data_and_train_reranker(qrels, docs, topics, training_params):
    ## Data wrangling and training logic goes here
    return None

def query_reformulation(topics):
    path_to_reformulated_topics_xml_file='./data/topics/topics2018.xml'
    ## Query reformulation logic goes here
    return path_to_reformulated_topics_xml_file

def rerank_and_save_trec_output(initial_ranking, documents, topics, reranking_model):
    path_to_reranked_file='ct2018_raw_bm25.results'
    ## Reranking logic goes here
    return path_to_reranked_file



## General workflow structure for the use of A2A api. Within this example we
## use TREC PM 2017 clinical trials task as a training dataset, while the 
## TREC PM 2018 clinical trials task data is used for evaluations.S

### **************** RERANKER TRAINING ****************************

## Get qrel data and document content for docs present in the qrels
x = requests.get('https://a2a.csiro.au/api/qrels/ct2017')
qrels=x.json()
x = requests.get('https://a2a.csiro.au/api/qrel_docs/ct2017')
qrel_docs=unzip_and_read_json(x)
topics2017 = requests.get('https://a2a.csiro.au/api/topics/ct2017').json()
reranker=prepare_data_and_train_reranker(qrels, qrel_docs, topics2017,[])

### **************** QUERY REFORMULATION **************************

###
## Get topics (queries) for the 'test' task (here ct2018)
x = requests.get('https://a2a.csiro.au/api/topics/ct2018')
topics=x.json()
new_topic_file=query_reformulation(topics)

### **************** RERANKING (inference) ************************

## Get a baseline result
x = requests.get('https://a2a.csiro.au/api/bm25/ct2018')
bm25_baseline=x.json()
## Save it to disk
bm25_data=to_trec(bm25_baseline['rankings'], run_id='ct2018_raw_bm25')
## Get document data for top k(=20) documents in the baseline ranking
files = {'file': open('ct2018_raw_bm25.results','rb')}
x = requests.post('https://a2a.csiro.au/api/result_docs/ct2018?k=20', files=files)
bm25_docs=x.json()
reranked_output=rerank_and_save_trec_output(bm25_data, bm25_docs, topics, reranker)

### **************** EVALUATIONS (reranking vs reformulation) ***********
files = {'file': open(reranked_output,'rb')}
x = requests.post('https://a2a.csiro.au/api/eval/ct2018', files=files)
reranked_results=x.json()

### reformulated queries (e.g., disease synonyms) could be saved into the disease field
files = {'file': open(new_topic_file,'rb')}
x = requests.post('https://a2a.csiro.au/api/dfr/ct2018?t=$disease $gene', files=files)
reformulated_results=x.json()
