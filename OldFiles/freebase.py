import json
import urllib

api_key = "AIzaSyCYYNeN_1GIgpYKeTUNSwaUjUcn623UZl4"
# service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
# query = [{'id': None, 'name': 'earth', 'type': '/astronomy/planet'}]
# params = {
#         'query': json.dumps(query),
#         'key': api_key
# }
# url = service_url + '?' + urllib.urlencode(params)
# response = json.loads(urllib.urlopen(url).read())
# for planet in response['result']:
#   print planet['name']


def normalize_university(university_name):
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
            'query': university_name,
            'key': api_key
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    results = response['result']
    print results[0]['name']
    print


univ_names = \
    [
        'uc berkeley', 'university of california, berkeley', 'university of california',
        'university of california at berkeley'
    ]

for u in univ_names:
    normalize_university(u)