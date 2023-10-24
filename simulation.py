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

    def interact_with_object(self, data=None):
        if data is not None:
            self.object.interact(data)
        else:
            return self.object.interact()
