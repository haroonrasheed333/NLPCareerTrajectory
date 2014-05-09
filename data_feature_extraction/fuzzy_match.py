from fuzzywuzzy import fuzz

job_titles = []
f = open('../extracted_data/JobTitles.txt')
for line in f:
    job_titles.append(line.lower().rstrip())

job_titles = list(set(job_titles))
print len(job_titles)

for i in job_titles:
    for j in job_titles:
        if 90 < fuzz.ratio(i, j) < 100:
        # if fuzz.partial_ratio(i, j) == 100:
            print "Title1: ", i
            print "Title2: ", j
            print