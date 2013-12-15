import re
import os
import nltk
import shutil
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def kmeans_clustering(source_path, files_list, clusters):
    """
    Function to perform kmeans clustering on the dataset.

    Args:
        source_path -- string. Path where the data files are located.
        files_list -- list of file names in the source path
        clusters -- number of clusters
    """
    stopwords = nltk.line_tokenize(open('stopwords.txt').read())
    docs = []
    filename = {}
    i = 0

    # To avoid np array issues due to large datasets, perform clustering by splitting the data into smaller subsets
    for file_name in files_list[:2000]:
        resume = open(source_path + '/' + file_name).read()
        docs.append(resume)
        filename[i] = file_name
        i += 1

    vectorizer = TfidfVectorizer(min_df=1)
    tfidf = vectorizer.fit_transform(docs)
    km = KMeans(n_clusters=clusters, init='k-means++', max_iter=10, n_init=1)
    km.fit(tfidf)
    results = []

    # Create a results list with filename and predicted cluster value for each resume.
    for i in range(0, len(tfidf.toarray())):
        try:
            results.append([str(filename[i]), int(km.predict(tfidf.toarray()[i]))])
        except:
            pass

    # Copy the resume file from its source directory and move it to new directory according to its predicted cluster
    for cluster in range(0, clusters):
        # Create a combined resume text for each cluster for further analysis using word clouds
        word_cloud_text = ""
        for i in range(0, len(results)-1):
            if results[i][1] == cluster:
                document = open(source_path + '/' + results[i][0], 'r').read()
                docu = re.sub('[^A-Za-z\' ]+', '', str(document).lower())
                unigrams = docu.split()
                word_list = [word.lower() for word in unigrams if word.lower() not in stopwords]
                text = " ".join(word_list)
                word_cloud_text += text
                destination = '/Users/' + user_name + '/Documents/Data/kmeans/pass1/' + str(cluster)
                shutil.copy2(source_path + '/' + results[i][0], destination)


        f = open('/Users/' + user_name + '/Documents/Data/kmeans/wordcloud/pass1/' + str(cluster) + ".txt", 'w')
        f.write(word_cloud_text)
        f.close()


if __name__ == '__main__':
    user_name = os.environ.get('USER')
    source_dir = '/Users/' + user_name + '/Documents/Data/samples_text_50000'
    files = [f for (dirpath, dirnames, filenames) in os.walk(source_dir) for f in filenames if f[-4:] == '.txt']

    num_clusters = 5

    kmeans_clustering(source_dir, files, num_clusters)



