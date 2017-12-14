# coding: utf-8

"""
Document Matrix Functions
"""

import numpy as np
import pandas as pd

import settings


## Document Matrix Functions


"""
term_document():

This function builds the Term-Document matrices for the query words and the
   extracted API synonyms, separately. The Term-Documents are turned into
   Pandas DataFrames for visualization purposes within the GUI.

param:      query_words     =  List of query words
            api_syns        =  List of API synonym words
            
return:     query_matrix_df =  Pandas DataFrame of 'query words x documents'
            api_matrix_df   =  Pandas DataFrame of 'api synonyms x documents'
"""
def term_document(query_words, api_syns):

    ## For our term_document matrix we will be using Pandas
    ##   to build a dataframe to hold our data and also for
    ##   easy visualization that may be utilized later on

    query_matrix = {}
    api_matrix = {}

    for doc in settings.doc_names:
        doc_vector = [0 for x in range(len(query_words))]
        api_vector = [0 for x in range(len(api_syns))]
        doc_tokens = settings.doc_info[doc]['tokens']
        
        for i, word in enumerate(query_words):
            if word in doc_tokens:
                doc_vector[i] = doc_tokens.count(word)
        for j, word in enumerate(api_syns):
            if word in doc_tokens:
                api_vector[i] = doc_tokens.count(word)
        #print doc_vector
        query_matrix[doc] = doc_vector
        api_matrix[doc] = api_vector


    index = pd.Index([str(x) for x in query_words])

    ## (1), (2)
    query_matrix_df = pd.DataFrame(data=query_matrix, index=index)
    api_matrix_df = pd.DataFrame(data=api_matrix)
    
    #print query_matrix_df
    #print api_matrix_df

    ##                 (1),          (2)
    return query_matrix_df, api_matrix_df



"""
word_word():

This function builds a 'psuedo-Word-Word matrix' for the query words.
   This instead simply counts the word-word frequencies for each document,
   simplifying the process necessary to use the values of an actual Word-Word
   matrix. A Pandas DataFrame of this matrix is not needed for visualization.

param:      query_words     =  List of query words
            api_syns        =  List of API synonym words
            
return:     query_matrix_df =  Pandas DataFrame of 'query words x documents'
            api_matrix_df   =  Pandas DataFrame of 'api synonyms x documents'
"""
def word_word(query_words):

    ww_count = []

    #print query_words
    #print ''
    for i, doc in enumerate(settings.doc_names):
        
        count = 0
        for word1 in query_words:
            for word2 in query_words:
                    
                if word1 != word2:
                    if (word1 in settings.doc_info[doc]['tokens'] and word2 in settings.doc_info[doc]['tokens']):
                        count += 1

        #print doc, count/float(2)
                        
        ww_count.append([i, doc, count/float(2)])

        
    return ww_count

