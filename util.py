import os
import nltk
import json
import re
from lxml import etree
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

user_name = os.environ.get('USER')
st = PorterStemmer()
stopwords = stopwords.words('english')
nltk.data.path.append('nltk_data')


class ResumeCorpus():
    """
    Class to read the source files from source directory and create a list of tuples with resume_text, tag and filename
    for each resume.

    Args:
        source_dir -- string. The path of the source directory.
        labels_file -- string. The path of the labels file (default: None)
    """
    def __init__(self, source_dir, labels_file=None):
        
        self.source_dir = source_dir
        if not labels_file:
            self.labels_file = self.source_dir + '/labels_0408.txt'
        else:
            self.labels_file = labels_file
        self.resumes = self.read_files()
        
    def read_files(self):
        """
        Method to return a list of tuples with resume_text, tag and filename for the training data

        Args:
            No Argument

        Returns:
            resumes -- list of tuples with resume_text, tag and filename for the training data
        """
        resumes = []

        for line in open(self.labels_file).readlines():
            try:
                filename_tag = line.split('\t')
                filename = filename_tag[0]
                resume_tag = filename_tag[1].rstrip()
                resumes.append((open(self.source_dir + '/training_0408/' + filename).read(), resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


def unigram_features(resume_text, top_unigram_list):
    """
    Function to create unigram features from the resume text

    Args:
        resume_text -- content of resume as string
        top_unigram_list -- list of top unigrams

    Returns:
        uni_features -- list of unigram features
    """
    resume_text = re.sub('[^A-Za-z\' ]+', '', str(resume_text))
    tokens = nltk.word_tokenize(resume_text.lower())
    tokens = [st.stem(token) for token in tokens]
    # c = Counter(tokens)
    uni_features = []
    for top_uni in top_unigram_list:
        try:
            uni_stem = str(st.stem(top_uni))
            if uni_stem in tokens:
                # uni_features.append(c[uni_stem])
                uni_features.append(1)
                # avg_word_len += len(token_stem)
                # count += 1
            else:
                uni_features.append(0)
        except UnicodeEncodeError:
            pass
    # uni_features['average_word_length'] = avg_word_len/(count+1)
    # uni_features['docu_length'] = len(tokens)
    return uni_features


def bigram_features(resume_text, top_bigram_list):
    """
    Function to create bigram features from the resume text

    Args:
        resume_text -- content of resume as string
        top_bigram_list -- list of top bigrams

    Returns:
        bi_features -- list of bigram features
    """
    tokens = [st.stem(word) for word in resume_text.lower().split() if word not in stopwords]
    bigrs = bigrams(tokens)
    bigram_list = []
    bigram_list += [(bigrm[0], bigrm[1]) for bigrm in bigrs if (bigrm[0] not in stopwords and bigrm[1] not in stopwords)]
    # c = Counter(bigrams_list)
    bi_features = []
    for top_bi in top_bigram_list:
        if top_bi in bigram_list:
            # bi_features.append(c[top_bi])
            bi_features.append(1)
        else:
            bi_features.append(0)
    return bi_features

    
def create_skills_json(data):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """

    skills_dict = dict()

    # Get the skills for each resume from its corresponding xml file.
    xml_directory = '/Users/' + user_name + '/Documents/Data/samples_0408'
    for (resume_text, tag_name, filename) in data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//skills/text()')

        if skill_list:
            slist = []
            for skill in skill_list:
                try:
                    skill = str(skill).encode('utf-8')
                except:
                    skill = skill.encode('utf-8')
                skill = skill.translate(None, ',:();-')
                skill = skill.replace('/', ' ')
                skill = skill.replace('.', '')
                skill_words = nltk.word_tokenize(skill.lower())

                skill_words_nouns = [
                    st.stem(w) for (w, t) in nltk.pos_tag(skill_words) if t.startswith('NN')
                    and w not in stopwords
                ]

                skill_words_nouns = list(set(skill_words_nouns))
                slist += skill_words_nouns

            temp_dict = dict()
            temp_dict[filename] = slist

            value = skills_dict.get(tag_name.lower(), None)
            if value is not None:
                skills_dict[tag_name.lower()].append(temp_dict)
            else:
                skills_dict[tag_name.lower()] = []
                skills_dict[tag_name.lower()].append(temp_dict)

    j = json.dumps(skills_dict, indent=4)
    f = open('skills.json', 'w')
    print >> f, j
    f.close()

if __name__ == '__main__':
    user_name = os.environ.get('USER')
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')
    create_skills_json(traintest_corpus.resumes)
