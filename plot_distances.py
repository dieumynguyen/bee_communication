# Imports
import json
import numpy as np
import plotly.plotly as py
import matplotlib as mpl
from matplotlib import cycler
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

def plot_avg_distances(dataset):

    ''' For each replicate in a set of parameters, open that cumulative
    JSON and plot each replicate as a line in a single plot.
    '''

    with open("combined_replicates_test/" + dataset, "r") as f:
        data = json.load(f)

    start_char = "j"
    filename = f.name
    fig_name = filename[20:filename.index(start_char)]

    fig = plt.figure(figsize=(6,4))
    ax = plt.axes()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for i in range(len(data)):
        average_distances = []
        for l in range(160):
            avg = data[i]['Replicate {}'.format(i+1)]['distance_from_queen'][l]['average']
            average_distances.append(avg)


        # Plot the line onto the same figure as other lines
        ax.plot(average_distances, label='Swarm {}'.format(i+1))

        plt.xlim(0, 160)
        plt.ylim(0, 5)

        plt.legend()

        plt.xlabel('Time (step)')
        plt.ylabel('Average distance to queen')
        plt.title('{}'.format(fig_name[:-1]))

        plt.tight_layout()
        plt.savefig("figures_test/distance_to_queen/{}pdf".format(fig_name), transparent=True)

########################################################################

def main():
    # Test above function
    # plot_avg_distances("Q0.01_W0.005_D0.05_T0.001.json")

    # Iterate through all (256) JSON's and produce 1 figure each
    reps_list = list(map(lambda x : x.split("/")[-1], glob2.glob("combined_replicates_test/*")))

    for r in reps_list:
        print("Plotting average distance to queen for: {}".format(r))
        plot_avg_distances(r)

main()
