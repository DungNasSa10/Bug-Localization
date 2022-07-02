import csv
import os
import random
import timeit
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from datasets import DATASET


def all_vsm_similarity_i(br_text, src_texts):
    """ Calculates the VSM Similarity between all bug reports and all source files

    Arguments:
        bug_reports {OrderDict of BugReport} -- all bug reports
        java_src_dict {OrderDict of SourceFile} -- all source files
    """

    tfidf = TfidfVectorizer(sublinear_tf=True, smooth_idf=False)
    src_tfidf = tfidf.fit_transform(src_texts)
    br_tfidf = tfidf.transform(br_text)

    # normalizing the length of sources files
    src_lengths = np.array([float(len(src_text.split())) for src_text in src_texts]).reshape(-1, 1)
    min_max_scaler = MinMaxScaler()
    normalized_src_len = min_max_scaler.fit_transform(src_lengths)

    # Applying logistic length function
    src_len_score = 1 / (1 + np.exp(-12 * normalized_src_len))

    s = cosine_similarity(src_tfidf, br_tfidf)
    # revised VSM score caculation
    rvsm_score = s * src_len_score
    all_normalized_simi_i = np.concatenate(min_max_scaler.fit_transform(rvsm_score))

    return all_normalized_simi_i


def top_k_wrong_files(br, java_src_dict, all_similarities_i, k=50):
    """ Randomly samples 2*k from all wrong files and returns metrics
        for top k files according to rvsm similarity.

    Arguments:
      br {BugReport} -- the current bug_report
      bug_reports {OrderDict of BugReport} -- all bug reports
      java_src_dict {OrderDict of SourceFile} -- all source files
      all_similarities_i {2D list} -- vsm_similarity all bug reports and all source files
      all_similarities_i {2D list} -- semantic_similarity of all bug reports and all source files

    Keyword Arguments:
        k {integer} -- the number of files to return metrics (default: {50})
    """

    right_files = br.files
    # Randomly sample 2*k files
    randomly_sampled = random.sample(set(java_src_dict) - set(right_files), 2*k)
    #sampled = set(java_src_dict) - set(right_files)

    all_files = []
    for java_file in randomly_sampled:
        java_file = os.path.normpath(java_file)

        try:
            # Source code of the java file
            src_keys = list(java_src_dict.keys())
            index = src_keys.index(java_file)

            # rVSM Text Similarity
            rvsm = all_similarities_i[index]

            all_files.append([java_file, rvsm])
        except:
            pass

    top_k_files = sorted(all_files, key=lambda x: x[1], reverse=True)[:k]

    return top_k_files



