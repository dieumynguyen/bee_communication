# Combine data of interest of 10 replicates of a single set of parameters
# into a single json file for further analysis

########################################################################

# Imports
import json
import numpy as np
import plotly.plotly as py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
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

    # Load config.json
    with open(experiment_dir + "/config.json", "r") as f:
        config_dict = json.load(f)

    # Pull out params of interest from config.json
    D = config_dict['diffusion_coefficient']
    Q = config_dict['swarm_parameters']['queen_bee_concentration']
    W = config_dict['swarm_parameters']['worker_bee_concentration']
    T = config_dict['swarm_parameters']['worker_bee_threshold']

    # Load measurements.json
    with open(experiment_dir + "/data/measurements.json", "r") as f:
        measurements = json.load(f)

    # Pull out params of interest from measurements.json
    distance_from_queen = measurements['distance_from_queen']
    distance_from_others = measurements['distance_from_others']

    # Create dict
    parameters = ['diffusion_coefficient', 'queen_bee_concentration',
         'worker_bee_concentration', 'worker_bee_threshold',
         'distance_from_queen', 'distance_from_others']
    values = [D, Q, W, T, distance_from_queen, distance_from_others]
    experiment_dict = dict(zip([p for p in parameters], values))
    outer_dict = {"Replicate {}".format(replicate_i) : experiment_dict}

    return outer_dict

########################################################################




def main():
    # Test "load_config_measurements" function
    experiment_dir = "experiments/05M_24D-13H_48M_06S/experiment0_Q0.01_W0.005_D0.05_T0.001"
    d = load_config_measurements(experiment_dir, 1)
    d["Replicate 1"]['queen_bee_concentration']

    return None
