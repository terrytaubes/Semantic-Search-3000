# coding: utf-8

"""
Menu Functions
"""

import re

import settings
import models
import search_words as sw
import document_matrix as dm
import similarity as sim


#### Menu Functions ####


"""
search():

This is the search function that is called from the menu.
   The input query is normalized, lemmatized, and returned in a list.
Then, API synonyms are extracted using the Princeton WordNet, Merriam-
   Webster Thesaurus, and Wikipedia APIs.
The query words and API synonyms are then used to create Term-Document
   matrices with the current document group.
The query_words are also used to get the summed counts within our
   pseudo-Word-Word matrix (explained within the function's documentation).
Our query_words, query_matrix_df, api_matrix_df, and word_word_counts are
   used as 4 of the 5 components within our similarity scoring function.
   The fifth component, query word matches in document names, is computed
   directly within similarity.py's scoring function.
Returns an ordered list of lists containing [docID, doc name, similarity score].

param:      n/a
return:     doc_byscore     =  List of [docID, doc name, similarity score],
                                  ordered by highest relevancy to the query.
"""
def search(query_input):
    
    query = query_input.lower()


    ####  [ Query Preprocessing ]  ####
    ##                               ####
    ##  Step 1: Remove Punctuation   
    ##  Step 2: Tokenize Clitics     
    ##  Step 3: List of lemmatized, lowercase query words 
    ##  
    ##  (1) query_words     :  list of search terms from user input

    query_nopunc = re.sub(r'[,\.!\?;:\'"\)\(]', r'', query)
    query_noclitics = re.sub(r"\'", r' ', query_nopunc)

    ##      (1)
    query_words = [settings.lmtzr.lemmatize(x.lower()).decode() for x in query_noclitics.split()]

    ####  [ Get Related Search Features ]  ####
    ##                               ######
    ##  (2) api_syns            :  list of all extracted API synonyms
    
    ##   (2)
    api_syns = sw.get_similar(query_words)


    ####  [ Build Term-Document Matrices ]  ####
    ##                                        ######
    ##  (3) query_matrix_df  :  DataFrame of 'query words vs documents' frequencies
    ##  (4) api_matrix_df    :  DataFrame of 'api synonyms vs documents' frequencies
    ##
    ## Note: We separate query and api words matrices to keep the query matrix small
    ##         and to give the query matrix a higher weight in the similarity scoring.
    ##       We use Pandas DataFrames for later visualization in the GUI.

    ##          (3),           (4)
    query_matrix_df, api_matrix_df = dm.term_document(query_words, api_syns)

    settings.term_doc_df = query_matrix_df

    ####  [ Word-Word Matrices Counts ]  ####
    ##
    ##  (5) word_word_counts  :  List of documents and their word_word co-occurrences,
    ##                             normalized by the total number of possible combinations
    ##                             of the query words, and sorted in order of greatest
    ##                             number of co-occurrences.

    ##           (5)
    word_word_counts = dm.word_word(query_words)


    ####  [ Display ]  ####

    display = False

    if display:

        ## Query Words
        print '\n', query_words

        ## API Synonyms
        print '\n', api_syns
        
        ## Print Preview of Each Document's Text ##
        
        print ''
        #for name in settings.doc_names:
        #    print '%s \t:\t %s [...]' % (name, settings.doc_info[name]['text'][:40])
        #print ''

    
    ##                           (1),            (3),            (4),              (5)
    doc_byscore = sim.similarity_score(query_words, query_matrix_df, api_matrix_df, word_word_counts, display)

    return doc_byscore


"""
select_document_group():

Menu function that generates our 'system call' to settings.py to change and
   load document group models.

param:      group   =  User-specified document group to select
return:     n/a
"""
def select_document_group(group):
    
    settings.get_document_group(group)

    return


"""
upload_documents():

Menu function that generates our 'system call' to settings.py to build and
   select a new document model.

param:      group   =  User-specified document group to upload
return:     n/a
"""
def upload_documents(group):
    
    settings.build_document_model(group)
    
    return



## print_menu():  Print menu functions to console

def print_menu():
    
    print "1) Search"
    print "2) Select Document Group"
    print "3) Upload Document Group"
    print "4) exit"



## command():  Multi-purpose user input function
    
def command(cmd="Select", menu=True):

    if (menu):
        option = raw_input(cmd+': ')[0]
    else:
        option = raw_input(cmd+': ')

    return option

    
## if document group not specified, select doc group
"""
run():

Runs the applications back-end functions when menu functions
   are selected by the user

param:      n/a
return:     n/a
"""
def run():

    run = True

    while (run):
        
        print_menu()
        cmd = command()

        if cmd == '1':
            query_input = raw_input("Search: ")
            doc_byscore = search(query_input)
        elif cmd == '2':
            g = command(cmd='Select Group', menu=False)
            select_document_group(g)
        elif cmd == '3':
            g = command(cmd='Select Group', menu=False)
            upload_documents(g)
        elif cmd == '4':
            run = False

        print '--------------------'
        
    

