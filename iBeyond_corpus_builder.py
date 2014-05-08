import os
import re
import time
import random
import shutil
import progressbar
from collections import Counter
from lxml import etree
from util import stripxml
from collections import defaultdict
from job_title_normalization import normalize_job_titles

user_name = os.environ.get('USER')

f = open('top_titles.txt', 'rb')
top_jobs = [t.strip().lower() for t in f.readlines()]

job_count = defaultdict(int)


def split_data(labels_list, paths):
    """
    Function to split the dataset into training and heldout datasets

    Args:
        labels_list -- list of tuples with filename and tag information for each resume
        paths -- Dict consisting of source and destination directories for data
    """

    # Path where the sample text resumes are present
    source_dir = paths['main_source_directory'] + '/' + paths['plaintext_data_directory']

    # Store the training and heldout data in different directories.
    training_dir = paths['main_source_directory'] + '/' + paths['training_directory']
    heldout_dir = paths['main_source_directory'] + '/' + paths['heldout_directory']

    random.seed(int(time.time()))
    random.shuffle(labels_list)

    num_files = len(labels_list)

    # Split the training and heldout files
    training_files = labels_list[:int(num_files*0.8)]
    heldout_files = labels_list[int(num_files*0.8):]

    labels = open(paths['main_source_directory'] + '/' + paths['labels_file_path'], 'w')
    labels_heldout = open(paths['main_source_directory'] + '/' + paths['labels_heldout_file_path'], 'w')

    for (filename, tag) in training_files:
        shutil.copy2(source_dir + '/' + filename, training_dir)
        labels.writelines(filename + "\t" + tag + "\n")

    for (filename, tag) in heldout_files:
        shutil.copy2(source_dir + '/' + filename, heldout_dir)
        labels_heldout.writelines(filename + "\t" + tag + "\n")

    labels.close()
    labels_heldout.close()


def clean_data_and_extract_job_titles(fname, paths, names, job_titles, labels_list):
    """
    Function to clean data and extract job titles from resume.

    Args:
        fname - string. Name of the resume file
        paths - dict containing paths of source directories
        names - string. Extracted candidate names from resume. Used to remove duplicate resumes.
        job_titles - list. Titles extracted from resume
        labels_list - list. Titles that will be used as labels for classifier.

    """

    source_dir = paths['main_source_directory'] + '/' + paths['xml_data_directory']

    try:
        xml = etree.parse(source_dir + '/' + fname)

        # Extract the current job title, and current job element from xml
        current_job_title = xml.xpath('//job[@end = "present"]/title/text()')
        current_job_title = normalize_job_titles(current_job_title)
        current_job = xml.xpath('//job[@end = "present"]')

        # Extract the contact information from xml.
        contact = xml.xpath('//contact')

        # Since there are many duplicate resumes in the data, filter out the resumes based on candidate name.
        # Extract the candidate name from the resume
        name = xml.xpath('//givenname/text()')[0] + ' ' + xml.xpath('//surname/text()')[0]

        if name not in names:
            names.append(name)
        else:
            return names, job_titles, labels_list

        # Remove the candidate contact information from the resume.
        if contact:
                contact[0].getparent().remove(contact[0])

        # Remove the current job section from the resume as we will be using current job title as lable and
        # use our algorithm to predict it.
        if current_job:
            if len(current_job) > 1:
                i = 0
                while i < len(current_job):
                    current_job[i].getparent().remove(current_job[i])
                    i += 1
            else:
                current_job[0].getparent().remove(current_job[0])

            # Convert xml to string.
            xml = etree.tostring(xml, pretty_print=True)

            # Strip the xml tags from the resume.
            text_data = stripxml(xml)
            i = 0
            flag = 0

            # From the resume text remove all the words matching the current job title as we do not want any
            # information about the current job in the resume text.
            if current_job_title:
                text_data = text_data.replace(current_job_title[0].strip(), '')
                if current_job_title[0].strip() in top_jobs:
                    flag = 1
                    job_count[current_job_title[0].strip()] += 1

        # Only save the resumes whose current job title is present in the top 100 jobs
        if flag == 1 and job_count[current_job_title[0].strip()] < 300:

            if current_job_title:
                job_titles.append(current_job_title[0].strip())
                directory = paths['main_source_directory'] + '/' + paths['plaintext_data_directory'] + '/'
                f = open(directory + '%s' % fname[:-4] + '_plaintext.txt', 'w')
                f.write(text_data)
                f.close()

                labels_list.append((fname[:-4] + '_plaintext.txt', current_job_title[0].strip().replace('\n', '')))

        return names, job_titles, labels_list
    except:
        return names, job_titles, labels_list

   
def prepare_data(paths):
    """
    Function to prepare data and split training and test data.

    Args:
        paths - dict containing paths of source directories

    """

    source_dir = paths['main_source_directory'] + '/' + paths['xml_data_directory']
    # Get the files from the source directory
    files = [f for (dirpath, dirnames, filenames) in os.walk(source_dir) for f in filenames if f[-4:] == '.txt']

    random.seed(int(time.time()))
    random.shuffle(files)

    names = []
    job_titles = []
    labels = []

    j, bar = 0, pbar(len(files))
    bar.start()

    # From each xml file extract the information and store in plaintext files.
    for f in files:
        # Create an xml parser object
        (names, job_titles, labels_list) = clean_data_and_extract_job_titles(f, paths, names, job_titles, labels)

        j += 1
        bar.update(j)
    bar.finish()

    # Split the saved resumes (resumes belonging to top 100 job titles) into training and heldout datasets.
    print Counter(job_titles)
    split_data(labels, paths)

    return


def pbar(size):
    """
    Function to display the progress of a long running operation.

    """
    bar = progressbar.ProgressBar(maxval=size,
                                  widgets=[progressbar.Bar('=', '[', ']'),
                                           ' ', progressbar.Percentage(),
                                           ' ', progressbar.ETA(),
                                           ' ', progressbar.Counter(),
                                           '/%s' % size])
    return bar

if __name__ == "__main__":
    paths = dict()
    paths['main_source_directory'] = '/Users/' + user_name + '/Documents/Data/'
    paths['xml_data_directory'] = 'samples_0426'
    paths['plaintext_data_directory'] = 'samples_0426_text'
    paths['training_directory'] = 'training_0426'
    paths['heldout_directory'] = 'heldout_0426'
    paths['labels_file_path'] = 'labels_0426.txt'
    paths['labels_heldout_file_path'] = 'labels_heldout_0426.txt'

    prepare_data(paths)

