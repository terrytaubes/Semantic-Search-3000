# coding: utf-8

"""
settings (initializer)
"""
from nltk.stem.wordnet import WordNetLemmatizer

from models import load_doc_model, create_doc_model


## init(): Initialize global variables and load default user and group model

def init():

    #  > user           :   current user
    #  > group          :   current document group
    #  > path           :   path to current document group
    #  > query          :   most recent query entered by user
    #  >
    #  > doc_vectors    :   current document group's document vectors
    #  > doc_model      :   current document group's document model
    #  > doc_names      :   names of documents in current document group
    #  > doc_info       :   text and indexes of documents in current document group
    #  > frequency_dict :   frequency counts for words in current document group
    #  > corpus         :   bag of words corpus for words in current document group
    #
    #  > term_doc_df    :   current document group's term-document matrix
    #  > lmtzr          :   NLTK WordNetLemmatizer

    
    global user
    global group
    global path
    global query
    global login

    global doc_vectors
    global doc_model
    global doc_names
    global doc_info
    global frequency_dict
    global corpus

    global term_doc_df
    global lmtzr

    user = 'terrytaubes'
    group = 'cs_ml_nlp'

    login = False
    doc_info = {}

    lmtzr = WordNetLemmatizer()


    try:
        doc_vectors, doc_model, doc_names, doc_info, frequency_dict, corpus = load_doc_model(group)
    except IOError:
        try:
            doc_vectors, doc_model, doc_names, doc_info, frequency_dict, corpus = create_doc_model(group)
        except IOError:
            print 'error: cannot find initial document group'


## get_document_group(): Used to switch between document groups,
##                          called from the menu function 'select_document_group(group)'

def get_document_group(new_group):

    group = new_group
    
    try:
        doc_vectors, doc_model, doc_names, doc_info, frequency_dict, corpus = load_doc_model(group)
    except IOError:
        print 'error: finding document group:', group


## build_document_model() : Used to build a model for a chosen document group,
##                             called from the menu function 'upload_documents(group)'
##                             or when a document group is selected by a user and no
##                             model for the document group currently exists.

def build_document_model(group):

    #doc_vectors, doc_model, doc_names, doc_info, frequency_dict, corpus = create_doc_model(group)


    try:
        doc_vectors, doc_model, doc_names, doc_info, frequency_dict, corpus = create_doc_model(group)
    except:
        print 'error: building document model', group
        

