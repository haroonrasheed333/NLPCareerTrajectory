import urllib2
from bs4 import BeautifulSoup
import re
import csv
import json


def cell_text(cell):
    return " ".join(cell.stripped_strings)
#
#soup = BeautifulSoup(urllib2.urlopen('http://www.onetonline.org/find/industry?i=0&g=Go').read())
#output = csv.writer(open("static/onet.csv", "wb"))
#
#for table in soup.find_all('table'):
#    for row in table.find_all('tr'):
#        col = map(cell_text, row.find_all(re.compile('t[dh]')))
#        output.writerow(col)
#    output.writerow([])

result = dict()
#onet = csv.reader(open("static/onet.csv","rb"))
titles = csv.reader(open("../extracted_data/top_titles.txt", "rb"))
for line in titles:
    result["%s" %line[0]] = {}


    lineModified = re.sub(' ','+', line[0])
    # soup = BeautifulSoup(urllib2.urlopen('http://www.onetonline.org/find/quick?s=' + '%s' %lineModified).read())
    # i = 0
    # for table in soup.find_all('table'):
    #     for row in table.find_all('tr'):
    #         if i ==1:
    #             col = map(cell_text, row.find_all(re.compile('t[dh]')))
    #             result["%s" %line[0]]["actual title"] = str(col[2]).strip('Bright Outlook')
    #             code = str(col[1])
    #             break
    #         i = i+1

    soup = BeautifulSoup(urllib2.urlopen('http://www.onetonline.org/link/summary/' + '%s' %code).read())
    result["%s" %line[0]]["description"] = str(soup.find_all('p')[0]).strip('<>p/')

    if (str(soup.find_all('p')[1])[:13] == '<p>\n<b>Sample'):
        result["%s" %line[0]]["reported titles"] = str(soup.find_all('p')[1]).split('</b>')[1].strip("</p>").strip('\n').split(',')
    else:
       result["%s" %line[0]]["reported titles"] = []
    table = soup.find('table', {"summary":"Wages & Employment Trends information for this occupation"})
    result["%s" %line[0]]["trends"] = {}
    if table:
        for row in table.find_all('tr'):
            col = map(cell_text, row.find_all(re.compile('t[dh]')))
            result["%s" %line[0]]["trends"][str(col[0])] = str(col[1])

    table = soup.find('table',{"summary":"Education information for this occupation"})
    result["%s" %line[0]]["education"] = {}
    if table:
        for row in table.find_all('tr'):
            if i > 1:
                col = map(cell_text, row.find_all(re.compile('t[dh]')))
                result["%s" %line[0]]["education"][str(col[0])] = str(col[1])
            i += 1

    lineModified = re.sub(' ','-', line[0])
    try:
        soup = BeautifulSoup(urllib2.urlopen('http://www.simplyhired.com/salaries-k-' + '%s' %lineModified + '-jobs.html').read())

        if (str(soup.find_all('p')[3])[:14] == "<p>The average"):

            result["%s" %line[0]]["salary"] = '$' + str(soup.find_all('p')[3]).split('$')[1].split('.')[0]

        else:
            result["%s" %line[0]]["salary"] = 'No data'

    except urllib2.HTTPError, e:
        result["%s" %line[0]]["salary"] = 'No data'

    print result["%s" %line[0]]


j = json.dumps(result, indent=4, separators=(',', ': '))
f = open("static/../static/titlesData.json", "w")
print >> f, j
f.close()