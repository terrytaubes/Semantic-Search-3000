# coding: utf-8

"""
Similarity Scoring
"""

import gensim
from operator import itemgetter
from math import factorial
import re

import settings
import models



def compute_similarity_lsa(query_words, display):


    ## Define LSI (LSA) Space
    lsi = gensim.models.LsiModel(settings.corpus, id2word=settings.frequency_dict, num_topics=2)

    # Bag of Words for query
    vec_bow = settings.frequency_dict.doc2bow(query_words)
    vec_lsi = lsi[vec_bow]

    index = gensim.similarities.MatrixSimilarity(lsi[settings.corpus])

    ## Perform similarity query against corpus
    sims = index[vec_lsi]
    
    
    sims = [sorted(enumerate(sims), key=lambda score: -score[1])]
    #print sims

    scores_lsa = []

    for sim_entry in sims:
        for i, entry in enumerate(sim_entry):
            scores_lsa.append([sim_entry[i][0], settings.doc_names[sim_entry[i][0]], sim_entry[i][1]])

    if display:
        print 'Results between Vector Space of the Query and Vector Space of the Document Group'
        for i, score in enumerate(scores_lsa):
            if i == 20:
                break
            print score
        print ''

    return scores_lsa


def compute_similarity_title(query_words, display):

    scores_title = []

    for doc in settings.doc_names:
        doc_name = re.sub('.txt', '', doc).lower().split()
        #print doc_name

        match = 0
        
        for word in query_words:
            if word in doc_name:
                match += 1
        match /= float(len(query_words))

        scores_title.append([doc, match])

    scores_title = sorted(scores_title, key=itemgetter(1))
    scores_title = scores_title[::-1]

    if display:
        print 'Results of matching Query words within Document titles:'
        for i, score in enumerate(scores_title):
            if i == 20:
                break
            print score
        print ''

    return scores_title


def compute_similarity_tfidf(query_matrix_df, display):

    #print query_matrix_df

    sums = query_matrix_df.sum(axis=0)


    scores_tfidf = []

    for i, doc in enumerate(settings.doc_names):
        length = float(len(settings.doc_info[doc]['tokens']))
        scores = []
        scores.append(i)
        scores.append(doc)
        scores.append(sums.loc[doc] / length)
        scores_tfidf.append(scores)
        
    scores_tfidf = sorted(scores_tfidf, key=itemgetter(2))
    scores_tfidf = scores_tfidf[::-1]

    #print scores_tfidf

    if display:
        print 'query occurrences\n', sums, '\n'

        print 'Results of the term frequency-inverse document frequency calculation for Query words:'
        for i, score in enumerate(scores_tfidf):
            if i == 20:
                break
            print score
        print ''

    return scores_tfidf


def compute_similarity_tfidf_api(api_matrix_df, display):

    sums = api_matrix_df.sum(axis=0)


    scores_tfidf_api = []

    for i, doc in enumerate(settings.doc_names):
        length = float(len(settings.doc_info[doc]['tokens']))
        scores = []
        scores.append(i)
        scores.append(doc)
        scores.append(sums.loc[doc] / length)
        scores_tfidf_api.append(scores)
        
    scores_tfidf_api = sorted(scores_tfidf_api, key=itemgetter(2))
    scores_tfidf_api = scores_tfidf_api[::-1]

    #print scores_tfidf

    if display:
        print 'api occurrences\n', sums, '\n'
        
        print 'Results of the term frequency-inverse document frequency calculation for API words'
        for i, score in enumerate(scores_tfidf_api):
            if i == 20:
                break
            print score
        print ''

    return scores_tfidf_api


def compute_similarity_ww(query_words, ww_count, display):

    if len(query_words) <= 2:
        num_combs = 1
    else:
        num_combs = (factorial(len(query_words)) / (factorial(2) * factorial(len(query_words) - 2)))
    #print num_combs

    for i in range(len(ww_count)):
        ww_count[i][2] /= num_combs

    scores_ww = sorted(ww_count, key=itemgetter(2))
    scores_ww = scores_ww[::-1]

    if display:
        print 'Results of the co-occurrence counts per document, normalized by the number of Query word combinations'
        for i, score in enumerate(scores_ww):
            if i == 20:
                break
            print score
        print ''

    return scores_ww




def similarity_score(query_words, query_matrix_df, api_matrix_df, word_word_counts, display):

    total_scores_computation = {}
    total_scores_vote = {}

    scores_lsa = compute_similarity_lsa(query_words, display)
    scores_title = compute_similarity_title(query_words, display)
    scores_tfidf = compute_similarity_tfidf(query_matrix_df, display)
    scores_tfidf_api = compute_similarity_tfidf_api(api_matrix_df, display)
    scores_ww = compute_similarity_ww(query_words, word_word_counts, display)

    doc_values = []

    for idx, doc in enumerate(settings.doc_names):
        doc_row = []
        doc_row.append(idx)
        doc_row.append(doc)
        for i, score in enumerate(scores_lsa):
            if doc == score[1]:
                doc_row.append(score[2]/float(2))

        for i, score in enumerate(scores_title):
            if doc == score[0]:
                doc_row[2] += (score[1]/float(2))

        for i, score in enumerate(scores_tfidf):
            if doc == score[1]:
                doc_row[2] += ((score[2]*10)/float(2))

        for i, score in enumerate(scores_tfidf_api):
            if doc == score[1]:
                doc_row[2] += ((score[2]*10)/float(6))

        for i, score in enumerate(scores_ww):
            if doc == score[1]:
                doc_row[2] += ((score[2]*10)/float(5))

        doc_values.append(doc_row)
    
    doc_byscore = sorted(doc_values, key=itemgetter(2))
    doc_byscore = doc_byscore[::-1]

    max_score = doc_byscore[0][2]

    for doc in doc_byscore:
        doc[2] /= max_score

    if display:
        print '\nDocuments by Calculated Score'
        for i, doc in enumerate(doc_byscore):
            if i == 10:
                break
            print doc

    return doc_byscore    

    
