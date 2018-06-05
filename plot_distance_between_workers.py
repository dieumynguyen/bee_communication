# Imports
import json
import numpy as np
import plotly.plotly as py
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import cycler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import os
import glob2
import re

########################################################################
# STYLESHEET

plt.style.use('seaborn-white')

plt.rcParams['font.sans-serif'] = "Tahoma"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.labelweight'] = 'normal'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['lines.linewidth'] = 3
params = {"ytick.color" : "#535956",
          "xtick.color" : "#535956",
          "axes.labelcolor" : "#535956",
          "axes.edgecolor" : "#535956",
          "text.color": "#535956"}
plt.rcParams.update(params)

########################################################################

def get_data_1_bee(data, replicate_i, bee_start_i):
    # Loop over 50 lists in 1 timestep
    # Each list is 1 bee and its distance to 49 other bees at this timestep
    # List of 160 lists, each list has 50 values
    one_bee_160_t = []

    # Loop over 160 timesteps here
    number_of_distances = len(data[0]["Replicate 1"]["distance_from_others"])

    for bee in range(bee_start_i, number_of_distances, 51):
        dist_to_49_others = data[replicate_i]["Replicate {}".format(replicate_i+1)]["distance_from_others"][bee]["distances"]
        one_bee_160_t.append(dist_to_49_others)

    return one_bee_160_t

########################################################################

def get_avg_neighbor_distances(data_list):
    # Loop over each timestep list
    # List of 160 floats for 1 bee's average distance from neighbors over time
    nearest_neighbors = []

    for t_list in data_list:
        # 160 avg values for distance to nearest neighbors
        # Threshold nearest neighbors at max = 2 distance units
        avg_list = []
        for val in t_list:
            if val <= 2:
                avg_list.append(val)
                # print(val)
        nearest_neighbors.append(np.mean(avg_list))

    return nearest_neighbors


########################################################################
''' Use get_data_1_bee & get_avg_neighbor_distances to get 50 lists for 50 bees
-- in 1 replicate -- later average over all replicates '''

def get_distances_50_bees(data, replicate_i):
    # List of 50 lists
    neighbor_distances_all_bees = []

    for i in range(51):
        # print(i)
        one_bee = get_data_1_bee(data, replicate_i, i)
        avg_distances = get_avg_neighbor_distances(one_bee)
        neighbor_distances_all_bees.append(avg_distances)

    return neighbor_distances_all_bees


def all_bees_all_time(data, replicate_i):
    ''' For 1 replicate swarm, get list of all bees avg distance
    from nearest neighbors over all 160 timesteps '''

    # Avg over all 50 bees for each of 160 timesteps
    # Get a list of 160 values
    all_distances = get_distances_50_bees(data, replicate_i)

    all_bees_over_time = []
    for i in range(160):
        # For each timestep, i, get values of each of the 50 bees at that i
        one_t = [item[i] for item in all_distances]
        # Get the avg of of all bees at the timestep
        avg_all_bees = np.mean(one_t)
        all_bees_over_time.append(avg_all_bees)

    return all_bees_over_time

########################################################################

def avg_all_replicates(data_json):
    # Get all replicates' lists into a list
    all_replicates = []
    for i in range(len(data_json)):
        one_replicate_data = all_bees_all_time(data_json, i)
        all_replicates.append(one_replicate_data)

    # Store means of 10 replicates
    all_reps_avgs = []

    # Also get min and max for range in plotting
    mins = np.min(all_replicates, axis=0)
    maxs = np.max(all_replicates, axis=0)

    data = {
        "all" : all_replicates,
        "min" : mins,
        "max" : maxs
    }

    return data

########################################################################

def plot_me(data_json):

    with open("combined_replicates/" + data_json, "r") as f:
        json_data = json.load(f)

    bee_data = avg_all_replicates(json_data)

    fig, ax = plt.subplots(1, figsize=(8, 5))
    sns.set(font_scale = 1.5)
    sns.set_style("whitegrid", {'axes.grid' : False})

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # sns.set_style("whitegrid")

    # Setup minmax bounds
    ax.plot(bee_data["min"], color='#2c7fb8', alpha=0.2)
    ax.plot(bee_data["max"], color='#2c7fb8', alpha=0.2)

    # Fill between minmax bounds
    ax.fill_between([i for i in range(len(bee_data["min"]))], bee_data["min"], bee_data["max"],
                    where = bee_data["max"] >= bee_data["min"], facecolor='#2c7fb8', alpha=0.15, interpolate=True)

    # Average with stds 68 and 95
    g = sns.tsplot(data=bee_data["all"], estimator=np.mean, color="#2eaf53", alpha=0.8, ci=[68, 95], ax=ax, err_kws={"color" : "#a1dab4", "alpha" : 0.})
    g.lines[2].set_linewidth(3)
    g.set(ylim=(0,2))

    ax.set(xlabel='Time', ylabel='Distance')
    plt.title("Distance between workers over time \n (Q0.15_W0.4_D0.35_T0.4_wb1)")
    plt.savefig('figures/distance_to_workers/Q0.15_W0.4_D0.35_T0.4_wb1.pdf')

    return None

########################################################################

def main():

    json_file = "Q0.15_W0.4_D0.2_T0.005_wb1.json"
    plot_me(json_file)


if __name__ == '__main__':
    main()
