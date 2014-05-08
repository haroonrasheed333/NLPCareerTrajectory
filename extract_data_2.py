import json

f = open('top_titles.txt', 'rb')
top_jobs = [t.strip() for t in f.readlines()]

salary_data = json.loads(open('salary_json.json').read())['salary_json']
salary_json = dict()

for sal in salary_data:
    salary_json[sal['title']] = sal['compensation']

for j in top_jobs:
    try:
        salary_json[j] = salary_json.pop(j.lower())
    except KeyError:
        pass

titles_data = json.loads(open('static/titlesData.json').read())

titles_data_new = dict()

for title in titles_data:
    titles_data_new[title] = dict()
    titles_data_new[title]["salary"] = '$' + salary_json[title]
    titles_data_new[title]["related_titles"] = titles_data[title]["reported_titles"][:5]
    titles_data_new[title]["description"] = titles_data[title]["description"]
    try:
        education = titles_data[title]["education"][max(titles_data[title]["education"].keys())]
    except:
        education = "N/A"
    titles_data_new[title]["education"] = education
    titles_data_new[title]["trends"] = titles_data[title]["trends"]

j = json.dumps(titles_data_new, indent=4, separators=(',', ': '))
f = open("extracted_data/titlesData_new.json", "w")
print >> f, j
f.close()
print "hi"