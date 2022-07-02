from util_1 import *
import numpy as np
from joblib import Parallel, delayed, cpu_count
import os
import pickle
from datasets import DATASET


def extract_features(br, java_src_dict, all_similarities_i):
    """ Extracts features for 50 wrong(randomly chosen) files for each
        right(buggy) file for the given bug report.

    Arguments:
        i {integer} -- Index for printing information
        br {dictionary} -- Given bug report
        bug_reports {list of dictionaries} -- All bug reports
        java_src_dict {dictionary} -- A dictionary of java source codes
    """

    br_id = br.bug_id
    br_files = br.files

    features = []

    for java_file in br_files:
        java_file = os.path.normpath(java_file)

        try:
            # Source code of the java file
            src_keys = list(java_src_dict.keys())
            index = src_keys.index(java_file)

            # rVSM Text Similarity
            rvsm = all_similarities_i[index]

            features.append([br_id, java_file, rvsm, 1])

            for java_file, rvsm in top_k_wrong_files(br, java_src_dict, all_similarities_i):
                features.append([br_id, java_file, rvsm, 0])

        except:
            pass

    return features


'''extracted_features = extract_features()
sum_rank_1 = 0
num_features = 0

for features in extracted_features:
    rank_1 = 1
    features = sorted(features, key=lambda x: x[-2], reverse=True)
    
    for feature in features:
        num_features += 1
        if feature[-1] == 1:
            break
        else:
            rank_1 += 1
    sum_rank_1 += rank_1

print(sum_rank_1 / num_features)'''



