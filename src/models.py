# coding: utf-8

"""
Models
"""

import gensim
import re
from os import listdir, getcwd
from collections import defaultdict
import json


import settings
import mw_thesaurus as mw

TaggedDocument = gensim.models.doc2vec.TaggedDocument


"""
LabeledLineSentence():

This class is used to store information about our documents and to provide
   an iterator to yield TaggedDocuments, used in our LSA space calculation later.
"""   
class LabeledLineSentence(object):
    
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list
        
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument([word for line in doc for word in line.split()], [self.labels_list[idx]])

"""
create_doc_model():


"""
def create_doc_model(group):

    #path = getcwd()
    #path = re.sub(r'src', r'users/', path)
    #path += settings.user+'/'+str(group)+'/Text/'
    path = '../users/'+settings.user+'/'+str(group)+'/Text/'


    docLabels = []
    docLabels = [f for f in listdir(path) if f.endswith('.txt')]
    #print docLabels

    data = []
    for i, doc in enumerate(docLabels):
        data.append(open(path + doc, 'r'))

    it = LabeledLineSentence(data, docLabels)
    

    ###---------------------------------###
    ###  Method 1 for Document Vectors  ###
    ###---------------------------------###

    ## Document Group Model
    doc_model = gensim.models.Doc2Vec(size=300, window=10, min_count=1, workers=4)
    doc_model.build_vocab(it)

    ## Train Document Group Model
    for epoch in range(10):
        doc_model.train(it, total_examples=doc_model.corpus_count, epochs=doc_model.iter)
        doc_model.alpha -= 0.002
        doc_model.min_alpha = doc_model.alpha
        doc_model.train(it, total_examples=doc_model.corpus_count, epochs=doc_model.iter)

    doc_model.delete_temporary_training_data()
        
    ## Save Current Document Group's Vector Representations (1)
    doc_vectors = doc_model.docvecs
    doc_vectors.save('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_vectors')

    ## Save Current Document Group's Model (2)
    doc_model.save('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_model')

    ## Save Document Labels to Text String (3)
    with open('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_docs.txt', 'w') as f:
        for doc in docLabels:
            f.write(doc+'%')

    ###---------------------------------###
    ###  Method 2 for Document Vectors  ###
    ###---------------------------------###

    ## Stop Words to be Removed
    stoplist = set('for a of the and to in'.split())

    tokens = []

    ## Nested List of [[tokens in document] for document in document group]
    for doc in docLabels:
        curr_tokens = []
        with open(path + doc, 'r') as f:
            for word in f.read().lower().split():
                if word not in stoplist:
                    try:
                        curr_tokens.append(settings.lmtzr.lemmatize(word))
                    except UnicodeDecodeError:
                        pass
        tokens.append(curr_tokens)

        
    ## Dictionary of {'Document Name' : {'text':doc_text, 'index':doc_index}}
    doc_info = {}
    for i, doc in enumerate(docLabels):
        doc_info[doc] = {}
        with open(path + doc, 'r') as f:
            doc_info[doc]['text'] = f.read()
        doc_info[doc]['index'] = i
        doc_info[doc]['tokens'] = tokens[i] 
        #print doc_info[doc]['tokens']

    freq_dict = defaultdict(int)
    for doc in tokens:
        for word in doc:
            freq_dict[word] += 1

    tokens = [[word for word in doc if freq_dict[word] > 1] for doc in tokens]


    ## Save Document Text dict as JSON file: (4)
    ##      >> doc_info = {'doc' : {'text' : doc text, 'index' : doc index}
    with open('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_docinfo.txt', 'w') as f:
        f.write(json.dumps(doc_info, sort_keys=True))

    ## Save Frequency Dict of document group (5)
    frequency_dict = gensim.corpora.Dictionary(tokens)
    frequency_dict.save('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'.dict')

    ## Save Bag of Words Corpus for Document Group (6)
    corpus = [frequency_dict.doc2bow(doc) for doc in tokens]
    gensim.corpora.MmCorpus.serialize('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'.mm', corpus)


  # Return:            (1),           (2),       (3),      (4),            (5),    (6)
    return doc_vectors, doc_model, docLabels, doc_info, frequency_dict, corpus


"""


"""
def load_doc_model(group):

    with open('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_docs.txt', 'r') as names:
        doc_names = names.read().split('%')

    with open('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_docinfo.txt', 'r') as doc_text:
        doc_info = json.loads(doc_text.read())

    doc_names = doc_names[:len(doc_names)-1]
    
    doc_vectors = gensim.models.keyedvectors.KeyedVectors.load('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_vectors')
    doc_model = gensim.models.doc2vec.Doc2Vec.load('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'_model')
    frequency_dict = gensim.corpora.Dictionary.load('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'.dict')
    corpus = gensim.corpora.MmCorpus('../users/'+settings.user+'/'+str(group)+'/ModelData/'+str(group)+'.mm')

    #print doc_info

  # Return:        (1),       (2),       (3),      (4),            (5),    (6)
    return doc_vectors, doc_model, doc_names, doc_info, frequency_dict, corpus
    
