import components


class Simulation:
    def __init__(self, object = None, delta_time=1.0):
        self.delta_time = delta_time
        self.object = object
        components.SIM_TIME = 0.0

    def running_simulation(self, time_interval):
        steps = int(time_interval//self.delta_time)
        for _ in range(steps):
            self.object.update()
            components.SIM_TIME += self.delta_time

    def interact_with_object(self, data=None):
        if data is not None:
            self.object.interact(data)
        else:
            return self.object.interact()
