__author__ = 'divyakarthikeyan'

from util import stripxml
import os
import re
import time
import csv
import json


def extract_univ(data):
    data = stripxml(str(data))
    data = data.lower()
    # print data
    data = re.sub ('[^A-Za-z0-9 ]+',' ',str(data))
    data = re.sub ('  ',' ',str(data))
    # print data

    if 'education' in data:
        parted = data.split('education')[1]
        second = parted[:150]
    else:
        second = data
    with open("static/UniqueFBUnivNames.csv", 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            row = re.sub('[^A-Za-z0-9 ]+', ' ', str(row))
            row = re.sub('  ', ' ', str(row))
            if str(row).lower() in second:
                if len(str(row).split())>1:
                    return str(row)
                    break
    return ""


def extract_from_resume(data):
    out = {}
    data = stripxml(str(data))
    data = data.lower()
    data = re.sub ('[^A-Za-z0-9 ]+',' ',str(data))
    data = re.sub ('  ',' ',str(data))
    if 'education' in data:
        parted = data.split('education')[1]
        second = parted[:150]
        out['split2'] = second
    else:
        second = data
    with open("static/UniqueFBUnivNames.csv", 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            row = re.sub('[^A-Za-z0-9 ]+', ' ', str(row))
            row = re.sub('  ', ' ', str(row))
            if str(row).lower() in second:
                if len(str(row).split())>1:
                    out['univ'] = str(row)
                    return out
                    break
    return out

if __name__ == '__main__':
    extract_univ("Berekeley")