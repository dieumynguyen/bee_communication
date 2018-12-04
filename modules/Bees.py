# Imports
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import scipy
from scipy import ndimage
from skimage.transform import rotate
import matplotlib.pyplot as plt

################################### CLASS: BEES #######################################

class Bee(object):
    def __init__(self, bee_type, init_position, pheromone_concentration, activation_threshold, movement, activity, bias, delta_t, delta_x, min_x, max_x, emission_period, queen_movement_params, plot_dir, rotate_bees_ON=False):
        # Class constructor method

        self.type = bee_type                            # Queen or worker
        self.rotate_bees_ON = rotate_bees_ON            # Rotating images not working yet... False for now

        self.img = ndimage.imread('imgs/queen_bee.png') if bee_type == "queen" else ndimage.imread('imgs/worker_bee.png')
        self.current_heading = 90

        self.x, self.y = init_position
        # DM added 15July2018: save local map for easier analysis
        self.local_map = []

        self.random_movement_active = activity["movement"]
        self.pheromone_active = activity["pheromone"]
        self.concentration = pheromone_concentration
        self.activation_threshold = activation_threshold

        # Movement of the bee
        self.dx, self.dy = movement

        # Set queen finding behavior params
        self.queen_directed_movement = False
        self.found_queen = False
        self.queen_movement_params = queen_movement_params
        self.found_queen_direction = False

        # DM added scenting data for each bee
        self.scenting = False

        # self.wait_threshold = int(np.random.normal(10, 1)) # wait X (10???) timesteps after finding the queen before moving
        # DM: test wait_threshold to be 4
        self.wait_threshold = 6

        self.num_timesteps_waited = 0

        # Bias is directed pheromone emission for workers
        # self.bias_x, self.bias_y = bias
        self.bias_x, self.bias_y = (0, 0)

        # Emission period
        self.emission_period = emission_period
        self.pheromone_emission_timestep = 1

        # Spatiotemporal intervals
        self.delta_t = delta_t
        self.delta_x = delta_x
        self.min_x = min_x
        self.max_x = max_x

        # History information
        self.plot_dir = plot_dir

        # Nov19
        self.reactivate_pheromone = False

### ------------------------------------------------------- ###

    def rotate_bees(self):

        # This method rotates the bees towards the queen's direction as they
        # detetct & go uphill the pheromone gradients

        try:
            # Calculate the direction bee needs to turn from its current
            # dir to head to queen
            degree_to_queen = np.arctan2(self.bias_y, self.bias_x) * 180 / np.pi

            degree_difference = self.current_heading + degree_to_queen

            # Why make it negative?
            degree_difference *= -1

            # DM commented out this test code
            # if self.type == "worker_6":
            #     print("degree_to_queen: {}".format(degree_to_queen))
            #     print("self.current_heading: {}".format(self.current_heading))
            #     print("degree_difference: {}".format(degree_difference))
            #     raw_input("")

            # Rotate the image
            self.img = rotate(self.img, degree_to_queen)

            # Update current heading
            self.current_heading = self.current_heading

        except Exception as e:
            print(e)

### ------------------------------------------------------- ###

    def update(self):

        # If pheromone active, increment emission timestep
        if self.pheromone_active:
            self.pheromone_emission_timestep += 1
            # # DM: try adding scenting data here
            # self.scenting = True

        # Check if queen has been found
        if self.found_queen_direction:
            # Check if queen-directed movement can be enabled yet
            if self.num_timesteps_waited < self.wait_threshold:
                self.num_timesteps_waited += 1

                # DM: try adding scenting data here
                self.scenting = True

            # Must reset scenting somehow to not freeze the bees
            else:
                # Waited long enough; Enable movement toward queen
                self.queen_directed_movement = True

                # DM: try adding scenting data here
                self.scenting = False

                # Set queen movement parameters
                # ========================================================================
                if self.queen_movement_params["disable_pheromone"]:
                    self.pheromone_active = False
                # ========================================================================

                # Update position to head in direction of queen
                steps = np.random.randint(1, 6)

                self.x += self.directions_to_queen["x"]*self.delta_x*steps
                self.y += self.directions_to_queen["y"]*self.delta_x*steps

            # Rotate image!
            if self.rotate_bees_ON:
                self.rotate_bees()

        # If random movement active, determine new movement behavior
        elif self.random_movement_active:
            # Pick direction, sign, and magnitude
            direction = "x" if np.random.uniform() < 0.5 else "y"
            sign = 1 if np.random.uniform() < 0.5 else -1
            steps = np.random.randint(1, 10)  # 2018-09-26 change back later to 10

            # Constrain movement to board (self.x and self.y here)
            self.__dict__[direction] += sign*self.delta_x*steps

            if self.__dict__[direction] <= self.min_x:
                self.__dict__[direction] += self.delta_x*steps

            elif self.__dict__[direction] >= self.max_x:
                self.__dict__[direction] -= self.delta_x*steps

        # Constrain x and y to bounds of space (self.min_x, self.max_x) for activated bees
        # ------------------------------------------------------------
        # DM edited 01Aug2018: + = like above so workers aren't stuck
        for dimension in ["x", "y"]:
            if self.__dict__[dimension] <= self.min_x:
                # self.__dict__[dimension] = self.min_x
                self.__dict__[dimension] += self.delta_x*2
            elif self.__dict__[dimension] >= self.max_x:
                # self.__dict__[dimension] = self.max_x
                self.__dict__[dimension] -= self.delta_x*2
        # ------------------------------------------------------------

