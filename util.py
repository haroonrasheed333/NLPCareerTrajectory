import os
import re
import csv
import sys
import nltk
import json
import string
import operator
from lxml import etree
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from JobTitleNormalization import normalize_job_titles

nltk.data.path.append('nltk_data')
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
            self.labels_file = self.source_dir + '/labels_0426.txt'
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
                resumes.append((open(self.source_dir + '/training_0426/' + filename).read(), resume_tag, filename))
            except IOError, (ErrorNumber, ErrorMessage):
                if ErrorNumber == 2:
                    pass

        return resumes


def read_skills_from_json_file(training_data):
    """
    This function will read from the skills json file, extract the skills that are part of the training data and create
    a dictionary with Job Titles as keys and list of all the skills for that Job Title as values

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    Returns:
        skills_dict -- A dictionary with Job Titles as keys and list of all the skills for that Job Title as values
    """

    skills_dict = dict()
    temp_dict = json.loads(open("skills_0418.json").read())
    training_files = [fname for (resume, resume_label, fname) in training_data]

    for title in temp_dict:
        for file_name in temp_dict[title]:
            if file_name.keys()[0] in training_files:
                value = skills_dict.get(title.lower(), None)
                if value is not None:
                    skills_dict[title.lower()] = value + file_name[file_name.keys()[0]]
                else:
                    skills_dict[title.lower()] = []
                    skills_dict[title.lower()] = file_name[file_name.keys()[0]]

    return skills_dict


def extract_top_skills(training_data):
    """
    Extract Top Skills for each Job Title from the training dataset.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    Returns:
        A consolidated list of top skills for all the Job Titles

    """
    skills_dict = read_skills_from_json_file(training_data)

    # Read the top n skills for each Job TiTle
    skill_features = []
    for skill in skills_dict:
        skill_list = skills_dict[skill]
        skill_count = Counter(skill_list)
        top_job_skills = sorted(skill_count, key=skill_count.get, reverse=True)[:50]
        skill_features += top_job_skills

    top_job_skills = list(set(skill_features))
    return top_job_skills


def xml_features(data):
    """
    Extract details from selected xml tags
    Strip the xml tags from the xml to make it plaintext

    Args:
        data -- Resume xml

    Returns:
        xml_features -- dictionary with plaintext resume without any xml tags and select xml features
    """
    xml_features = {}
    jobs = data.xpath('//job/title/text()')
    job_normalized = []
    for title in jobs:
        job_normalized.append(normalize_job_titles(title))
    xml_features["jobs"] = jobs
    employers = data.xpath('//job/employer/text()')
    institution = data.xpath('//education/school/institution/text()')
    degree = data.xpath('//education/school/degree/text()')
    xml_features["employers"] = employers
    xml_features["institution"] = institution
    xml_features["degree"] = degree
    pattern = re.compile(r'<.*?>')
    data = etree.tostring(data, pretty_print=True)
    text = pattern.sub('', data)
    xml_features["raw_resume"] = text
    return xml_features


def miscellaneous_features(resume_text):
    """
    Function to create miscellaneous features

    Args:
        resume_text -- content of resume as string

    Returns:
        mis_features -- list of miscellaneous features
    """

    resume_text = re.sub('[^A-Za-z\' ]+', '', str(resume_text))
    tokens = nltk.word_tokenize(resume_text.lower())
    mis_features =dict()
    mis_features["length"] = len(tokens)
    sum = 0
    adj_count = 0
    noun_count = 0
    pos_tagged_text = nltk.pos_tag(tokens)
    for t in pos_tagged_text:
        sum = sum + len(t[0])
        if t[1] == "NN":
            noun_count += 1
        if t[1] == "JJ":
            adj_count += 1

    mis_features["avg_word_length"] = sum/ len(tokens)
    mis_features["adj_count"] = adj_count
    mis_features["noun_count"] = noun_count
    return mis_features


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


