import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import time
import os
import datetime
import json
import numpy as np
import threading

from modules.Environment import Environment
from modules.Bees import Swarm
from modules.config import *
import modules.utils as utils

def init_factors():
    # Setup parameters for model

    global queen_bee_concentrations
    # queen_bee_concentrations = np.linspace(0.01, 0.5, CONDITION_COUNTS["queen"])
    queen_bee_concentrations = [0.15]

    global worker_bee_concentrations
    # worker_bee_concentrations = np.linspace(0.005, 0.4, CONDITION_COUNTS["worker_concentration"])
    # worker_bee_concentrations = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.5]
    worker_bee_concentrations = [0.5]

    global diffusion_coefficients
    # diffusion_coefficients = np.linspace(0.05, 0.5, CONDITION_COUNTS["diffusion_coefficient"])
    # diffusion_coefficients = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55]
    diffusion_coefficients = [0.55]

    global worker_bee_thresholds
    # worker_bee_thresholds = np.linspace(0.005, 0.5, CONDITION_COUNTS["worker_threshold"])
    worker_bee_thresholds = [0.005, 0.5]

##################################################################################################

def run_experiment(run_event, experiment_i, Q, W, D, T, wb, experiment_iteration, experiment_dir, queen_bee_params, worker_bee_params, diffusion_coefficient, spatiotemporal_parameters):

    # Make directories

    dirs = utils.make_directories(experiment_dir, experiment_i, Q, W, D, T, wb, experiment_iteration, worker_bee_params["number"])
    experiment_dir_path = dirs[0]
    data_dir_path = dirs[1]
    if PLOTTING_ON:
        plots_dir_path = dirs[3]
        env_plots_dir_path = dirs[4]
    else:
        plots_dir_path = ""
        env_plots_dir_path = ""

    # ---------------------------------------------------------------------------

    # Set up swarm & plot parameters

    swarm_parameters = {
        "queen_bee_concentration"   : queen_bee_params["concentration"],
        "worker_bee_concentration"  : worker_bee_params["concentration"],
        "worker_bee_threshold"      : worker_bee_params["threshold"],
        "num_workers"               : worker_bee_params["number"],
        "delta_t"                   : spatiotemporal_parameters["temporal"]["delta_t"],
        "delta_x"                   : spatiotemporal_parameters["spatial"]["delta_x"],
        "min_x"                     : spatiotemporal_parameters["spatial"]["min_x"],
        "max_x"                     : spatiotemporal_parameters["spatial"]["max_x"],
        # "w_b"                       : spatiotemporal_parameters["spatial"]["w_b"],
        "emission_periods"          : {
            "queen"     : queen_bee_params["emission_period"],
            "worker"    : worker_bee_params["emission_period"]
        },
        "queen_movement_params"     : {
            "disable_pheromone" : worker_bee_params["disable_pheromone"]
        },
        "worker_plot_dir"           : plots_dir_path,
        "rotate_bees_ON"            : ROTATE_BEES_ON,
        "random_positions"          : RANDOM_BEE_POSITIONS
    }

    plot_params = {
        "display_real_img"  : True,
        "save_dir"          : env_plots_dir_path
    }

    # ---------------------------------------------------------------------------

    # Save parameters

    config_save_path = "{}/config.json".format(experiment_dir_path)
    save_params = {
        "swarm_parameters"          : swarm_parameters,
        "diffusion_coefficient"     : diffusion_coefficient,
        "spatiotemporal_parameters" : spatiotemporal_parameters
    }
    with open(config_save_path, "w") as outfile:
        json.dump(save_params, outfile)

    # ---------------------------------------------------------------------------

    # Pass in dict of swam parameters (**kwargs) into Swarm module
    # Pass in environment parameters

    swarm = Swarm(**swarm_parameters)
    env = Environment(swarm.bees, diffusion_coefficient, spatiotemporal_parameters, plot_params, data_dir_path, REAL_TIME_VISUALIZATION, PLOTTING_ON)
    env.run(run_event)

##################################################################################################

