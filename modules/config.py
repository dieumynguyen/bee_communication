RANDOM_SEED = 42

TESTING = False      # Testing with one set of parameters
PLOTTING_ON = False
REAL_TIME_VISUALIZATION = False

THREADING_ON = True
NUM_ITERATIONS_PER_EXPERIMENTAL_CONDITION = 1 # Ideally, 10

NUM_WORKERS = 50
RANDOM_BEE_POSITIONS = True # If False, reads from bee_positions.txt

CONDITION_COUNTS = {
    "queen"                     : 1,
    "worker_concentration"      : 1,
    "worker_threshold"          : 1,
    "diffusion_coefficient"     : 1
}

THREADS = []
SECONDS_TO_RUN = 16 # doubled from 8
DELTA_T = 0.05
DELTA_X = 0.01
MIN_X = -3
MAX_X = 3
w_b = 1

ROTATE_BEES_ON = False
DIFFUSION_COEFFICIENT = 0.5 # Used for TESTING
QUEEN_EMISSION_PERIOD = 6
WORKER_EMISSION_PERIOD = 6
WORKER_BEE_THRESHOLD = 0.001
DISABLE_PHEROMONE_ON_WORKER_MOVEMENT = True