def feature_consolidation(resumes, top_unigram_list, top_bigram_list,  add_true_score=False):
    """
    Function to consolidate all the featuresets for the training data

    Args:
        resumes -- list of tuples [(resume_text, tag, filename), (resume_text, tag, filename)...]
        top_unigram_list -- list of top unigrams from the training dataset
        top_bigram_list -- list of top bigrams from the training dataset
        add_true_score -- boolean (default: False)

    Returns:
        consolidated_features -- list of consolidated features
    """
    uni_feats = []
    bi_feats = []
    xml_feats = []
    mis_feats = []
    pattern = re.compile(r'<.*?>')
    for (dataxml, label, fname) in resumes:
        data = etree.tostring(dataxml, pretty_print=True)
        resume_text = str(pattern.sub('', data))
        uni_feats.append(unigram_features(resume_text, top_unigram_list))
        bi_feats.append(bigram_features(resume_text, top_bigram_list))
        xml_feats.append(xml_features(dataxml))
        mis_feats.append(miscellaneous_features(resume_text))
    consolidated_features = []
    ind = 0
    while ind < len(uni_feats):
        consolidated_features.append((uni_feats[ind], bi_feats[ind] , xml_feats[ind], mis_feats[ind]))
        ind += 1
    return consolidated_features

    
def create_skills_json(data, xml_directory, save_json=False):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """

    skills_dict = dict()

    # Get the skills for each resume from its corresponding xml file.
    for (resume_text, tag_name, filename) in data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//skills/text()')

        skills_ignore = open('skills_exclude_list').read().splitlines()

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
                    and w not in stopwords and string.capwords(w) not in skills_ignore
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

    if save_json:
        j = json.dumps(skills_dict, indent=4, separators=(',', ': '))
        f = open('skills_0426.json', 'w')
        print >> f, j
        f.close()
    else:
        return skills_dict


def create_skills_json_no_stemming(data, xml_directory, save_json=False):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """

    skills_dict = dict()

    # Get the skills for each resume from its corresponding xml file.
    for (resume_text, tag_name, filename) in data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//skills/text()')

        skills_ignore = open('skills_exclude_list').read().splitlines()

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
                    w for (w, t) in nltk.pos_tag(skill_words) if t.startswith('NN')
                    and w not in stopwords and string.capwords(w) not in skills_ignore
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

    if save_json:
        j = json.dumps(skills_dict, indent=4, separators=(',', ': '))
        f = open('skills_0418_no_stemming.json', 'w')
        print >> f, j
        f.close()
    else:
        return skills_dict


def create_skills_json_no_stemming_full_ds():
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """

    user_name = os.environ.get('USER')
    xml_directory = '/Users/' + user_name + '/Documents/Data/samples_0418'

    skills_dict = dict()

    skills_ignore = open('skills_exclude_list').read().splitlines()

    for root, dirs, files in os.walk(xml_directory, topdown=False):
        for f in files:
            try:
                xml = etree.parse(xml_directory + '/' + f)
                skill_list = xml.xpath('//skills/text()')
            except:
                continue

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
                        w for (w, t) in nltk.pos_tag(skill_words) if t.startswith('NN')
                        and w not in stopwords and string.capwords(w) not in skills_ignore
                    ]

                    slist += skill_words_nouns

                skills_dict[f] = []
                skills_dict[f] = list(set(slist))

        j = json.dumps(skills_dict, indent=4, separators=(',', ': '))
        f = open('skills_0424_no_stemming_full_ds.json', 'w')
        print >> f, j
        f.close()


def stripxml(data):
    """
    Strip the xml tags from the xml to make it plaintext

    Args:
        data -- Resume xml

    Returns:
        text -- plaintext resume without any xml tags.
    """
    pattern = re.compile(r'<.*?>')
    text = pattern.sub('', data)
    return text


def create_skills_map(data, xml_directory):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """
    skills_map = dict()

    # Get the skills for each resume from its corresponding xml file.
    for (resume_text, tag_name, filename) in data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//skills/text()')

        skills_ignore = \
            [
                'Skills', 'Years', 'Languages', 'Proficient', 'Tools', 'Expert', 'System', 'Business', 'Systems', 'Ms',
                'Computer', 'Software', 'Suite', 'Development', 'Human', 'Month', 'Level', 'Studio', 'Applications',
                'Application', 'Proficiency', 'Certifications', 'Applications', 'Implementation', 'Architecture',
                'Experience', 'Services', 'Administration', 'Provider', 'Functions', 'Concur', 'Knowledge'
            ]

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
                    string.capwords(w) for (w, t) in nltk.pos_tag(skill_words) if t.startswith('NN')
                    and w not in stopwords and string.capwords(w) not in skills_ignore
                ]

                slist += skill_words_nouns

            value = skills_map.get(tag_name.lower(), None)
            if value is not None:
                skills_map[tag_name.lower()] += slist
            else:
                skills_map[tag_name.lower()] = []
                skills_map[tag_name.lower()] += slist

    for sk in skills_map:
        temp_skills_list = skills_map[sk]
        top_ten_skills = Counter(temp_skills_list).most_common(20)
        skills_map[sk] = []
        for top_ten in top_ten_skills:
            skills_map[sk].append(top_ten[0])

    j = json.dumps(skills_map, indent=4, separators=(',', ': '))
    f = open('skills_map.json', 'w')
    print >> f, j
    f.close()


