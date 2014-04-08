import re
import string
from nltk.tag import pos_tag
from itertools import permutations
from nltk.stem.porter import PorterStemmer

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
    title_pos = [st.stem(word) for word,pos in title_tagged if pos != 'IN']

    title_perms = list(map("*".join, permutations(title_pos)))
    return title_perms


def main():
    f = open('JobTitles.txt')

    titles = []
    titles_original = []
    titles_dict = {}
    for line in f:
        temp_title = line.rstrip()
        if temp_title.find('\\') > -1:
            temp_title = temp_title.split('\\')[1]
        if temp_title.find('/') > -1:
            temp_title = temp_title.split('/')[1]
        if temp_title.find('&') > -1:
            temp_title = temp_title.split('&')[1]

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

        titles.append(titles_dict[title])

        titles_original.append(line.rstrip())

    print len(titles_original)
    print len(titles)
    print len(set(titles_original))
    print len(set(titles))

    spacing = len(max(titles_original, key=len))
    print '{:<45}'.format("Actual Title"), '{:<45}'.format("Normalized Title")
    print "-------------------------------------------------------------------"

    for i in range(len(titles)):
        print '{:<45}'.format(titles_original[i]), '{:<45}'.format(string.capwords(titles[i]))



if __name__ == '__main__':
    main()