import re
import json
#test = open ("/Users/divyakarthikeyan/univ_map.json" , "wb")
#test.write('{\n')
#with open ("/Users/divyakarthikeyan/Downloads/FBUniversities_aliases_reformated-3.json") as f:
#    for line in f:
#        line = re.sub ('[^A-Za-z0-9:" ]+',' ',str(line))
#        line = re.sub ('  ',' ',str(line))
#        #print line
#        test.write(line.lower() + ',\n')
#    test.write('}')

result = {}
skills_map = json.loads(open ("univ_major_emp_skill_0501.json" , "rb").read())
for key in skills_map:
    result[key] = {}
    result[key]["links"] = []
    for i in range ( 0 ,len(skills_map[key])):
        for j in range (0,len(skills_map[key][i][0])):
            for k in range (0, len(skills_map[key][i][1])):
                newdict = {"source": skills_map[key][i][0][j] , "target" :skills_map[key][i][1][k] , "weight" :1 }
                result[key]["links"].append(newdict)

j = json.dumps(result, indent=4, separators=(',', ': '))
f = open('static/networkgraph.json', 'w')
print >> f, j
f.close()
#
#map = json.loads(open("univ_major_number_map_0501.json" , "rb").read())
#result = {}
#for key in map:
#    univ,code = key.split('_')
#    univ = re.sub ('[^A-Za-z0-9 ]+',' ',str(univ))
#    univ = re.sub ('  ',' ',str(univ))
#    code = code[:4]
#    if univ in result:
#        result[univ][code] = map[key]
#    else:
#        result[univ] = {}
#        result[univ][code] = map[key]
#
#
#
#
#
#j = json.dumps(result, indent=4, separators=(',', ': '))
#f = open('static/univ_mapping.json', 'w')
#print >> f, j
#f.close()




#skills_employer = json.loads(open("static/networkgraph.json").read())
#univ_major_map = json.loads(open("static/univ_mapping.json").read())
#print "from create data for graph"
#univ = "university of california berkeley"
#result = {}
#result["links"] = []
#if univ in univ_major_map:
#    print "here"
#    indices = []
#    for key in univ_major_map[univ]:
#        indices.append(univ_major_map[univ][key])
#    print indices
#    for index in indices:
#        if str(index) in skills_employer:
#            for d in skills_employer[str(index)]["links"]:
#                result["links"].append(d)
#print result