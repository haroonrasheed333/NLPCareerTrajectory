import os
import csv
from lxml import etree

# resume_id, school_id, institution, degree_level, degree, major_code, major, employer, job_title

user_name = os.environ.get('USER')
xml_directory = '/Users/' + user_name + '/Documents/Data/samples_0418'
degrees_list = []
school_job_details = []
for root, dirs, files in os.walk(xml_directory, topdown=False):
    for f in files:
        try:
            xml = etree.parse(xml_directory + '/' + f)
            education = xml.xpath('//education')[0]
            schools = education.xpath('//school')
            school_details = []
            resume_id = f.split('.')[0]
            for school in schools:
                school_id = school.attrib['id']
                institution = school.xpath('institution/text()')[0]
                degree_level = school.xpath('degree/@level')[0]
                degree = school.xpath('degree/text()')[0]
                major_code = school.xpath('major/@code')[0]
                major = school.xpath('major/text()')[0]
                school_details.append((school_id, institution, degree_level, degree, major_code, major))

            job_details = []
            experience = xml.xpath('//experience')[0]
            jobs = experience.xpath('//job')
            for job in jobs:
                employer = job.xpath('employer/text()')[0]
                job_location = job.xpath('address/city/text()')[0]
                job_state = job.xpath('address/state/text()')[0]
                title = job.xpath('title/text()')[0]
                job_details.append((employer, job_location, job_state, title))

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


        except:
            pass

with open("extracted_data/institution_degree_job_map.csv", "wb") as csv_file:
    writer = csv.writer(csv_file)
    for school_job_detail in school_job_details:
        try:
            writer.writerow(school_job_detail)
        except:
            pass

