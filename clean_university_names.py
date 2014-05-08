import re
import json

result = {}
skills_map = json.loads(open ("univ_major_emp_skill_0507.json" , "rb").read())
for key in skills_map:
    for i in range ( 0 ,len(skills_map[key])):
        for j in range (0,len(skills_map[key][i][0])):
            if skills_map[key][i][0][j].lower() not in result:
                result[skills_map[key][i][0][j].lower()] = {}
print "got employers"
for emp in result:
    for key in skills_map:
        for i in range (0 ,len(skills_map[key])):
            if emp.lower() in skills_map[key][i][0]:
                for j in range (0, len(skills_map[key][i][0])):
                    if skills_map[key][i][0][j].lower() != emp.lower():
                        if skills_map[key][i][0][j].title() not in result[emp.lower()]:
                            result[emp.lower()][skills_map[key][i][0][j].title()] = 1
print "almost there"
j = json.dumps(result, indent=4, separators=(',', ': '))
f = open('static/treegraphemployer0507.json', 'w')
print >> f, j
f.close()
