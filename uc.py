import csv

f = open('institution_degree_job_map.csv', 'rb')
reader = csv.reader(f)
uc_res = []
for row in reader:
    if row[2].lower() == '' and row[5] == '0402' and row[0] not in uc_res:
        uc_res.append(row[0])

print uc_res
print len(uc_res)
