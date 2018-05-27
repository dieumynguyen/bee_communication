# %load plot_distances.py
# Imports
import json
import numpy as np
import plotly.plotly as py
import matplotlib as mpl
from matplotlib import cycler
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import os
import glob2
import re
# from wand.image import Image as WImage


############################# STYLESHEET ###############################

plt.style.use('seaborn-white')

plt.rcParams['font.sans-serif'] = "Tahoma"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.labelweight'] = 'normal'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['lines.linewidth'] = 3
params = {"ytick.color" : "#535956",
          "xtick.color" : "#535956",
          "axes.labelcolor" : "#535956",
          "axes.edgecolor" : "#535956",
          "text.color": "#535956"}
plt.rcParams.update(params)

########################################################################

def standardize_filenames(fname, start_char):
    fig_name = fname[20:fname.index(start_char)-1]
    split_list = fig_name.split("_")
    # print(split_list)

    new_name = ""
    for i in range(len(split_list)):
        if len(split_list[i][1:]) > 5:
            if int(split_list[i][6]) <= 5:
                round_down = split_list[i][1:6]
                new_name += split_list[i][0] + round_down + "_"
                # print(round_down)
            else:
                round_up = str(float(split_list[i][1:6]) + 0.001)
                new_name += split_list[i][0] + round_up + "_"
                # print(round_up)

        else:
            new_name += split_list[i] + "_"

    # print(new_name)

    if new_name[-1] == "_":
        new_name = new_name[:-1]

    # print(new_name)

    return new_name

########################################################################

def plot_avg_distances(data_json):

    ''' For each replicate in a set of parameters, open that cumulative
    JSON and plot each replicate as a line in a single plot.
    '''

    with open("avg_distance_data/" + data_json, "r") as f:
        data = json.load(f)

    fig = plt.figure()
    ax = plt.axes()

    # Standardize file names
    fname = f.name
    start_char = "j"
    fig_name = standardize_filenames(fname, start_char)

    # Plotting
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for i, d in enumerate(data):
        ax.plot(d, label='Swarm {}'.format(i+1))

        plt.xlim(0, 160)
        plt.ylim(0, 5)

        plt.legend(bbox_to_anchor=(1,0.5), loc="center left")

        plt.xlabel('Time (step)')
        plt.ylabel('Average distance to queen')
        plt.title('{}'.format(fig_name))

        plt.tight_layout()
        plt.savefig("figures/distance_to_queen/{}.pdf".format(fig_name), transparent=True)

    plt.close()

########################################################################

def main():

    # Iterate through all (256) JSON's and produce 1 figure each
    reps_list = list(map(lambda x : x.split("/")[-1], glob2.glob("avg_distance_data/Q0.5_W0.005_D0.5_T0.001.json")))

    for i, r in enumerate(reps_list):
        print("{}. Plotting average distance to queen for: {}".format(i+1, r))
        plot_avg_distances(r)

main()
