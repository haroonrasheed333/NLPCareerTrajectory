import os
import csv
import json
from lxml import etree
import re
from util import stripxml
from univ_lookup import extract_univ
# resume_id, school_id, institution, degree_level, degree, major_code, major, employer, job_title

user_name = os.environ.get('USER')
xml_directory = '/Users/' + user_name + '/Documents/Data/samples_0418'
univ_major_number_map = dict()
univ_major_list = []
univ_major_emp_skill = dict()
counter = 0
names = []
univ_dict = json.loads(open("static/univs_list.json","rb").read())
univ_normalize = json.loads(open("static/univ_map.json","rb").read())
print univ_normalize["oakland city university main campus"]

with open('skills_0424_no_stemming_full_ds.json') as skills_json_file:
    skills_json = json.loads(skills_json_file.read())

for root, dirs, files in os.walk(xml_directory, topdown=False):
    for f in files:

        try:
            xml = etree.parse(xml_directory + '/' + f)
            name = xml.xpath('//givenname/text()')[0] + ' ' + xml.xpath('//surname/text()')[0]
            if name not in names:
                names.append(name)
                education = xml.xpath('//education')[0]
                schools = education.xpath('//school')

                resume_id = f.split('.')[0]
                temp_univ_major_list = []
                for school in schools:
                    school_text = stripxml(etree.tostring(school))
                    #institution = school.xpath('institution/text()')[0]
                    institution = extract_univ( school_text, univ_dict, univ_normalize)
                    institution = re.sub ('[^A-Za-z0-9 ]+',' ',str(institution))
                    institution = re.sub ('  ',' ',str(institution))
                    #print institution
                    if institution.lower() in univ_normalize:
                        #print "NORMALIZED"
                        institution = univ_normalize[institution]

                    degree_level = school.xpath('degree/@level')[0]
                    degree = school.xpath('degree/text()')[0]
                    major_code = str(school.xpath('major/@code')[0])
                    major = school.xpath('major/text()')[0]

                    temp_univ_major_list.append(str(institution + '_' + major_code).lower())
                    if str(institution + '_' + major_code).lower() not in univ_major_list:
                        counter += 1
                        univ_major_list.append(str(institution + '_' + major_code).lower())
                        univ_major_number_map[str(institution + '_' + major_code).lower()] = counter
                        #univ_major_number_map[str(institution + '_' + major).lower()] = counter

                    if str(institution + '_' + major).lower() == 'vellore institute of technology_computer science':
                        pass

                employers = []
                experience = xml.xpath('//experience')[0]
                jobs = experience.xpath('//job')
                for job in jobs:
                    try:
                        employer = job.xpath('employer/text()')[0]
                        employers.append(employer)
                    except:
                        pass

                try:
                    skills = skills_json[f]
                except:
                    skills = []

                temp_list = [employers, skills]

                for tum in temp_univ_major_list:
                    value = univ_major_emp_skill.get(univ_major_number_map[tum])
                    if value is not None:
                        univ_major_emp_skill[univ_major_number_map[tum]].append(temp_list)
                    else:
                        univ_major_emp_skill[univ_major_number_map[tum]] = []
                        univ_major_emp_skill[univ_major_number_map[tum]].append(temp_list)


        except:
            pass

j = json.dumps(univ_major_emp_skill, indent=4, separators=(',', ': '))
f = open('univ_major_emp_skill_0502.json', 'w')
print >> f, j
f.close()

j1 = json.dumps(univ_major_number_map, indent=4, separators=(',', ': '))
f = open('univ_major_number_map_0502.json', 'w')
print >> f, j1
f.close()