### ------------------------------------------------------- ###

    def sense_environment(self, concentration_map, x_i, y_i):

        ### TOMORROW:
        # Try using return to see which bees freeze
        # Why are bees disappearing when they're constrained?

        # If empty local map... then walk
        # if self.found_queen:
        #     # Pick direction, sign, and magnitude
        #     direction = "x" if np.random.uniform() < 0.5 else "y"
        #     sign = 1 if np.random.uniform() < 0.5 else -1
        #     steps = 5
        #
        #     # Constrain movement to board (self.x and self.y here)
        #     self.__dict__[direction] += sign*self.delta_x*steps
        #
        #     if self.__dict__[direction] <= self.min_x:
        #         self.__dict__[direction] += self.delta_x*steps
        #
        #     elif self.__dict__[direction] >= self.max_x:
        #         self.__dict__[direction] -= self.delta_x*steps


            # return

        # Check if worker will be activated
        if not self.pheromone_active:

            if concentration_map[x_i, y_i] >= self.activation_threshold:
                self.activate_pheromones()
                self.found_queen_direction = True
                # DM added scenting data for single bees
                # self.scenting = True

        # DM indented 18July2018: emit in 1 direction for duration of scenting
        # so that bias_x and bias_y constant during that time
            # look for queen
            if not self.type == "queen":
                self.find_queen(concentration_map, x_i, y_i)

        self.update()

        # # Nov 19: try to make bees emit more than once, whenever threshold is met
        # # this works to activate workers as long as threshold is met
        # if self.found_queen_direction:
        #     if concentration_map[x_i, y_i] >= self.activation_threshold:
        #         self.pheromone_emission_timestep = 1
        #         self.num_timesteps_waited = 0
        #         self.activate_pheromones()
        #     # self.found_queen_direction = True
        #
        #     # Reset scenting
        #     # self.num_timesteps_waited = 0
        #     # self.pheromone_emission_timestep = 0
        #
        #     # print("\n {} \n".format(self.num_timesteps_waited))
        #     #
        #     if not self.type == "queen":
        #         self.find_queen(concentration_map, x_i, y_i)
        #
        #     self.update()

        # self.update()

### ------------------------------------------------------- ###

    def measure(self):
        # DM: Test emission_period

        # DM: Try distinguishing queen vs workers for these so
        # queen emits every x emission_period while workers only once
        # This works!
        emitting = False   # TESTING NOV 19
        if self.type == "queen":
            emitting = True if self.pheromone_emission_timestep % self.emission_period == 1 else False
            # test concentration map of 1 bee
            # emitting = True if self.pheromone_emission_timestep <= self.emission_period else False
        else:
            # emitting = self.pheromone_emission_timestep <= self.emission_period
            # emitting = True if self.pheromone_emission_timestep % self.emission_period == 1 else False
            if self.pheromone_emission_timestep <= self.emission_period:
                emitting = True
            # Nov20: This might've worked to make scenting multiple times
            # But msut check if movement when threshold isn't met is correct
            else: # Nov19 to control for multiple scentings... Reset when scenting is done for 1 period
                emitting = False
                self.pheromone_active = False
                self.pheromone_emission_timestep = 1
                self.num_timesteps_waited = 0

        bee_info = {
            "x"                     : self.x,
            "y"                     : self.y,
            "bias_x"                : self.bias_x,
            "bias_y"                : self.bias_y,
            "concentration"         : self.concentration,
            "emitting"              : emitting,
            "found_queen_direction" : self.found_queen_direction,
            # DM added scenting data
            "scenting"              : self.scenting,
            "type"                  : self.type,
            # DM added 15July2018: save local map
            "local_map"             : self.local_map

        }


        return bee_info