def main(run_event):

    spatiotemporal_parameters = {
        "spatial"   : {
            "min_x"     : MIN_X,
            "max_x"     : MAX_X,
            "delta_x"   : DELTA_X,
            #"w_b"       : w_b
        },
        "temporal"  : {
            "start_t"   : 0,
            "finish_t"  : SECONDS_TO_RUN,
            "delta_t"   : DELTA_T
        }
    }

    # -----------------------------------------------------------------------------

    # Directory for current experiment

    experiment_timestamp = datetime.datetime.now().strftime("%mM_%dD-%HH_%MM_%SS")
    experiment_dir = "experiments/{}".format(experiment_timestamp)
    if not os.path.exists(experiment_dir):
        os.mkdir(experiment_dir)

    # -----------------------------------------------------------------------------

    # Testing conditions: 1 set of parameters

    ''' Run tests:
    1. 50 workers with Q = 0.15, W = 0.05, D = 0.3, T = 0.005
    2. Work with h5 files to see if needed: Save data on # scenting bees, concentration in arena, positions of bees
    '''

    if TESTING:
        queen_bee_params = {
            "concentration"     : 0.15,
            "emission_period"   : 6
        }

        worker_bee_params = {
            "number"            : 50,
            "concentration"     : 0.005,
            "threshold"         : 0.02,
            "emission_period"   : 6,
            "disable_pheromone" : True
        }

        experiment_params = {
            "run_event"                 : run_event,
            "experiment_i"              : 1,
            "experiment_iteration"      : 0,
            "experiment_dir"            : experiment_dir,
            "queen_bee_params"          : queen_bee_params,
            "worker_bee_params"         : worker_bee_params,
            "diffusion_coefficient"     : 0.5,
            "spatiotemporal_parameters" : spatiotemporal_parameters,
            "Q"                         : 0.15,
            "W"                         : 0.005,
            "D"                         : 0.5,
            "T"                         : 0.02,
            "wb"                        : 1,
        }
        run_experiment(**experiment_params)     # pass in dict of parameters

    # Non-test: give parameters from config.py & here

    else:
        # Number of experiments as product of different parameters' sets
        num_experiments = len(queen_bee_concentrations) * len(worker_bee_concentrations) * len(diffusion_coefficients) * len(worker_bee_thresholds) * NUM_ITERATIONS_PER_EXPERIMENTAL_CONDITION

        # Create dicts of different parameters by looping through each combo
        experiment_i = 0

        # DM added variables for labeling experiments with parameters
        Q = 0
        W = 0
        D = 0
        T = 0
        wb = 1
        # End DM's adds

        for queen_bee_concentration in queen_bee_concentrations:
            Q = queen_bee_concentration           # DM
            for worker_bee_concentration in worker_bee_concentrations:
                W = worker_bee_concentration      # DM
                for diffusion_coefficient in diffusion_coefficients:
                    D = diffusion_coefficient     # DM
                    for worker_bee_threshold in worker_bee_thresholds:
                        T = worker_bee_threshold  # DM
                        for experiment_condition_iteration in range(NUM_ITERATIONS_PER_EXPERIMENTAL_CONDITION):

                            if not run_event.is_set():
                                return
                            queen_bee_params = {
                                "concentration"     : queen_bee_concentration,
                                "emission_period"   : QUEEN_EMISSION_PERIOD
                            }

                            worker_bee_params = {
                                "number"            : NUM_WORKERS,
                                "concentration"     : worker_bee_concentration,
                                "threshold"         : worker_bee_threshold,
                                "emission_period"   : WORKER_EMISSION_PERIOD,
                                "disable_pheromone" : DISABLE_PHEROMONE_ON_WORKER_MOVEMENT
                            }

                            experiment_params = {
                                "run_event"                 : run_event,
                                "experiment_i"              : experiment_i,
                                "Q"                         : Q,
                                "W"                         : W,
                                "D"                         : D,
                                "T"                         : T,
                                "wb"                        : wb,
                                "experiment_iteration"      : experiment_condition_iteration,
                                "experiment_dir"            : experiment_dir,
                                "queen_bee_params"          : queen_bee_params,
                                "worker_bee_params"         : worker_bee_params,
                                "diffusion_coefficient"     : diffusion_coefficient,
                                "spatiotemporal_parameters" : spatiotemporal_parameters
                            }

                            print_string = "\n\nExperiment {}/{} - iteration {} --- Queen Concentration: {} -- Worker Concentration: {} -- Diffussion Coefficient: {} -- Worker Bee Threshold: {}".format(experiment_i+1, num_experiments, experiment_condition_iteration, queen_bee_concentration, worker_bee_concentration, diffusion_coefficient, worker_bee_threshold)

                            if THREADING_ON:
                                print("Creating thread for {}".format(print_string))
                                experiment_thread = threading.Thread(target=run_experiment, kwargs=experiment_params)
                                THREADS.append(experiment_thread)
                            else:
                                print(print_string)
                                run_experiment(**experiment_params)

                        experiment_i += 1

        if THREADING_ON:
            for thread in THREADS:
                thread.start()

##################################################################################################

if __name__ == '__main__':
    np.random.seed(seed=RANDOM_SEED)

    init_factors()

    running = threading.Event()
    running.set()

    main_thread = threading.Thread(target=main, args=(running,))
    main_thread.start()

    try:
        while True:
            if utils.check_all_threads_finished():
                main_thread.join()
                break
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Attempting to close threads...")
        running.clear()
        for thread in THREADS:
            thread.join()

        main_thread.join()

        print("Threads successfully closed.")
