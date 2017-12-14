# coding: utf-8

"""
Wikipedia API for text extraction
"""

import wikipedia
import re

#import settings


def find_similar(word):

    syns = []

    try:
        search = wikipedia.search(word)

        stoplist = set('for a of the and to in'.split())


        for feat in search:
            syns.extend([x.lower() for x in re.sub(r'\)|\(', '', feat).split() if x not in stoplist])

        syns = list(set(syns))

        if word.lower() in syns:
            syns.remove(word.lower())
    except:
        pass

    #print syns

    return syns


def download_wiki_topic(topic, docs):

    #print wikipedia.summary(word)
    #print wikipedia.search(word)
    links = wikipedia.page(topic).links
    print len(wikipedia.page(topic).links)

    user = 'terrytaubes'
    group = 'cs_ml_nlp'


    for i in range(200):

        try:
            wiki = wikipedia.page(links[i]).content
        
            with open('../users/'+user+'/'+group+'/Text/'+links[i]+'.txt', 'w') as f:
                f.write(wiki.encode('utf8'))
        except:
            continue

    


        


def main():

    while (True):
        
        string = raw_input("Enter Wikipedia Topic: ")

        #string = string[0].upper() + string[1:]
        #print string

        
        find_similar(string)
            

if __name__ == "__main__":
    main()
