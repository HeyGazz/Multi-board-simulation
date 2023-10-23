import random

SIM_TIME = 0.0


class CPU:
    def __init__(self, id):
        self.id = id
        self.is_busy = False
        self.current_task = None
        self.task_time = 0.0

    def assign_task(self, task):
        if not self.is_busy:
            self.is_busy = True
            self.current_task = task
            self.execute_task()

    def execute_task(self):
        self.task_time = self.current_task.execute() + SIM_TIME

    def update(self):
        if SIM_TIME < self.task_time:
            # print(f"{SIM_TIME:.3f} - {self.status()}")
            return
        # FREE THE CPU
        self.is_busy = False
        self.current_task = None
        self.task_time = 0.0
        # print(f"{SIM_TIME:.3f} - {self.status()}")

    def status(self):
        if self.is_busy:
            return f"CPU: {self.id} > {self.current_task.id}"
        return f"CPU: {self.id} > -1"


class Task:
    def __init__(self, id, base_execution_time=0.0, std=0.0, is_periodic=False):
        self.id = id
        self.base_execution_time = base_execution_time
        self.std = std
        self.is_periodic = is_periodic

    def execute(self):
        execution_time = self.base_execution_time + abs(random.gauss(self.base_execution_time, self.std))
        # print(f"Task {self.id} is being executed for {execution_time:.3f} seconds.")
        return execution_time


class Board:
    def __init__(self, id, num_cpus):
        self.id = id
        self.cpus = [CPU(i) for i in range(num_cpus)]

    def assign_task(self, task):
        for idx, t in enumerate(task):
            if t is not None:
                self.cpus[idx].assign_task(t)

    def update(self):
        for cpu in self.cpus:
            cpu.update()

    def self_report(self):
        string_output = f"Board: {self.id} "
        for cpu in self.cpus:
            string_output += f"\t|\t"
            string_output += cpu.status()
        string_output += "\t||"
        return string_output


class Network:
    def __init__(self, num_boards, num_cpus):
        self.boards = [Board(idx, num_cpus) for idx in range(num_boards)]

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
