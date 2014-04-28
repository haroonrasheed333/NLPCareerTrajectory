__author__ = 'divyakarthikeyan'

from util import stripxml
import os
import re
import time
import csv
import json
import ngram
from ngram import NGram
import nltk
#from iHire import extract_text_from_pdf


punct = re.compile(r'^[^A-Za-z0-9]+|[^a-zA-Z0-9]+$')
is_word=re.compile(r'[a-z]', re.IGNORECASE)
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer=nltk.tokenize.punkt.PunktWordTokenizer()

def get_words(sentence):
    return [punct.sub('',word) for word in word_tokenizer.tokenize(sentence) if is_word.search(word)]

def ngrams(text, n):
    for sentence in sentence_tokenizer.tokenize(text.lower()):
        words = get_words(sentence)
        for i in range(len(words)-(n-1)):
            yield(' '.join(words[i:i+n]))

def extract_univ(data):
    data = stripxml(str(data))
    data = data.lower()
    data=data.replace('\xc2\xa0', ' ')
    print data
    data = re.sub ('[^A-Za-z0-9 ]+',' ',str(data))
    data = re.sub ('  ',' ',str(data))
    if 'education' in data:
        parted = data.split('education')[1]
        second = parted[:150]
    else:
        second = data
    univ_dict = json.loads(open("static/univs_list.json","rb").read())
    n=10
    while (n>1):
        for ngram in ngrams(str(second).lower(), n):
            if ngram.lower() in univ_dict:
                return ngram.title()
        n = n - 1

    #with open("static/UniqueFBUnivNames.csv", 'rb') as f:
    #    reader = csv.reader(f)
    #    for row in reader:
    #        row = re.sub('[^A-Za-z0-9 ]+', ' ', str(row))
    #        row = re.sub('  ', ' ', str(row))
    #        if str(row).lower() in second:
    #            if len(str(row).split())>1:
    #                return str(row)
    #                break
    return ""

def extract_univ_json(data):
    univ_dict = json.loads(open("static/univs_list.json","rb").read())
    n=10
    while (n>1):
        for ngram in ngrams(str(data).lower(), n):
            print ngram
        n = n - 1
    #print "curry college" in univ_dict

def extract_from_resume(data):
    out = {}
    data = stripxml(str(data))
    data = data.lower()
    data = re.sub ('[^A-Za-z0-9 ]+',' ',str(data))
    data = re.sub ('  ',' ',str(data))
    if 'education' in data:
        parted = data.split('education')[1]
        second = parted[:150]
        out['split2'] = second
    else:
        second = data
    with open("static/UniqueFBUnivNames.csv", 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            row = re.sub('[^A-Za-z0-9 ]+', ' ', str(row))
            row = re.sub('  ', ' ', str(row))
            if str(row).lower() in second:
                if len(str(row).split())>1:
                    out['univ'] = str(row)
                    return out
                    break
    return out

def ngram_similarity(univ_name):
    out = {}
    with open("static/UniqueFBUnivNames.csv", 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            row = re.sub('[^A-Za-z0-9 ]+', ' ', str(row))
            row = re.sub('  ', ' ', str(row))
            out['score'] = NGram.compare(str(row).lower(), univ_name, N=1)
            if NGram.compare(str(row).lower(), str(univ_name).lower()) > 0.5:
                out['score_used'] = NGram.compare(str(row).lower(), univ_name)
                out['univ'] = str(row)
                return out
    return out

def generate_ngrams(res):
    tokens = str(res).split()
    out = {}
    result = []
    for n in range(2,6):
        out[n] = zip(*[tokens[i:] for i in range(n)])

    return out

if __name__ == '__main__':
    #extract_univ("Berekeley")
    #data = open('/Users/divyakarthikeyan/Downloads/39-bc5e01a4f80acbcc3b0f1a92c1c7cd1a_CPhamDesignResume.pdf').
    data = extract_text_from_pdf('/Users/divyakarthikeyan/Downloads/39-bc5e01a4f80acbcc3b0f1a92c1c7cd1a_CPhamDesignResume.pdf')
    print data
    print "---"
    print extract_univ(data)
