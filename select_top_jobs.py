import os
import re
# import progressbar
from lxml import etree
from collections import Counter
from JobTitleNormalization import normalize_job_titles

user_name = os.environ.get('USER')


def stripxml(data):
    """
    Strip the xml tags from the xml to make it plaintext

    Args:
        data -- Resume xml

    Returns:
        text -- plaintext resume without any xml tags.
    """
    pattern = re.compile(r'<.*?>')
    text = pattern.sub('', str(data))
    return text


def extract_top_jobs(source_dir):
    """
    Function to extract top jobs

    Args:
        source_dir -- path to the source xml files.

    """

    # Get the files from the source directory
    files = [f for (dirpath, dirnames, filenames) in os.walk(source_dir) for f in filenames if f[-4:] == '.txt']

    names = []
    job_titles = []

    # j, bar = 0, pbar(len(files))
    # bar.start()
    labels_list = []

    # From each xml file extract the information and store in plaintext files.
    for fname in files:
        # Create an xml parser object
        xml = etree.parse(source_dir + '/' + fname)

        # Extract the current job title, and current job element from xml
        current_job_title = xml.xpath('//job[@end = "present"]/title/text()')

        try:
            # Since there are many duplicate resumes in the data, filter out the resumes based on candidate name.
            # Extract the candidate name from the resume
            name = xml.xpath('//givenname/text()')[0] + ' ' + xml.xpath('//surname/text()')[0]

            if name not in names:
                names.append(name)

                if current_job_title:
                    i = 0
                    if len(current_job_title) > 1:
                        while i < len(current_job_title):
                            job_titles.append(current_job_title[i])
                            i += 1
                    else:
                        job_titles.append(current_job_title[0])

        except:
            pass

    #     j += 1
    #     bar.update(j)
    # bar.finish()

    print job_titles[:10]
    print len(job_titles)
    print len(set(job_titles))
    print Counter(job_titles).most_common(200)
    normalized_titles = normalize_job_titles(job_titles)
    print len(normalized_titles)
    print len(set(normalized_titles))
    top_normalized_jobs_counter = Counter(normalized_titles).most_common(200)
    print top_normalized_jobs_counter

    top_normalized_jobs = []
    for tj in top_normalized_jobs_counter:
        top_normalized_jobs.append(tj[0])

    return top_normalized_jobs


# def pbar(size):
#     """
#     Function to display the progress of a long running operation.
#
#     """
#     bar = progressbar.ProgressBar(maxval=size,
#                                   widgets=[progressbar.Bar('=', '[', ']'),
#                                            ' ', progressbar.Percentage(),
#                                            ' ', progressbar.ETA(),
#                                            ' ', progressbar.Counter(),
#                                            '/%s' % size])
#     return bar


if __name__ == "__main__":
    print extract_top_jobs('/Users/' + user_name + '/Documents/Data/samples_0418')

