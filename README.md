The Apples-to-Apples API (A2A-API) is a RESTful API that serves as an easy-to-use and programming-language-independent interface to existing biomedical TREC collections. It builds upon A2A (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-020-03894-8), our system for biomedical information retrieval bench-marking, and extends it with additional functionalities. The A2A-API provides programmatic access to the features of the original A2A system and support biomedical IR researchers in the development of systems featuring reranking and query reformulation components. This repository showcases several examples of using the A2A-API for Biomedical Information Retrieval Research.

Examples:
- `Example_1.py`: Showcases all A2A-API methods and hyperparameters 
- `Example_2.py`: Outlines the structure of a typical program using A2A, that compares reranking and reformulation methods
- `Example_3_T5Reranking.ipynb`: Demonstrates the complete code for implementation of T5 reranking (https://arxiv.org/abs/2003.06713) with the A2A-API, in combination with Pytorch Lightning and 🤗 Transformers
- `Example_4_BERTReranking&Downloaded_Data.ipynb`: Re-implements our BERT reranking system, which came 3rd. in the TREC2021 Clinical Trials Track. Also highlights how data from the A2A-API can be stored to avoid repeated downloads.
