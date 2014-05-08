import re
import nltk
import string
from nltk.tag import pos_tag
from itertools import permutations
from nltk.stem.porter import PorterStemmer

nltk.data.path.append('nltk_data')

expand = [
    ('asst.', 'assistant '),
    ('asst', 'assistant'),
    ('admin', 'administrator'),
    ('admin.', 'administrator '),
    ('sr.', 'senior '),
    ('sr', 'senior'),
    ('jr.', 'junior '),
    ('jr', 'junior'),
    ('rep', 'representative'),
    ('mgr.', 'manager '),
    ('mngr.', 'manager '),
    ('mgr', 'manager'),
    ('mngr', 'manager'),
    ('ceo', 'chief executive officer'),
    ('coo', 'chief operating officer'),
    ('cto', 'chief technology officer'),
    ('cfo', 'chief finance officer'),
    ('vp', 'vice president'),
    ('hr', 'human resources'),
    ('principle', 'principal'),
    ('qa', 'quality assurance'),
    ('it', 'information technology'),
    ('csr', 'customer service representative'),
    ('sw', 'software'),
    ('tech', 'technical'),
    ('software developer', 'software engineer'),
]


def expand_job_title(actual_title):
    title = actual_title
    for match in expand:
        title = re.sub(r'\b' + match[0] + r'\b', match[1], title.lower().replace('.', ''))
        title = title.replace('/', ' ')
        title = title.replace('& ', '')
        title = title.replace('  ', ' ')

    return title.lower()


def title_permutations(title_expanded):
    title_tagged = pos_tag(title_expanded.split())
    st = PorterStemmer()
    title_pos = [st.stem(word) for word, pos in title_tagged if pos != 'IN']

    title_perms = list(map("*".join, permutations(title_pos)))
    return title_perms


def normalize_job_titles(original_titles):
    normalized_titles = []
    titles_dict = {}

    for original_title in original_titles:

        temp_title = original_title.splitlines()[0].rstrip()
        if temp_title.find('\\') > -1:
            temp_title = temp_title.split('\\')[1]
        if temp_title.find('/') > -1:
            temp_title = temp_title.split('/')[1]
        if temp_title.find('|') > -1:
            temp_title = temp_title.split('|')[1]
        if temp_title.find('&') > -1:
            temp_title = temp_title.split('&')[1]
        if temp_title.find(',') > -1:
            temp_title = temp_title.split(',')[1]

        ui_ux_design = ['ui/ux design', 'ui design', 'ux design', 'user interface design', 'user experience design']
        ui_ux_develop = ['ui/ux develop', 'ui develop', 'ux develop', 'user interface develop', 'user experience develop']

        flag = False
        for des in ui_ux_design:
            if des in original_title.lower():
                normalized_titles.append("ui/ux designer")
                flag = True
                break
        if flag:
            continue

        for dev in ui_ux_develop:
            if dev in original_title.lower():
                normalized_titles.append("ui/ux developer")
                flag = True
                break
        if flag:
            continue

        title_expand = expand_job_title(temp_title)
        title_perms = title_permutations(title_expand)

        flag = 0
        for tp in title_perms:
            if tp in titles_dict:
                title = tp
                flag = 1
                break

        if flag == 0:
            title = title_perms[0]
            titles_dict[title] = title_expand

        normalized_titles.append(titles_dict[title])

    return normalized_titles



if __name__ == '__main__':
    # job_titles_file = 'JobTitles.txt'
    # f = open(job_titles_file)
    # original_titles = f.readlines()
    # normalized_titles = normalize_job_titles(original_titles)
    #
    # print len(original_titles)
    # print len(normalized_titles)
    # print len(set(original_titles))
    # print len(set(normalized_titles))
    #
    # print '{:<45}'.format("Actual Title"), '{:<45}'.format("Normalized Title")
    # print "-------------------------------------------------------------------"
    #
    # for i in range(len(normalized_titles)):
    #     print '{:<45}'.format(original_titles[i].rstrip()), '{:<45}'.format(string.capwords(normalized_titles[i]))

    normalized_titles = normalize_job_titles(['user interface developer'])
    print normalized_titles