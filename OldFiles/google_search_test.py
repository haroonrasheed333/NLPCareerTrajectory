#!/usr/bin/python
import json
import urllib


def normalize_university(university_name):
    query = urllib.urlencode({'q': university_name})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']
    print hits[0]['titleNoFormatting']


univ_names = \
    [
        'uc berkeley', 'university of california, berkeley', 'university of california',
        'university of california at berkeley'
    ]

for u in univ_names:
    normalize_university(u)