def create_skills_map_with_percentage(data, xml_directory, save_json):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """
    skills_in_files = dict()

    # Get the skills for each resume from its corresponding xml file.
    for (resume_text, tag_name, filename) in data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//skills/text()')

        current_file_directory = os.path.dirname(os.path.realpath(__file__))

        skills_ignore = open(current_file_directory + '/skills_exclude_list').read().splitlines()

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
                    string.capwords(w) for (w, t) in nltk.pos_tag(skill_words) if t.startswith('NN')
                    and w not in stopwords and string.capwords(w) not in skills_ignore
                ]

                slist += skill_words_nouns

            value = skills_in_files.get(tag_name.lower(), None)
            if value is not None:
                skills_in_files[tag_name.lower()].append(list(set(slist)))
            else:
                skills_in_files[tag_name.lower()] = []
                skills_in_files[tag_name.lower()].append(list(set(slist)))

    skills_map_with_percent = dict()
    for sk in skills_in_files:
        total_skills_for_title = list(set(sum(skills_in_files[sk], [])))
        skills_map_with_percent[sk] = dict()
        skills_map_with_percent[sk]['skills'] = []
        skills_map_with_percent[sk]['percent'] = []
        files_count = len(skills_in_files[sk])
        temp_skill_percent_map = dict()
        for skill in total_skills_for_title:
            skill_count = 0
            for file_skills in skills_in_files[sk]:
                if skill in file_skills:
                    skill_count += 1
            skill_percent = int(skill_count * 100 / files_count)
            temp_skill_percent_map[skill] = skill_percent

        sorted_percents = sorted(temp_skill_percent_map.iteritems(), key=operator.itemgetter(1), reverse=True)
        for sp in sorted_percents:
            skills_map_with_percent[sk]['skills'].append(sp[0])
            skills_map_with_percent[sk]['percent'].append(sp[1])

    if save_json:
        j = json.dumps(skills_map_with_percent, indent=4, separators=(',', ': '))
        f = open('skills_map_with_percent.json', 'w')
        print >> f, j
        f.close()
    else:
        return skills_map_with_percent


def extract_features_for_network_map(xml_directory, save_csv):

    if not os.path.exists(xml_directory):
        return {}

    school_job_details = []
    for root, dirs, files in os.walk(xml_directory, topdown=False):
        for f in files:
            if os.path.isfile(xml_directory + '/' + f):
                xml = etree.parse(xml_directory + '/' + f)
                education = xml.xpath('//education')[0]
                schools = education.xpath('//school')
                school_details = []
                resume_id = f.split('.')[0]
                for school in schools:
                    try:
                        school_id = school.attrib['id']
                    except ValueError:
                        school_id = ''

                    institution = school.xpath('institution/text()')[0]

                    try:
                        degree_level = school.xpath('degree/@level')[0]
                    except IndexError:
                        degree_level = ''

                    degree = school.xpath('degree/text()')[0]

                    major_code = school.xpath('major/@code')[0]
                    major = school.xpath('major/text()')[0]
                    school_details.append((school_id, institution, degree_level, degree, major_code, major))

                job_details = []
                try:
                    experience = xml.xpath('//experience')[0]
                    jobs = experience.xpath('//job')
                    for job in jobs:
                        employer = job.xpath('employer/text()')[0]

                        try:
                            job_location = job.xpath('address/city/text()')[0]
                            job_state = job.xpath('address/state/text()')[0]
                        except IndexError:
                            job_location = ''
                            job_state = ''

                        title = job.xpath('title/text()')[0]
                        job_details.append((employer, job_location, job_state, title))
                except IndexError:
                    job_details.append(('', '', '', ''))

                for school_detail in school_details:
                    for job_detail in job_details:
                        school_job_details.append(
                            (
                                resume_id,
                                school_detail[0],
                                school_detail[1],
                                school_detail[2],
                                school_detail[3],
                                school_detail[4],
                                school_detail[5],
                                job_detail[0],
                                job_detail[1],
                                job_detail[2],
                                job_detail[3]
                            )
                        )

            else:
                school_job_details.append(['', '', '', '', '', '', '', '', '', ''])

    if save_csv:
        with open("institution_degree_job_map.csv", "wb") as csv_file:
            writer = csv.writer(csv_file)
            for school_job_detail in school_job_details:
                try:
                    writer.writerow(school_job_detail)
                except:
                    pass
    else:
        school_job_details_dict = dict()
        for sjd in school_job_details:
            value = school_job_details_dict.get(sjd[0], None)
            if value:
                school_job_details_dict[sjd[0]].append(sjd)
            else:
                school_job_details_dict[sjd[0]] = []
                school_job_details_dict[sjd[0]].append(sjd)
        return school_job_details_dict


def create_skills_map_with_percentage_new(data, xml_directory, save_json):
    """
    This function will extract all the skills from the training corpus and create a dictionary with Job Titles as
    keys and list of dictionaries containing the skills for each resume as values. The dictionary is converted and
    stored as a json file.

    Args:
        training_data -- list of tuples. Eg. [(resume, tag, filename), (resume, tag, filename)...]

    """
    skills_in_files = dict()

    # Get the skills for each resume from its corresponding xml file.
    for (resume_text, tag_name, filename) in data:
        xml_file = filename.split('_')[0] + '.txt'
        xml = etree.parse(xml_directory + '/' + xml_file)
        skill_list = xml.xpath('//variant/text()')

        if skill_list:
            skill_list = [string.capwords(s) for s in skill_list]
            value = skills_in_files.get(tag_name.lower(), None)
            if value is not None:
                skills_in_files[tag_name.lower()].append(list(set(skill_list)))
            else:
                skills_in_files[tag_name.lower()] = []
                skills_in_files[tag_name.lower()].append(list(set(skill_list)))

    skills_map_with_percent = dict()
    for sk in skills_in_files:
        total_skills_for_title = list(set(sum(skills_in_files[sk], [])))
        skills_map_with_percent[sk] = dict()
        skills_map_with_percent[sk]['skills'] = []
        skills_map_with_percent[sk]['percent'] = []
        files_count = len(skills_in_files[sk])
        temp_skill_percent_map = dict()
        for skill in total_skills_for_title:
            skill_count = 0
            for file_skills in skills_in_files[sk]:
                if skill in file_skills:
                    skill_count += 1
            skill_percent = int(skill_count * 100 / files_count)
            temp_skill_percent_map[skill] = skill_percent

        sorted_percents = sorted(temp_skill_percent_map.iteritems(), key=operator.itemgetter(1), reverse=True)
        for sp in sorted_percents:
            skills_map_with_percent[sk]['skills'].append(sp[0])
            skills_map_with_percent[sk]['percent'].append(sp[1])

        skills_map_with_percent[sk]['skills'] = skills_map_with_percent[sk]['skills'][:50]
        skills_map_with_percent[sk]['percent'] = skills_map_with_percent[sk]['percent'][:50]

    if save_json:
        j = json.dumps(skills_map_with_percent, indent=4, separators=(',', ': '))
        f = open('skills_map_with_percent_new_0429.json', 'w')
        print >> f, j
        f.close()
    else:
        return skills_map_with_percent



if __name__ == '__main__':
    user_name = os.environ.get('USER')
    traintest_corpus = ResumeCorpus('/Users/' + user_name + '/Documents/Data')
    xml_directory = '/Users/' + user_name + '/Documents/Data/samples_0426'
    # create_skills_json_no_stemming(traintest_corpus.resumes, xml_directory, True)
    # create_skills_json(traintest_corpus.resumes, xml_directory, True)
    # create_skills_map(traintest_corpus.resumes, xml_directory)
    # create_skills_map_with_percentage(traintest_corpus.resumes, xml_directory, True)
    create_skills_map_with_percentage_new(traintest_corpus.resumes, xml_directory, True)
    # create_skills_json_no_stemming_full_ds()