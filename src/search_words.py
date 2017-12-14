# coding: utf-8

"""
Get API Synonyms
"""


import mw_thesaurus as mw
import wordnet_interface as wn
import wiki_extract as wiki

def get_similar(query_words):
    
    ## Added Features from Merriam-Webster, WordNet and Wikipedia APIs
    api_syns = []


    ####  [ Extract synonyms for each word in query_words ]  ####
    
    for word in query_words:
        
        ## Merriam-Webster Thesaurus API
        try:
            mw_list = mw.find_similar(word)
        except:
            mw_list = []
        api_syns.extend(mw_list)

        ## WordNet Database API
        wn_list = wn.wordnet_syns(word)
        api_syns.extend(wn_list)

        ## Wikipedia API
        wiki_list = wiki.find_similar(word)
        api_syns.extend(wiki_list)
        

    api_syns = [x.lower() for x in api_syns if x not in query_words]

    api_syns = list(set(api_syns))
    #print api_syns


    return api_syns

