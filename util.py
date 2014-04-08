import os
import nltk
import json
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

user_name = os.environ.get('USER')
st = PorterStemmer()
stopwords = stopwords.words('english')


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
            self.labels_file = self.source_dir + '/labels_0219.txt'
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
                resumes.append((open(self.source_dir + '/training_0219/' + filename).read(), resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


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
    xml_directory = '/Users/' + user_name + '/Documents/Data/samples_0219'
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
