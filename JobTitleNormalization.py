import re
normalize = [
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
]

f = open('labels_50000.txt')

for line in f:
    title = line.split('\t')[1]
    for match in normalize:
        title = re.sub(r'\b' + match[0] + r'\b', match[1], title.lower().replace('.', ''))

    if title.lower() != line.split('\t')[1].lower():
        print line.split('\t')[1]
        print title