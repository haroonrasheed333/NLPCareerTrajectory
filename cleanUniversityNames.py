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
#
#result = {}
#
#skills_map = json.loads(open ("univ_major_emp_skill_0502.json" , "rb").read())
#for key in skills_map:
#    result[key] = {}
#    result[key]["name"] = "Me"
#    result[key]["children"] = []
#    for i in range ( 0 ,len(skills_map[key])):
#        for j in range (0,len(skills_map[key][i][0])):
#            skills_map[key][i][0][j] = skills_map[key][i][0][j].lower()
#            newdict = {}
#            newdict = {"name": skills_map[key][i][0][j].title() , "children" :[]}
#            result[key]["children"].append(newdict)
#
#j = json.dumps(result, indent=4, separators=(',', ': '))
#f = open('static/treegraphdata.json', 'w')
#print >> f, j
#f.close()
#
#j = json.dumps(skills_map, indent=4, separators=(',', ': '))
#f = open('univ_major_emp_skill_0507.json', 'w')
#print >> f, j
#f.close()




#result = {}
#
#skills_map = json.loads(open ("univ_major_emp_skill_0507.json" , "rb").read())
#for key in skills_map:
#    for i in range ( 0 ,len(skills_map[key])):
#        for j in range (0,len(skills_map[key][i][0])):
#            if  skills_map[key][i][0][j].lower() not in result:
#                result[skills_map[key][i][0][j].lower()] = []
#print len(result)
##i = 0
#emp_names = json.loads(open ("static/treegraphemployer.json" , "rb").read())
#tree1 = json.loads(open ("static/treegraphdata1.json" , "rb").read())
#tree2 = json.loads(open ("static/treegraphdata2.json" , "rb").read())
#
#for key in tree1:
#    for name in tree1[key]["children"]:
#        if name["name"].lower() in emp_names:
#            for employer in emp_names[name["name"].lower()]:
#                #print employer
#                name["children"].append({"name" : employer , "children" : []})
#
#print len(tree1)
#j = json.dumps(tree1, indent=4, separators=(',', ': '))
#f = open('static/tree1.json', 'wb')
#print >> f, j
#f.close()


#for key in tree2:
#    for name in tree2[key]["children"]:
#        if name["name"].lower() in emp_names:
#            for employer in emp_names[name["name"].lower()]:
#                #print employer
#                name["children"].append({"name" : employer , "children" : []})
#
#print len(tree2)
#j = json.dumps(tree2, indent=4, separators=(',', ': '))
#f = open('static/tree2.json', 'wb')
#print >> f, j
#f.close()
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

#map = json.loads(open("univ_major_number_map_0502.json" , "rb").read())
#result = {}
#new_univs = []
#for key in map:
#
#    univ,code = key.split('_')
#    univ = re.sub ('[^A-Za-z0-9 ]+',' ',str(univ))
#    univ = re.sub ('  ',' ',str(univ))
#    code = re.sub ('[^A-Za-z0-9 ]+',' ',str(code))
#    code = re.sub ('  ',' ',str(code))
#    code_list_new = []
#    code_list_new = code.split()[1:]
#    code = code.split()[0]
#    if univ:
#        if (code_list_new):
#            new_univs.append([univ,code_list_new,key])
#
#        if univ in result:
#            if str(code) not in result[univ]:
#                result[univ][str(code)] = map[key]
#            else:
#                pass
#        else:
#            result[univ] = {}
#            result[univ][str(code)] = map[key]
#
#for univ in new_univs:
#    for code in univ[1]:
#        if univ[0] in result:
#            if str(code) not in result[univ[0]]:
#                result[univ[0]][str(code)] = map[univ[2]]
#
#        else:
#            result[univ[0]] = {}
#            result[univ[0]][str(code)] = map[univ[2]]
#
#
#
#j = json.dumps(result, indent=4, separators=(',', ': '))
#f = open('static/univ_mapping.json', 'w')
#print >> f, j
#f.close()



#
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


#major_code_lookup = json.loads(open("/Users/divyakarthikeyan/Downloads/DeptCodes-3.json").read())
#result = {}
#for key in major_code_lookup:
#    result [major_code_lookup[key]]= key
#
#
#
#j = json.dumps(result, indent=4, separators=(',', ': '))
#f = open('static/DeptCodes.json', 'w')
#print >> f, j
#f.close()


# univ = '"uc berekley"'
# print univ.strip("'")
