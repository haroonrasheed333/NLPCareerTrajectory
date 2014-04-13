import csv
import json

with open('univ_degree_employer_4-11-14_new.csv', 'rb') as univ_degree_employer_file:
    univ_degree_employer_reader = csv.reader(univ_degree_employer_file)

    i = 0

    univ_degree_employer_dict = dict()

    for ude in univ_degree_employer_reader:
        try:
            if i == 0:
                i += 1
                continue
            num_resumes = int(ude[0])
            univ = ude[1].lower().strip()
            degree = ude[2].lower().strip()
            employer = ude[3].lower().strip()
            try:
                univ_degree_employer_dict[(univ, degree)][employer] += num_resumes
            except:
                try:
                    univ_degree_employer_dict[(univ, degree)][employer] = num_resumes
                except:
                    univ_degree_employer_dict[(univ, degree)] = dict()
                    univ_degree_employer_dict[(univ, degree)][employer] = num_resumes
            i += 1
        except:
            i += 1

    js = json.dumps({str(k): v for k, v in univ_degree_employer_dict.iteritems()}, indent=4, ensure_ascii=False)
    f = open('University_degree_employer.json', 'w')
    print >> f, js
    f.close()
    print "hi"

