import numpy as np

from components import *
from simulation import *


def custom_print(text):
    formatted_time = f"{components.SIM_TIME:.2f}"
    print(f"t[s]: {formatted_time:03}" + " " * (8 - len(formatted_time)), end='\t')
    print(*text)


def simulation_one_board_test(_params):
    # Create tasks
    task_params = _params.get("task")
    list_tasks = [Task(idx,
                  base_execution_time=task_params.get(idx)['base_execution_time'],
                  std=task_params.get(idx)['std'],
                  is_periodic=task_params.get(idx)['periodic']) for idx in task_params.keys()]

    # task_A = Task(0,
    #               base_execution_time=task_params.get(0)['base_execution_time'],
    #               std=2,
    #               is_periodic=True)
    # task_B = Task(1, base_execution_time=5, std=0.5)
    # task_C = Task(2, base_execution_time=10, std=2, is_periodic=True)
    # task_D = Task(3, base_execution_time=5, std=0.5)

    # Create Network
    num_boards = _params.get("num_boards")
    num_cpus = _params.get("num_cpus")
    net = Network(num_boards=num_boards, num_cpus=num_cpus, _random=random, _params=_params)

    # Create Simulation
    sim = Simulation(_object=net, delta_time=_params.get('delta_time'))

    data = {0: [list_tasks[0], list_tasks[2], list_tasks[1], list_tasks[0]]}

    print(f"*** EXPERIMENT 1 - assign tasks, simulate for 30 seconds")

    sim.interact_with_object(data, is_assign_task=True)
    for _ in range(30):
        network_status, debug_text = sim.interact_with_object(is_get_data=True)
        custom_print(debug_text)
        sim.running_simulation(time_interval=1.0)

    print()
    print(f"*** EXPERIMENT 2 - assign task NULL to second cpu, simulate for 40 seconds")
    data = {
        0: [None],
        # 1: [task_B, task_B]
    }

    sim.interact_with_object(data, is_assign_task=True)
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
            "delta_time": 0.5,
            "num_boards": 1,
            "num_cpus": 4,
            "cpu": {
                "time_change_status": 10.,
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
