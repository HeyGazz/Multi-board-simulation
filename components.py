import random
from power_temp_simulation.power_temp_simulation import PowerTemperatureSimulator

SIM_TIME = 0.0


class CPU:
    def __init__(self, _id, _random, status=0):
        # GENERIC PARAMETERS
        self.delta_time_change_status = 10.

        # CPU SPECIFIC PARAMETERS
        self.id = _id
        self.status = status
        self.working_time = 0.0

        # TASK SPECIFIC PARAMETERS
        self.is_busy = False
        self.current_task = None
        self.task_time = 0.0
        self.task_start_time = 0.0

        # POWER TEMPERATURE SPECIFIC PARAMETERS
        self.temperature = 0
        self.power = 0

        self.power_temp_sim = PowerTemperatureSimulator(random=_random)
        self.power_temp_sim.set_level(self.status)

    def assign_task(self, task):
        if not self.is_busy:
            self.is_busy = True
            self.current_task = task
            self.execute_task()

    def execute_task(self):
        self.task_start_time = SIM_TIME
        self.task_time = self.current_task.execute() + SIM_TIME

    def change_status(self, val):
        self.status = val
        self.power_temp_sim.set_level(self.status)

    def simulate_params(self):
        self.power, self.temperature = self.power_temp_sim.value_at(1)

    def prob_to_change_status(self):
        # Dividing the working_time in chunks, each one correspond to the status time interval
        int_value = int(self.working_time / self.delta_time_change_status)
        if int_value > self.status:
            # Get the decimal part, used as probability score
            prob = (self.working_time / self.delta_time_change_status) - int_value
            if random.random() < prob:
                self.change_status(int_value)

    def update(self):

        # Simulate temperature and power consumption
        self.simulate_params()

        # If the cpu is working increase working time
        # and check eventually status changes
        if SIM_TIME < self.task_time:
            self.working_time = SIM_TIME - self.task_start_time
            self.prob_to_change_status()
            return

        # FREE THE CPU
        self.is_busy = False
        self.current_task = None
        self.task_time = 0.0
        # print(f"{SIM_TIME:.3f} - {self.status()}")


    def get_param_info(self)->str:
        return f"|JID:{self.current_task} |T:{self.temperature:.3f} |W:{self.power:.3f} |S:{self.status} |"

    def __str__(self):
        if self.is_busy:
            return f"CPU[{self.id}:.] > {self.current_task.id}"
        return f"CPU[{self.id}] > -1"


class Task:
    def __init__(self, _id, base_execution_time=0.0, std=0.0, is_periodic=False):
        self.id = _id
        self.base_execution_time = base_execution_time
        self.std = std
        self.is_periodic = is_periodic

    def execute(self):
        execution_time = self.base_execution_time + abs(random.gauss(self.base_execution_time, self.std))
        # print(f"Task {self.id} is being executed for {execution_time:.3f} seconds.")
        return execution_time


class Board:
    def __init__(self, _id, num_cpus, _random):
        self.id = _id
        self.cpus = [CPU(i, _random) for i in range(num_cpus)]

    def assign_task(self, task):
        for idx, t in enumerate(task):
            if t is not None:
                self.cpus[idx].assign_task(t)

    def update(self):
        for cpu in self.cpus:
            cpu.update()

    def self_report(self):
        string_output = f"Board[ {self.id} ]"
        for cpu in self.cpus:
            string_output += f"\t|\t"
            string_output += cpu.__str__()
        string_output += "\t||"
        return string_output


class Network:
    def __init__(self, num_boards, num_cpus, _random):
        self.boards = [Board(idx, num_cpus, _random) for idx in range(num_boards)]

    def update(self):
        for board in self.boards:
            board.update()

    def interact(self, data=None):
        if data is not None:
            for idx, board in enumerate(self.boards):
                board.assign_task(data.get(idx))
        else:
            output_string = list()
            for board in self.boards:
                output_string.append(board.self_report())
            return output_string
