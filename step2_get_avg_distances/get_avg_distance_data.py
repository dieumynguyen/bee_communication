# Imports
import json
import numpy as np
import os
import glob2
import re

########################################################################

def get_distances(param_set_json):

    ''' Load in each JSON created by combine_replicates.py and only pull out avg distances
    or distances from others later '''

    with open("/Users/dieumynguyen/Desktop/Projects/bee_communication/step1_combine_replicates/combined_replicates/" + param_set_json, "r") as f:
        data = json.load(f)

    sample_length = len(data[0]["Replicate {}".format(1)]["distance_from_queen"])

    all_distances = []
    for j in range(len(data)):  # Loop over each replicate
        avg_distance = []
        for i in range(sample_length):    # Loop over all the 160 averages/values/lists
            avg_distance.append(data[j]["Replicate {}".format(j+1)]["distance_from_queen"][i]["average"])
        all_distances.append(avg_distance)


    # Write truncated data to JSON
    start_char = "j"
    filename = f.name
    name = filename[100:filename.index(start_char)]

    with open('/Users/dieumynguyen/Desktop/Projects/bee_communication/step2_get_avg_distances/avg_distance_data/{}.json'.format(name), 'w') as outfile:
        json.dump(all_distances, outfile)

    return None

################################ MAIN #################################
def main():
    # Test on one json
    # get_distances("Q0.01_W0.005_D0.05_T0.001.json")

    # Iterate through all (256) JSON's and produce 1 file each
    reps_list = list(map(lambda x : x.split("/")[-1], glob2.glob("/Users/dieumynguyen/Desktop/Projects/bee_communication/step1_combine_replicates/combined_replicates/*")))

    print(reps_list)

    for r in reps_list:
        print("Getting avg distances for: {}".format(r))
        get_distances(r)

if __name__ == '__main__':
    main()
