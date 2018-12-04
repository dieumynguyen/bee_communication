# Imports
import json
import numpy as np
import os
import glob2
import re

########################################################################
def get_position_data(param_set_json):

    ''' Load in each JSON created by combine_replicates.py and get position_history data '''

    with open("/Users/dieumynguyen/Desktop/Projects/bee_communication/step1_combine_replicates/combined_replicates/" + param_set_json, "r") as f:
        data = json.load(f)

    # sample_length = len(data[0]["Replicate {}".format(1)]["position_history"])

    all_replicates = []
    for j in range(len(data)):  # Loop over each replicate

        # print(j)

        all_distances = {}
        # Loop over 50 workers
        for i in range(1, 51):
            position = data[j]["Replicate {}".format(j+1)]["position_history"]["worker_{}".format(i)]
            all_distances["worker_{}".format(i)] = position

        all_replicates.append(all_distances)

    # Write truncated data to JSON
    start_char = "json"
    filename = f.name
    name = filename[100:filename.index(start_char)]
    # print(filename)

    with open('/Users/dieumynguyen/Desktop/Projects/bee_communication/step4_position_data_scenting/position_data/{}json'.format(name), 'w') as outfile:
        json.dump(all_replicates, outfile)

    return None

################################ MAIN #################################
def main():
    # Test on one json
    # get_distances("Q0.01_W0.005_D0.05_T0.001.json")

    # Iterate through all (256) JSON's and produce 1 file each
    reps_list = list(map(lambda x : x.split("/")[-1], glob2.glob("/Users/dieumynguyen/Desktop/Projects/bee_communication/step1_combine_replicates/combined_replicates/*")))

    for r in reps_list:
        print("Getting position data for: {}".format(r))
        get_position_data(r)

if __name__ == '__main__':
    main()
