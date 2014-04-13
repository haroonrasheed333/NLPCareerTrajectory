import csv
import json
import urllib


def extract_univ_names():
    univs_dict = dict()
    univ_names = []
    with open('univ_degree_4-12-14.csv', 'rb') as univ_file:
        csv_reader = csv.reader(univ_file)

        for row in csv_reader:
            try:
                if row[0] and row[1]:
                    univs_dict[row[0]] = row[0].lower().strip()
                    univ_names.append(row[0].lower().strip())
            except:
                pass

        j = json.dumps(univs_dict, indent=4, ensure_ascii=False)
        f = open('Universities.json', 'w')
        print >> f, j
        f.close()

        univ_names = list(set(univ_names))
        f = open('UnivNames.txt', 'w')
        for u in univ_names:
            print >> f, u

        f.close()


def normalize_universities():
    with open('UnivNames.txt') as u_names:
        univ_names = u_names.readlines()
        univ_dict_normalized = dict()
        i = 0
        while i < 10000:
            try:
                u = univ_names[i].strip()
                if u:
                    api_key = "AIzaSyCYYNeN_1GIgpYKeTUNSwaUjUcn623UZl4"
                    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
                    query = [{'id': None, 'name': None, 'name~=': u.strip()}]
                    params = \
                        {
                            'query': json.dumps(query, ensure_ascii=False),
                            'key': api_key
                        }
                    url = service_url + '?' + urllib.urlencode(params)
                    response = json.loads(urllib.urlopen(url).read())
                    result = response['result']
                    if result and len(result) == 1:
                        univ_dict_normalized[u] = result[0]['name']
                    else:
                        univ_dict_normalized[u] = u
                i += 1
            except:
                pass

        js = json.dumps(univ_dict_normalized, indent=4, ensure_ascii=False)
        f = open('Universities_normalized1.json', 'w')
        print >> f, js
        f.close()


normalize_universities()

