# coding: utf-8

"""
Merriam-Webster API
"""

from urllib2 import urlopen
import xmltodict, json
import re

def find_similar(word):

    url = "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"
    url += word
    url += "?key=5d067142-afb1-4a69-bf52-0c6f15f5023f"

    #print url

    response = urlopen(url)
    word_xml = response.read()
    response.close()

    word_json = json.loads(json.dumps(xmltodict.parse(word_xml)))
    #print word_json


    ## function returns Synonym list and Related list
    syn_list = []

    #print word_json['entry_list']


    ## Parse JSON for Synonyms and Relevant words
    for entry in word_json['entry_list']:
        for i in range(len(word_json['entry_list'][entry])):
            #print word_json['entry_list'][entry][i], '\n'
            try:            
                if type(word_json['entry_list'][entry][i]) == dict:
                    for key in word_json['entry_list'][entry][i].keys():
                        #print "Key1:", key, word_json['entry_list'][entry][i][key]

                        if key == "sens":
                            for j in range(len(word_json['entry_list'][entry][i][key])):
                                #print word_json['entry_list'][entry][i][key][j], '\n'
                                try:
                                    for key2 in word_json['entry_list'][entry][i][key][j].keys():
                                        #print "key2:", key2, word_json['entry_list'][entry][i][key][j][key2]

                                        if key2 == 'syn':
                                            #print word_json['entry_list'][entry][i][key][j][key2], '\n'
                                            if type(word_json['entry_list'][entry][i][key][j][key2]) == dict:
                                                syn_str = word_json['entry_list'][entry][i][key][j][key2]['#text']
                                                syn_str = re.sub(r'\]|\[|\s', r'', syn_str)
                                                syn_str = re.sub(r';', r' ', syn_str)
                                                syns = re.sub(r'\(.*\)', r'', syn_str).split(',')
                                                syn_list.extend(syns)
                                                #print 'syns:', syns, '\n'
                                            else:    
                                                syn_str = word_json['entry_list'][entry][i][key][j][key2]
                                                syn_str = re.sub(r'\]|\[|\s', r'', syn_str)
                                                syn_str = re.sub(r';', r' ', syn_str)
                                                syns = re.sub(r'\(.*\)', r'', syn_str).split(',')
                                                syn_list.extend(syns)
                                                #print 'syns:', syns, '\n'

                                        else:
                                            continue
                                except AttributeError:
                                    continue;
                        else:
                            continue
                else:
                    continue
            except KeyError:
                continue
            
    #print syn_list
    return syn_list
    

def main():

    syn_list = find_similar("happy")
    print syn_list


if __name__ == "__main__":
    main()