### ------------------------------------------------------- ###

    def activate_pheromones(self):
        self.pheromone_active = True
        self.random_movement_active = False
        # DM added scenting data
        # self.scenting = True

### ------------------------------------------------------- ###

    def find_queen(self, concentration_map, x_i, y_i):

        current_c = concentration_map[x_i, y_i]
        local_map = concentration_map[x_i-1:x_i+2, y_i-1:y_i+2]

        try:
            # Get the max concentration in the local map
            max_concentration = np.max(local_map[np.where(local_map > current_c)])

            # if max_concentration >= 1:
            #     print(max_concentration)

                # print(max_concentration, type(max_concentration))
            # except ValueError:
            #     # self.found_queen = True # do nothing; that's why some bees freeze at edges?
            #     # self.queen_directed_movement = True
            #     max_concentration = local_map[np.where(local_map == current_c)]
            #     print(max_concentration, type(max_concentration))

            # Get the indicies of the max concentration
            max_concentration_indices = list(np.where(local_map == max_concentration))
            max_concentration_indices = [max_concentration_indices[0][0], max_concentration_indices[1][0]]

            # print(max_concentration_indices)
            # print(max_concentration_indices[1][0])

            ########### DM 18July2018: Fix adjusted indicies ##############
            # max_concentration_indices_tup = tuple([int(index) for index in max_concentration_indices])

            # Dictionary of original indices : adjusted indices
            # mapping_dict = {
            #                 (0,0): (-1,1),
            #                 (1,0): (-1,0),
            #                 (2,0): (-1,-1),
            #                 (0,1): (0,1),
            #                 (1,1): (0,0),
            #                 (2,1): (0,-1),
            #                 (0,2): (1,1),
            #                 (1,2): (1, 0),
            #                 (2,2): (1,-1),
            #                }

            # adjusted_indices = (0,0)
            # if max_concentration_indices_tup in mapping_dict.keys():
            #     adjusted_indices =  mapping_dict[max_concentration_indices_tup]
            #     # print(adjusted_indices)

            ########### End DM's add ##############


            # Adjust the indicies to be within [-1, 1] rather than in [0, 2]
            adjusted_indices = [int(i)-1 for i in max_concentration_indices]

            # Assign directions to queen
            # DM: This only gives 4 possible directions of bias; neglects when max at either x=0 or y=0
            self.directions_to_queen = { "x" : adjusted_indices[0], "y": adjusted_indices[1] }

            # Set conditions for more accurate emission when x or y is close to 0?
            # Ex: if self.x <= 0.5, bias_direction_x = 0 and change sign of bias_direction_y


            # Update bias
            # bias_direction_x = -1 if (self.directions_to_queen["x"] > 0) else 0 if (self.directions_to_queen["x"] == 0) else 1
            # bias_direction_y = -1 if (self.directions_to_queen["y"] > 0) else 0 if (self.directions_to_queen["y"] == 0) else 1
            # DM edited 18July2018: Added conditions that if x_i or y_i near queen (300,300),
            # let them emit without angle
            if x_i <= 305 and x_i >= 295:
                    bias_direction_x = 0
            else:
                if (self.directions_to_queen["x"] > 0):
                    bias_direction_x = -1
                elif (self.directions_to_queen["x"] == 0):
                    bias_direction_x = 0
                else:
                    bias_direction_x = 1

            ### for y ###
            if y_i <= 305 and y_i >= 295:
                    bias_direction_y = 0
            else:
                if (self.directions_to_queen["y"] > 0):
                    bias_direction_y = -1
                elif (self.directions_to_queen["y"] == 0):
                    bias_direction_y = 0
                else:
                    bias_direction_y = 1

            # Vector magnitude / norm
            magn = np.sqrt(bias_direction_x**2 + bias_direction_y**2) + 1e-9

            # Define a scalar multiplier for w_x and worker_y
            # Set to 1 for now
            # 21Aug2018 - fix hardcode
            w_b = 0

            # Update bias - unit vectors
            # self.bias_x = w_b * (bias_direction_x / float(magn))
            # self.bias_y = w_b * (bias_direction_y / float(magn))

            # Turn off bias
            self.bias_x = 0
            self.bias_y = 0

            # DM: Test fixing the bias
            # self.bias_x =   0
            # self.bias_y =   (1 / np.sqrt(2))

            self.local_map = [list(ele) for ele in local_map]

        except ValueError or TypeError:
            self.found_queen = True
            self.queen_directed_movement = False


    # # Michael's edit 16July2018
    # def find_queen(self, concentration_map, x_i, y_i):
    #     current_c = concentration_map[x_i, y_i]
    #     local_map = concentration_map[x_i-1:x_i+2, y_i-1:y_i+2]
    #
    #     try:
    #         ttt = np.copy(local_map)
    #         ttt[1, 1] = 0
    #
    #         mapper = np.zeros((3, 3, 2))
    #         mapper[0,:,1] = 1
    #         mapper[1,:,1] = 0
    #         mapper[2,:,1] = -1
    #
    #         mapper[:,0,0] = -1
    #         mapper[:,1,0] = 0
    #         mapper[:,2,0] = 1
    #
    #
    #         # Get the indicies of the max concentration
    #         max_concentration_indices = np.unravel_index(ttt.argmax(), ttt.shape)
    #
    #         vector_to_queen = mapper[max_concentration_indices]
    #
    #         self.directions_to_queen = { "x" : vector_to_queen[0], "y": vector_to_queen[1] }
    #
    #         vector_away_from_queen = -vector_to_queen
    #
    #         # Define a scalar multiplier for w_x and worker_y
    #         # Set to 1 for now
    #         w_b = 1
    #
    #         # Update bias - unit vectors
    #         self.bias_x = vector_away_from_queen[0] / np.linalg.norm(vector_away_from_queen)
    #         self.bias_y = vector_away_from_queen[1] / np.linalg.norm(vector_away_from_queen)
    #
    #         self.local_map = [list(ele) for ele in local_map]
    #
    # except ValueError:
    #     self.found_queen = True
    #     self.queen_directed_movement = False


