import re
import csv
import json
import urllib2
from bs4 import BeautifulSoup


def cell_text(cell):
    return " ".join(cell.stripped_strings)

title_onet_dict = dict()
with open('title_onet_txt.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        value = title_onet_dict.get(row[0], None)
        if value is None:
            title_onet_dict[row[0]] = dict()
            title_onet_dict[row[0]][row[1]] = dict()
        else:
            value1 = title_onet_dict[row[0]].get(row[1])
            if value1 is None:
                title_onet_dict[row[0]][row[1]] = dict()

for title in title_onet_dict:
    for onet in title_onet_dict[title]:
        soup = BeautifulSoup(urllib2.urlopen('http://www.onetonline.org/link/summary/' + onet).read())
        title_onet_dict[title][onet]["description"] = str(soup.find_all('p')[0]).strip('<>p/')

        if str(soup.find_all('p')[1])[:13] == '<p>\n<b>Sample':
            title_onet_dict[title][onet]["reported_titles"] = \
                str(soup.find_all('p')[1]).split('</b>')[1].strip("</p>").strip('\n').split(',')
        else:
           title_onet_dict[title][onet]["reported_titles"] = []

        table = soup.find('table', {"summary":"Wages & Employment Trends information for this occupation"})
        title_onet_dict[title][onet]["trends"] = {}
        if table:
            for row in table.find_all('tr'):
                col = map(cell_text, row.find_all(re.compile('t[dh]')))
                title_onet_dict[title][onet]["trends"][str(col[0])] = str(col[1])

        table = soup.find('table',{"summary":"Education information for this occupation"})
        title_onet_dict[title][onet]["education"] = {}
        if table:
            for row in table.find_all('tr'):
                col = map(cell_text, row.find_all(re.compile('t[dh]')))
                title_onet_dict[title][onet]["education"][str(col[0])] = str(col[1])

j = json.dumps(title_onet_dict, indent=4, separators=(',', ': '))
f = open("static/titlesData_0505.json", "w")
print >> f, j
f.close()


print "Hi"