# Combine data of interest of 15 replicates of a single set of parameters
# into a single json file for further analysis

########################################################################

# Imports
import json
import numpy as np
import os
import glob2
import re

########################################################################

def load_config_measurements(experiment_dir, replicate_i):

    ''' This function loads in data from a single experiment given
    the directory path and replicate number. Returns a dictionary
    of a single replicate containing: model parameter configurations,
    distance from queen & from other workers.
    '''

    ### Load config.json
    with open(experiment_dir + "/config.json", "r") as f:
        config_dict = json.load(f)

    # Pull out params of interest from config.json
    D = config_dict['diffusion_coefficient']
    Q = config_dict['swarm_parameters']['queen_bee_concentration']
    W = config_dict['swarm_parameters']['worker_bee_concentration']
    T = config_dict['swarm_parameters']['worker_bee_threshold']

    ### Load measurements.json
    try:
        with open(experiment_dir + "/data/measurements.json", "r") as f:
            measurements = json.load(f)
    except Exception as e:
        print("Function failing at: {}".format(experiment_dir))
        raise e

    else:
        # Pull out params of interest from measurements.json
        distance_from_queen = measurements['distance_from_queen']
        distance_from_others = measurements['distance_from_others']
        position_history = measurements['position_history']

        # Create dict
        parameters = ['diffusion_coefficient', 'queen_bee_concentration',
             'worker_bee_concentration', 'worker_bee_threshold',
             'distance_from_queen', 'distance_from_others', 'position_history']
        values = [D, Q, W, T, distance_from_queen, distance_from_others, position_history]
        experiment_dict = dict(zip([p for p in parameters], values))
        outer_dict = {"Replicate {}".format(replicate_i) : experiment_dict}

    return outer_dict

########################################################################

def combine_replicates(data_folders, param_set):
    ''' This function finds replicates of a set of parameters across
    all experiment runs. Iteratively calls the function
    "load_config_measurements" to create a dictionary for a single
    replicate. Then combine all replicates' data into a list, and write
    to a JSON file for further data analysis. Will run this 64 times for
    64 sets.
    '''

    # List to contain all replicates
    all_replicates = []

    # If find the param_set in a data_folders[i], get the index of
    # that data_folders[i]
    data_folder_i = []
    for i in range(len(data_folders)):
        found_index = data_folders[i].find(param_set)
        if found_index != -1:
            # print(i)
            data_folder_i.append(i)

    # Load data using "load_config_measurements"
    for j in range(len(data_folder_i)):
        data = load_config_measurements(data_folders[data_folder_i[j]], j+1)
        all_replicates.append(data)

    # Truncate string "param_set" to save as name for json file
    start_char = "Q"
    truncate_name = param_set[param_set.index(start_char):]

    # Write the cumulative list containing all replicates to JSON
    with open('combined_replicates/{}.json'.format(truncate_name), 'w') as outfile:
        json.dump(all_replicates, outfile)

    return None

################################## MAIN #################################
def main():
    # Test "load_config_measurements" function
    # experiment_dir = "experiments/05M_24D-16H_04M_42S/experiment0_Q0.01_W0.005_D0.05_T0.001"
    # d = load_config_measurements(experiment_dir, 1)
    # print(d["Replicate 1"]['worker_bee_concentration'])

    # All data folders: ultimately 64 x 15
    # Modify the directory to run on particular experiments directory(ies)
    data_folders = glob2.glob("experiments/*/*")
    # print(data_folders)

    # List of 64 unique sets of parameters
    # Any of the 15 folders will contain 64 sets with same names, so choose any
    sets_list = next(os.walk('experiments/06M_02D-19H_28M_49S/'))[1]
    # print(sets_list)

    # Test "combine_replicates" function using 2 sample lists above
    for k in sets_list:
        print("Combining all replicates of set: {}".format(k))
        save_lists_json = combine_replicates(data_folders, k)

    return None

main()