################################### CLASS: SWARM #######################################

class Swarm(object):
    def __init__(self, num_workers, queen_bee_concentration, worker_bee_concentration, worker_bee_threshold, delta_t, delta_x, min_x, max_x, emission_periods, queen_movement_params, worker_plot_dir, rotate_bees_ON, random_positions):

        WORKER_BEE_MOVEMENT = True # Michael's add 17July2018

        queen_data = {
            "init_position"             : (0, 0),       # DM: Move queen up for bias test
            "pheromone_concentration"   : queen_bee_concentration,
            "activation_threshold"      : worker_bee_threshold,
            "activity"                  : {
                "movement"  : False,
                "pheromone" : True
            },
            "movement"                  : (0.0, 0.0),
            "bias"                      : (0, 0),           # DM: Test bias on queen
            "emission_period"           : emission_periods["queen"],
            "queen_movement_params"     : queen_movement_params,
            "plot_dir"                  : None
        }

        bees = {"queen" : queen_data}

        # DM 01Aug2018: keep random positions constant across experiments for testing
        np.random.seed(10)
        if random_positions:
            # Randomly set step size for each bee, between the min and max
            # To put in corner: -2.8, -1.8
            x_position = lambda : np.random.uniform(-3, 3)
            # DM test
            # To put in corner: 1.8, 2.8
            y_position = lambda : np.random.uniform(-3, 3)

            new_position = lambda bee_i : (x_position(), y_position())
        else:
            def new_position(bee_i):
                with open("bee_positions.txt", "r") as infile:
                    bee_position_data = infile.readlines()
                bee_i_position = bee_position_data[bee_i].split(",")
                bee_i_position = [float(ele) for ele in bee_i_position]

                return bee_i_position



        temp_bias_1 = 0.25
        temp_bias_2 = np.sqrt(1 - temp_bias_1**2)
        temp_bias = (temp_bias_1, temp_bias_2)

        get_worker_data = lambda bee_i : {
            "init_position"             : (new_position(bee_i)),
            "pheromone_concentration"   : worker_bee_concentration,
            "activation_threshold"      : worker_bee_threshold,
            "activity"                  : {
                "movement"  : WORKER_BEE_MOVEMENT,
                "pheromone" : False
            },
            "movement"                  : (0.001, 0.001),
            # "bias"                      : temp_bias,
            "bias"                      : (0, 0),
            "emission_period"           : emission_periods["worker"],
            "queen_movement_params"     : queen_movement_params,
            "plot_dir"                  : "{}/worker_{}".format(worker_plot_dir, bee_i),
            "rotate_bees_ON"            : rotate_bees_ON
        }

        worker_bees = {"worker_{}".format(i+1) : get_worker_data(i) for i in range(num_workers)}

        for worker_bee, worker_bee_info in worker_bees.items():
            bees[worker_bee] = worker_bee_info

        self.bees = []
        for bee, bee_info in bees.items():
            bee_info["bee_type"] = bee
            bee_info["delta_t"] = delta_t
            bee_info["delta_x"] = delta_x
            bee_info["min_x"] = min_x
            bee_info["max_x"] = max_x

            self.bees.append(Bee(**bee_info))
