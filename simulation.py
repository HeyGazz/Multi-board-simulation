import components


class Simulation:
    def __init__(self, _object=None, delta_time=1.0):
        # self.delta_time = delta_time
        self.object = _object
        components.SIM_TIME = 0.0
        components.DELTA_TIME = delta_time

    def running_simulation(self, time_interval):
        # CHECK if the time interval is lesser than the delta time
        time_interval = max(components.DELTA_TIME, time_interval)

        # COMPUTE how many steps to take
        steps = int(time_interval // components.DELTA_TIME)
        for _ in range(steps):
            # UPDATE the network
            self.object.update()
            # INCREASE the simulation time
            components.SIM_TIME += components.DELTA_TIME

    def interact_with_object(self, data=None, is_assign_task=False, is_get_data=False, is_reset=False, is_fault=False):

        if is_assign_task:
            self.object.interact(data)
        elif is_get_data:
            return self.object.interact()
        elif is_reset:
            self.object.reset()
        elif is_fault:
            self.object.interact(data, is_fault)
        # if data is not None:
        #     self.object.interact(data)
        # else:
        #     return self.object.interact()
