# Imports
import json
import numpy as np
import os
import glob2
import re

########################################################################
def distance_bw_workers(param_set_json):

    ''' Load in each JSON created by combine_replicates.py and get distance_bw_workers '''

    with open("combined_replicates/" + param_set_json, "r") as f:
        data = json.load(f)

    # sample_length = len(data[0]["Replicate {}".format(1)]["position_history"])

    all_replicates = []
    for j in range(len(data)):  # Loop over each replicate

        # print(j)

        # all_distances = []
        # Loop over 50 workers
        # for i in range(1, 51):
        distances = data[j]["Replicate {}".format(j+1)]["distance_from_others"]
        # all_distances.append(distances)

        all_replicates.append(distances)

    # Write truncated data to JSON
    start_char = "j"
    filename = f.name
    name = filename[20:filename.index(start_char)]

    with open('distance_bw_workers/{}json'.format(name), 'w') as outfile:
        json.dump(all_replicates, outfile)

    return None

################################ MAIN #################################
def main():
    # Test on one json
    # distance_bw_workers("Q0.15_W0.01_D0.35_T0.5_wb1.json")

    # Iterate through all (256) JSON's and produce 1 file each
    reps_list = list(map(lambda x : x.split("/")[-1], glob2.glob("combined_replicates/*")))

    for r in reps_list:
        print("Getting distance bw workers for: {}".format(r))
        distance_bw_workers(r)

if __name__ == '__main__':
    main()
