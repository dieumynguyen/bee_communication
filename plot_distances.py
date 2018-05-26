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


############################# STYLESHEET ###############################

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

def plot_avg_distances(data_json):

    ''' For each replicate in a set of parameters, open that cumulative
    JSON and plot each replicate as a line in a single plot.
    '''

    with open("avg_distance_data/" + data_json, "r") as f:
        data = json.load(f)

    fig = plt.figure(figsize=(6,4))
    ax = plt.axes()

    start_char = "j"
    filename = f.name
    fig_name = filename[18:filename.index(start_char)]

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for i, d in enumerate(data):
        ax.plot(d, label='Swarm {}'.format(i+1))

        plt.xlim(0, 160)
        plt.ylim(0, 5)

        plt.legend()

        plt.xlabel('Time (step)')
        plt.ylabel('Average distance to queen')
        plt.title('{}'.format(fig_name[:-1]))

        plt.tight_layout()
        plt.savefig("figures/distance_to_queen/{}pdf".format(fig_name), transparent=True)

    plt.close()

########################################################################

def main():
    # Iterate through all (256) JSON's and produce 1 figure each
    reps_list = list(map(lambda x : x.split("/")[-1], glob2.glob("combined_replicates/*")))

    for r in reps_list:
        print("Plotting average distance to queen for: {}".format(r))
        plot_avg_distances(r)

main()
