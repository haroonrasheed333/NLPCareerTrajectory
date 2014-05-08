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
is_word = re.compile(r'[a-z]', re.IGNORECASE)
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()


def get_words(sentence):
    return [punct.sub('',word) for word in word_tokenizer.tokenize(sentence) if is_word.search(word)]


def ngrams(text, n):
    for sentence in sentence_tokenizer.tokenize(text.lower()):
        words = get_words(sentence)
        for i in range(len(words)-(n-1)):
            yield(' '.join(words[i:i+n]))


def extract_univ(data,univ_dict,univ_normalize):
    try:
        data = stripxml(str(data))

        data = data.lower()
        data = data.replace('\xc2\xa0', ' ')
        #print data
        data = re.sub ('[^A-Za-z0-9 ]+',' ',str(data))
        data = re.sub ('  ',' ',str(data))

        if 'education' in data:
            parted = data.split('education')[1]
            second = parted[:150]
        else:
            second = data
        n = 10
        while n > 1:
            for ngram in ngrams(str(second).lower(), n):
                if ngram.lower() in univ_normalize:
                    return univ_normalize[str(ngram.lower())]
                elif ngram.lower() in univ_dict:
                    return ngram.title()
            n -= 1
        return ""
    except UnicodeEncodeError:
        return data
    except UnicodeDecodeError:
        return data


def create_data_for_graph(univ, major, skills_employer, univ_major_map, major_code):
    print "Inside create data"
    univ = str(univ).lower()
    result = {}
    result["links"] = []
    print univ
    if univ in univ_major_map:
        indices = []
        if (major):
            print major_code[major]
            if major in major_code:
                if major_code[major] in univ_major_map[univ]:
                    indices.append(univ_major_map[univ][major_code[major]])
        else:
            for key in univ_major_map[univ]:
                indices.append(univ_major_map[univ][key])
        print indices
        for index in indices:
            if str(index) in skills_employer:
                if "links" in skills_employer[str(index)]:
                    for d in skills_employer[str(index)]["links"]:
                        result["links"].append(d)

    j = json.dumps(result, indent=4, separators=(',', ': '))
    if os.path.isfile("static/miserables.json"):
        os.remove("static/miserables.json")
    f = open("static/miserables.json", "w")
    print >> f, j
    f.close()
    return


def create_data_for_tree(univ, major, skills_employer_tree, univ_major_map, major_code, employer_second_degree_tree):
    if os.path.isfile("static/treegraph.json"):
        os.remove("static/treegraph.json")

    univ = str(univ).lower()

    result = {}
    result["name"] = "Me"
    result["children"] = []
    if univ in univ_major_map:
        indices = []
        if major:
            print major_code[major]
            if major in major_code:
                if major_code[major] in univ_major_map[univ]:
                    indices.append(univ_major_map[univ][major_code[major]])
        else:
            for key in univ_major_map[univ]:
                if len(indices) < 8:
                    indices.append(univ_major_map[univ][key])
        temp = {}

        for index in indices:
            if str(index) in skills_employer_tree:
                for i in range(0, len(skills_employer_tree[str(index)]["children"])):
                    if skills_employer_tree[str(index)]["children"][i]["name"] in temp:
                        pass
                    else:
                        temp [skills_employer_tree[str(index)]["children"][i]["name"]] = 1
        i = 0

        for key in temp:
            new = []
            if key.lower() in employer_second_degree_tree:
                for x in employer_second_degree_tree[key.lower()]:
                    if x not in temp:
                        if len(new) < 51:
                            new.append({"name": x.strip('\t').strip('\n').strip() , "children": []})
                result["children"].append({"name" : key.title(), "children" : new })
            i += 1

    j = json.dumps(result, indent=4, separators=(',', ': '))
    f = open("static/treegraph.json", "w")
    print >> f, j
    f.close()
    return


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


def create_data(univ, skills_employer, univ_major_map):
    univ = str(univ).lower()
    result = {}
    result["links"] = []
    if univ in univ_major_map:
        indices = []
        for key in univ_major_map[univ]:
            indices.append(univ_major_map[univ][key])
        for index in indices:
            if str(index)in skills_employer:
                for d in skills_employer[str(index)]["links"]:
                    result["links"].append(d)
    return result

if __name__ == '__main__':
    pass
    #extract_univ("Berekeley")
    #data = open('/Users/divyakarthikeyan/Downloads/39-bc5e01a4f80acbcc3b0f1a92c1c7cd1a_CPhamDesignResume.pdf').
    # data = extract_text_from_pdf('/Users/divyakarthikeyan/Downloads/39-bc5e01a4f80acbcc3b0f1a92c1c7cd1a_CPhamDesignResume.pdf')
    # print data
    # print "---"
    # print extract_univ(data)