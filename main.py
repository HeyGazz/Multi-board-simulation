import numpy as np

from components import *
from simulation import *


NO_CHANGE = 0

def custom_print(text):
    formatted_time = f"{components.SIM_TIME:.2f}"
    print(f"t[s]: {formatted_time:03}" + " " * (8 - len(formatted_time)), end='\t')
    print(*text)


# USE IT AS A EXAMPLE
def simulation_one_board_test(_params):
    # Create tasks
    task_params = _params.get("task")
    list_tasks = [Task(idx,
                       base_execution_time=task_params.get(idx)['base_execution_time'],
                       std=task_params.get(idx)['std'],
                       is_periodic=task_params.get(idx)['periodic']) for idx in task_params.keys()]

    # Create Network
    num_boards = _params.get("num_boards")
    num_cpus = _params.get("num_cpus")
    net = Network(num_boards=num_boards, num_cpus=num_cpus, _random=random, _params=_params)

    # Create Simulation
    sim = Simulation(_object=net, delta_time=_params.get('delta_time'))

    print(f"*** EXPERIMENT 1 - assign tasks, simulate for 30 seconds")
    # CREATE dictionary for assign task
    # The dictionary is composed as follow:
    #   key: id board
    #   value: list of tasks to assign (NB use None to not assign a task to a cpu)

    # DEFAULT DATA
    data = {key: [None for _ in range(num_cpus)] for key in range(num_boards)}

    data[0] = [list_tasks[0], list_tasks[2], list_tasks[1], list_tasks[0]]

    # ASSIGN TASK
    sim.interact_with_object(data, is_assign_task=True)
    # Iterate for 30 times:
    for _ in range(30):
        # GET Data from cpus
        network_status, debug_text = sim.interact_with_object(is_get_data=True)
        # PRINT the status (OPTIONAL, debugging purpose)
        custom_print(debug_text)
        # SIMULATE THE NETWORK FOR 1 [virtual] seconds, with delta_time set as 0.5 the function will make 2 steps
        # in the simulation
        sim.running_simulation(time_interval=1.0)
    # In total the simulation will make 60 steps for a total of 30 [virtual] seconds

    # THE PREVIOUS LINE CAN BE REWRITTEN LIKE THIS:
    # sim.interact_with_object(data, is_assign_task=True)
    # network_status, debug_text = sim.interact_with_object(is_get_data=True)
    # custom_print(debug_text)
    # sim.running_simulation(time_interval=30.0)
    # network_status, debug_text = sim.interact_with_object(is_get_data=True)
    # BUT YOU WILL GET THE DATA FROM THE NETWORK ONLY AT THE BEGINNING AND AFTER 60 STEPS

    print()
    print(f"*** EXPERIMENT 2 - assign task NULL (STOP EXECUTION) to third cpu, simulate for 40 seconds")
    data[0] = [NO_CHANGE, NO_CHANGE, None]

    sim.interact_with_object(data, is_assign_task=True, is_fault=True)
    for _ in range(40):
        network_status, debug_text = sim.interact_with_object(is_get_data=True)
        custom_print(debug_text)
        sim.running_simulation(time_interval=1.0)

    print()
    print(f"*** EXPERIMENT 3 - assign status 3 to cpus, simulate for 0.5 seconds")

    data = {
        0: [3 for _ in range(num_cpus)],
    }

    sim.interact_with_object(data, is_fault=True)
    for _ in range(1):
        network_status, debug_text = sim.interact_with_object(is_get_data=True)
        custom_print(debug_text)
        sim.running_simulation(time_interval=0.5)

    print()
    print(f"*** SIMULATION ENDED")


if __name__ == '__main__':
    random = np.random.RandomState(1234)

    params = \
        {
            "delta_time": 0.5,  # Time interval between steps in the simulation
            "num_boards": 1,
            "num_cpus": 4,
            "cpu": {
                "time_change_status": 10.,  # Time interval to start to change statu when the cpu is running
                "status": 0,
                "temperature": 45.0,
                "power": 12.0
            },
            "task": {
                0: {
                    "base_execution_time": 10.0,
                    "std": 0.5,
                    "periodic": True
                },
                1: {
                    "base_execution_time": 7.0,
                    "std": 0.2,
                    "periodic": True
                },
                2: {
                    "base_execution_time": 5.0,
                    "std": 0.1,
                    "periodic": False
                },
                3: {
                    "base_execution_time": 3.0,
                    "std": 0.08,
                    "periodic": False
                }
            }
        }

    simulation_one_board_test(params)
