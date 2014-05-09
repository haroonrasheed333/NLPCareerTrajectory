import json

f = open('../extracted_data/top_titles.txt', 'rb')
top_jobs = [t.strip() for t in f.readlines()]

skills_with_percent_dict = json.loads(open('../extracted_data/skills_map_with_percent.json').read())

for j in top_jobs:
    try:
        skills_with_percent_dict[j] = skills_with_percent_dict.pop(j.lower())
    except KeyError:
        pass

# skills_with_percent_dict['UI/UX Designer'] = skills_with_percent_dict.pop('ui/ux designer')
# skills_with_percent_dict['UI/UX developer'] = skills_with_percent_dict.pop('ui/ux developer')

j = json.dumps(skills_with_percent_dict, indent=4, separators=(',', ': '))
f = open('../skills_map_with_percent_new_0504_upper.json', 'w')
print >> f, j
f.close()

# title_dict = \
#     {
#         'customer service associate': 299, 'attorney': 299, 'product manager': 299, 'general manager': 299,
#         'sales associate': 299, 'project manager': 299, 'sales representative': 299, 'executive assistant': 299,
#         'senior project manager': 299, 'accountant': 299, 'vice president': 299, 'graphic designer': 299,
#         'human resources manager': 299, 'business analyst': 299, 'assistant manager': 299,
#         'chief executive officer': 299, 'senior software engineer': 299, 'president': 299, 'financial analyst': 299,
#         'customer service representative': 299, 'marketing manager': 299, 'consultant': 299,
#         'administrative assistant': 299, 'senior accountant': 299, 'program manager': 299, 'software engineer': 299,
#         'web developer': 292, 'account executive': 279, 'recruiter': 278, 'designer': 276, 'ui/ux designer': 264,
#         'sales manager': 259, 'business development manager': 255, 'senior consultant': 251, 'executive director': 246,
#         'chief information officer': 230, 'marketing specialist': 219, 'senior vice president': 215,
#         'chief financial officer': 210, 'quality assurance analyst': 202, 'senior financial analyst': 200,
#         'human resources generalist': 195, 'data analyst': 195, 'marketing assistant': 194, 'technical writer': 192,
#         'information technology manager': 190, 'information technology consultant': 188, 'senior business analyst': 185,
#         'accounting assistant': 182, 'customer service manager': 177, 'chief operating officer': 176,
#         'business consultant': 165, 'systems administrator': 155, 'human resources assistant': 153,
#         'management consultant': 137, 'assistant vice president': 135, 'legal assistant': 129,
#         'web designer': 121, 'senior program manager': 120, 'human resources coordinator': 119,
#         'sales consultant': 116, 'marketing consultant': 114, 'senior director': 113, 'human resources director': 111,
#         'managing director': 110, 'developer': 98, 'marketing director': 98, 'marketing coordinator': 93,
#         'systems analyst': 77, 'accounting manager': 64, 'senior account executive': 63,
#         'executive administrative assistant': 61, 'associate director': 59, 'assistant director': 58,
#         'senior account manager': 55, 'system engineer': 49, 'legal secretary': 49, 'senior associate': 48,
#         'computer technician': 32, 'business development director': 8, 'ux researcher': 2, 'data researcher': 2,
#         'data scientist': 1
#     }
#
# title_title_dict = dict()
#
# for title in top_jobs:
#     value = title_dict.get(title.lower(), None)
#     if value is not None:
#         title_title_dict[title.lower()] = title
#
# title_title_dict['ui/ux designer'] = 'UI/UX Designer / Developer'
# title_title_dict['ui/ux designer / developer'] = 'UI/UX Designer / Developer'
#
# j = json.dumps(title_title_dict, indent=4, separators=(',', ': '))
# f = open('title_title_map.json', 'w')
# print >> f, j
# f.close()
#
# print "hi"