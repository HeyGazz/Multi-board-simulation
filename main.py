from components import *
from simulation import *


def custom_print(text):
    print(f"t: {components.SIM_TIME:.2f}"+" "*10, end='\t')
    print(*text)


if __name__ == '__main__':
    # Create tasks
    task_A = Task(0, base_execution_time=10, std=2)
    task_B = Task(1, base_execution_time=5, std=0.5)

    # Create Network
    net = Network(num_boards=2, num_cpus=2)

    # Create Simulation
    sim = Simulation(object=net, delta_time=0.5)

    data = {0: [task_A, task_B],
            1: [task_B, task_B]}

    sim.interact_with_object(data)
    sim.running_simulation(time_interval=7.0)

    custom_print(sim.interact_with_object())
    sim.running_simulation(time_interval=7.0)

    custom_print(sim.interact_with_object())
    sim.running_simulation(time_interval=14.0)

    custom_print(sim.interact_with_object())


    #
    # # Create boards
    # boards = [Board(0, num_cpus=2)]
    #
    # time_simulation = 0.0  # Seconds
    # delta_time = 0.2
    # simulation_running = True
    #
    # boards[0].assign_task([task_A, task_B])
    #
    # while components.SIM_TIME < 20.:
    #     print(f"{components.SIM_TIME:.1f}", end='\t')
    #     for board in boards:
    #         board.update()
    #         print(*board.self_report(), end='| ')
    #     print("")
    #     components.SIM_TIME += delta_time

