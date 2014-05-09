import os
import csv
import json
import nltk
from lxml import etree
from nltk.stem.porter import PorterStemmer


st = PorterStemmer()


def extract_features_for_network_map(xml_directory, save_csv=True):
    """
    This function will extract various features like university,
    degree, degree level, major, major code, and employer from
    resume text

    Parameters:
    -----------
    xml_directory -- string
        The path where the xml resumes are stored

    save_csv -- boolean (default: True)
        Boolean value to denote if the extracted features should
        be saved in a csv file or returned back as a dictionary

    Returns:
    --------
    school_job_details_dict -- dict
        Dictionary with resume ids as keys and list of extracted
        features as values

    """

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
        with open("extracted_data/institution_degree_job_map.csv", "wb") as csv_file:
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


def get_top_five_predictions(predicted_decision, labels_names=[]):
    """
    Function to find the top predictions and compute scores based
    on the svm classifier decision scores

    Parameters:
    -----------
    predicted_decision -- list
        List of svm prediction decision scores

    Returns:
    --------
    top_five_predictions, normalized_prediction_score -- tuple
        Top five predictions list and normalized scores list as tuple
    """
    if not predicted_decision:
        return [], []

    top_five_predictions = []
    normalized_prediction_score = []
    for i in range(1):
        predicted_dec_dup = predicted_decision[i]
        predicted_dec_dup_sorted = sorted(predicted_dec_dup, reverse=True)
        max_s = max(predicted_dec_dup_sorted)
        min_s = min(predicted_dec_dup_sorted)

        normalized_prediction_score = \
            [
                int(float(val - min_s) * 100 / float(max_s - min_s)) for val in predicted_dec_dup_sorted[:5]
            ]

        if type(predicted_decision[i]) is list:
            predicted_decision_temp = predicted_decision[i]
        else:
            predicted_decision_temp = predicted_decision[i].tolist()

        for j in range(5):
            top_five_predictions.append(
                labels_names[predicted_decision_temp.index(predicted_dec_dup_sorted[j])]
            )

    return top_five_predictions, normalized_prediction_score


def get_degree(resume_text):
    """
    Function to find the degree level from resume text

    Parameters:
    -----------
    resume_text -- string
        The content of candidate resume as string

    Returns:
    --------
    degree_level -- float
        A float value assigned based on the degree level of the
        candidate
    """
    resume_text = resume_text.lower()

    if 'education' in resume_text:
        parted = resume_text.split('education')[1]
        edu_text = parted[:150]
    else:
        edu_text = resume_text
    degree_level = 0

    for d in ["doctor ", "ph.d", "phd", "ph. d"]:
        if d in edu_text:
            return 0.021

    masters = \
        [
            "master", "ms degree", "mpa ", "mhrm", "mfa ", "mba ", "m.sc", "m.s ", "m.h.a", "m.f.a", "m.b.a", "m. s",
            "m.a", "m. tech", "m. ed", "m. a"
        ]

    for m in masters:
        if m in edu_text:
            return 0.018

    bachelors = \
        [
            "bachelor", "bsc", "bsit", "bse", "bsba", "bs of", "bs degree", "bgs", "bfa", "bba", "bs ", "ba ", "b.sc",
            "b.s.n", "b.s.", "b.s. ", "b.phil", "b.f.a", "b.e", "b.com", "b.b.a", "b.a.", "b.tech", "b. tech", "b. a",
            "bs,"
        ]

    for b in bachelors:
        if b in edu_text:
            return 0.016

    associate = ["associate", "as degree", "as ", "aas ", "a.s.", "a.s ", "a.a.s", "a.a. ", "a. a"]

    for a in associate:
        if a in edu_text:
            return 0.014

    if "diploma" in edu_text:
        return 0.013

    high_school = ["high school diploma", "hs dip", "h. s. ", "high school degree", "h.s "]

    for h in high_school:
        if h in edu_text:
            return 0.012

    return degree_level


def get_degree_level_from_resume(resume_data):
    """
    Function to find the degree levels of the each resume in the corpus

    Parameters:
    -----------
    resume_data -- list
        List containing the resume text of all resumes in the corpus

    Returns:
    --------
    degree_level -- list
        A list containing the degree level of each resume in the corpus
    """
    degree_level = [get_degree(resume_text) for (resume_text, tag, fname) in resume_data]
    return degree_level


def extract_all_skills():
    """
    Function to extract all the skills from skills map json to display
    in autocomplete suggestion.
    """
    skill_file = json.loads(open('skills_map_with_percent.json').read())
    skills = []
    for title in skill_file:
        skills += skill_file[title]['skills']

    skills = list(set(skills))

    skills_autocomplete_list = []

    for skill in skills:
        temp_dict = {"value": skill}
        skills_autocomplete_list.append(temp_dict)

    j = json.dumps(skills_autocomplete_list, indent=2)
    f = open('extracted_data/skills_autocomplete_list.txt', 'w')
    print >> f, j
    f.close()

    return


def get_skill_features(resume_text, top_skills):
    """
    Function to generate skill based features

    Parameters:
    -----------
    resume_text -- string
        The content of resume as string

    top_skills - list
        List of top skills

    Returns:
    --------
    skill_features -- list
        A list representing the presence or absence of each top skill
        in the resume text
    """
    skill_features = []
    tokens = nltk.word_tokenize(resume_text.lower())
    tokens = [st.stem(token) for token in tokens]

    for skill in top_skills:
        if skill in tokens:
            skill_features.append(1)
        else:
            skill_features.append(0)

    return skill_features


def get_skill_features_from_resume(resume_data, top_skills):
    """
    Function to generate skill based features

    Parameters:
    -----------
    resume_data -- list
        List containing the resume text of all resumes in the corpus

    top_skills - list
        List of top skills

    Returns:
    --------
    skill_list -- list
        A list containing skill feature list for each resume
    """
    skill_list = [get_skill_features(resume_text, top_skills) for (resume_text, tag, fname) in resume_data ]
    return skill_list


if __name__ == '__main__':
    extract_all_skills()