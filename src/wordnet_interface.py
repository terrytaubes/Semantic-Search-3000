# coding: utf-8

"""
WordNet Interface
"""

from nltk.corpus import wordnet


def wordnet_syns(word):

    syns = wordnet.synsets(word)
    
    feature_list = []
    features = []

    first = True

    for syn in syns:
            
        if syn.lemmas()[0].name() == word:
            feature_list.extend(syn.hypernyms())
            feature_list.extend(syn.hyponyms())
        feature_list.append(syn)

    features = [feat.lemmas()[0].name().lower() for feat in feature_list]
    features.append(word.lower())

    features = [x for x in set(features)]
    
    #print features

    return features

def main():
    wordnet_syns("quick")
    #find_similar("quick")

if __name__ == "__main__":
    main()
