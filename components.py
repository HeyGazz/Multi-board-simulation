import random
from power_temp_simulation.power_temp_simulation import PowerTemperatureSimulator

SIM_TIME = 0.0
DELTA_TIME = 0.0


class CPU:
    def __init__(self, _id, _random, _params=None):
        self.id = _id
        self.power_temp_sim = PowerTemperatureSimulator(random=_random)
        self.default_params = _params

        # GENERIC PARAMETERS
        self.delta_time_change_status = 10.

        # CPU SPECIFIC PARAMETERS
        self.status = 0
        self.working_time = 0.0

        # TASK SPECIFIC PARAMETERS
        self.is_busy = False
        self.current_task = None
        self.task_time = 0.0
        self.task_start_time = 0.0

        # POWER TEMPERATURE SPECIFIC PARAMETERS
        self.temperature = 0
        self.power = 0

        self.reset()
        self.power_temp_sim.set_level(self.status)

    def reset(self):
        # GENERIC PARAMETERS
        self.delta_time_change_status = self.default_params.get('time_change_status')

        # CPU SPECIFIC PARAMETERS
        self.status = self.default_params.get('status')
        self.working_time = 0.0

        # TASK SPECIFIC PARAMETERS
        self.is_busy = False
        self.current_task = None
        self.task_time = 0.0
        self.task_start_time = 0.0

        # POWER TEMPERATURE SPECIFIC PARAMETERS
        self.temperature = self.default_params.get('temperature')
        self.power = self.default_params.get('power')

    def assign_task(self, task):
        self.current_task = task
        # if the task is the null task put the cpu in idle
        if self.current_task is None:
            self.task_time = 0
            return
        # execute the task
        self.is_busy = True
        self.execute_task()

    def execute_task(self):
        self.task_start_time = SIM_TIME
        self.task_time = self.current_task.execute() + SIM_TIME

    def set_status(self, val):
        self.status = val
        self.power_temp_sim.set_level(self.status)

    def simulate_params(self):
        self.power, self.temperature = self.power_temp_sim.value_at(1)

    def prob_to_change_status(self):
        # Dividing the working_time in chunks, each one correspond to the status time interval
        int_value = int(self.working_time / self.delta_time_change_status)
        int_value = min(3, int_value)

        if int_value != self.status:
            # Get the decimal part, used as probability
            prob = (self.working_time / self.delta_time_change_status) - int_value
            # If the status is changing from high value to low, the probability is (1 - prob)
            if int_value < self.status:
                prob = 1 - prob

            if random.random() < prob:
                self.set_status(int_value)

    def update(self):

        # compute probability to change status
        self.prob_to_change_status()

        # Simulate temperature and power consumption
        self.simulate_params()

        # CPU IS WORKING
        if self.current_task is not None:
            # TASK isn't ended yet
            if SIM_TIME < self.task_time:
                self.working_time += DELTA_TIME
                return

            # If the task is a periodic one the cpu will auto re-assign the same task
            if self.current_task.is_periodic:
                self.assign_task(self.current_task)
                return

            # Task is ended and isn't periodic
            else:
                # FREE THE CPU
                self.is_busy = False
                self.task_time = 0.0
                # CLEAR TASK
                self.current_task = None
                return

        # REDUCE WORKING TIME SINCE
        self.working_time -= DELTA_TIME
        self.working_time = max(0.0, self.working_time)

    def get_param_info(self) -> str:
        task_value = [self.current_task.id if self.current_task is not None else -1]
        return ("JID:[" + f"{task_value[0]}".rjust(2) + "] " +
                "T:" + f"{self.temperature:.3f}".rjust(6) + " " +
                "W:" + f"{self.power:.3f}".rjust(6) + " " +
                f"S:{self.status} "
                f"{self.working_time:6}" + "[s]")

    def __str__(self):
        if self.is_busy:
            return f"CPU[{self.id:03}] {self.get_param_info()}"
        return f"CPU[{self.id:03}] {self.get_param_info()}"


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
    def __init__(self, _id, num_cpus, _random, _params=None):
        self.id = _id
        cpu_params = None
        if _params is not None:
            cpu_params = _params.get('cpu')
        self.cpus = [CPU(i, _random, cpu_params) for i in range(num_cpus)]

    def assign_data(self, data, is_fault=False):
        for idx, _d in enumerate(data):
            if is_fault:
                if _d != -1:
                    self.cpus[idx].set_status(_d)
            else:
                self.cpus[idx].assign_task(_d)

    def update(self):
        for cpu in self.cpus:
            cpu.update()

    def collect_data_from_cpus(self):
        output_list = list()
        for cpu in self.cpus:
            if cpu.current_task is not None:
                output_list.append(cpu.current_task.id)
            else:
                output_list.append(-1)
            output_list.append(cpu.temperature)
            output_list.append(cpu.power)
            output_list.append(cpu.status)
        return output_list

    def self_report(self):
        string_output = f"Board[{self.id:03}]"
        for cpu in self.cpus:
            string_output += f"\t|"
            string_output += cpu.__str__()
        string_output += "\t||"
        return string_output

    def reset(self):
        for cpu in self.cpus:
            cpu.reset()


class Network:
    def __init__(self, num_boards, num_cpus, _random, _params=None):
        self.boards = [Board(idx, num_cpus, _random, _params) for idx in range(num_boards)]

    def update(self):
        for board in self.boards:
            board.update()

    def reset(self):
        for board in enumerate(self.boards):
            board.reset()

    def interact(self, data=None, is_fault=False):
        if data is not None:
            for idx, board in enumerate(self.boards):
                board.assign_data(data.get(idx), is_fault)

        else:
            output_string = list()
            output_data = list()
            for board in self.boards:
                output_string.append(board.self_report())
                output_data.append(board.collect_data_from_cpus())
            return output_data, output_string
