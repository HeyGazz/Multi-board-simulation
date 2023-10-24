import numpy as np

from components import *
from simulation import *


def custom_print(text):
    formatted_time = f"{components.SIM_TIME:.2f}"
    print(f"t[s]: {formatted_time:03}" + " " * (8-len(formatted_time)), end='\t')
    print(*text)


def simulation_one_board_test(num_cpus=2):

    # Create tasks
    task_A = Task(0, base_execution_time=10, std=2, is_periodic=True)
    task_B = Task(1, base_execution_time=5, std=0.5)

    # Create Network
    net = Network(num_boards=1, num_cpus=num_cpus, _random=random)

    # Create Simulation
    sim = Simulation(_object=net, delta_time=0.5)

    data = {0: [task_A, task_B]}

    print(f"*** EXPERIMENT 1 - assign task {task_A.id} and {task_B.id}, simulate for 30 seconds")

    sim.interact_with_object(data)
    for _ in range(30):
        custom_print(sim.interact_with_object())
        sim.running_simulation(time_interval=1.0)

    print()
    print(f"*** EXPERIMENT 2 - assign task NULL to second board, simulate for 40 seconds")
    data = {
        0: [None],
        # 1: [task_B, task_B]
    }

    sim.interact_with_object(data)
    for _ in range(40):
        custom_print(sim.interact_with_object())
        sim.running_simulation(time_interval=1.0)

    print()
    print(f"*** SIMULATION ENDED")


if __name__ == '__main__':
    random = np.random.RandomState(1234)

    simulation_one_board_test()


