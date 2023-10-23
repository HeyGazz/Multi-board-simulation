import numpy as np
import matplotlib.pyplot as plt

from ornstein_uhlenbeck import OUParameters, OrnsteinUhlenbeck, MultivariateOrnsteinUhlenbeck


class PowerSimulator:
    def __init__(self, random=None, level=0):
        self.random = random
        self.level = level
        self.levels = dict()
        self.levels[0] = OUParameters(
            mu=12.0,        # Average value
            delta=1.0,      # Rate of time
            sigma=0.025,    # Volatility of the stochastic process
            theta=0.3       # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.levels[1] = OUParameters(
            mu=18.0,        # average value
            delta=1.0,      # Rate of time
            sigma=0.050,    # Volatility of the stochastic process
            theta=0.2       # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.levels[2] = OUParameters(
            mu=34.0,        # Average value
            delta=1.0,      # Rate of time
            sigma=0.010,    # Volatility of the stochastic process
            theta=0.1       # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.levels[3] = OUParameters(
            mu=52,          # Average value
            delta=1.0,      # Rate of time
            sigma=1.0,      # Volatility of the stochastic process
            theta=0.1       # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.generator = OrnsteinUhlenbeck(self.levels[level], random=self.random)

    def set_level(self, level):
        if level not in self.levels:
            raise f"Unknown level: {level}"

        self.generator.ou_params = self.levels[level]

    def value_at(self, time_clock):
        return self.generator.value_at(time_clock)


class PowerTemperatureSimulator:
    def __init__(self, random=None, level=0):
        self.random = random
        self.level = level
        self.levels = dict()
        self.levels[0] = OUParameters(
            mu=np.array([12.0, 45.0]),          # Average value
            delta=1.0,                          # Rate of time
            sigma=np.array([[0.025, 0.001],
                            [0.001, 0.050]]),   # Volatility of the stochastic process
            theta=np.array([[0.3, 0.0],
                            [0.0, 0.2]])        # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.levels[1] = OUParameters(
            mu=np.array([18.0, 55.0]),          # Average value
            delta=1.0,                          # Rate of time
            sigma=np.array([[0.050, 0.001],
                            [0.001, 0.75]]),   # Volatility of the stochastic process
            theta=np.array([[0.2, 0.0],
                            [0.0, 0.2]])        # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.levels[2] = OUParameters(
            mu=np.array([34.0, 75.0]),          # Average value
            delta=1.0,                          # Rate of time
            sigma=np.array([[0.100,  0.010],
                            [0.010,  0.150]]),  # Volatility of the stochastic process
            theta=np.array([[0.1, -0.001],
                            [-0.001, 0.1]])     # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.levels[3] = OUParameters(
            mu=np.array([52.0, 85.0]),          # Average value
            delta=1.0,                          # Rate of time
            sigma=np.array([[0.150,  0.010],
                            [0.010,  0.200]]),  # Volatility of the stochastic process
            theta=np.array([[0.1, -0.010],
                            [-0.010, 0.1]])     # Rate of mean reversion for Ornstein Uhlenbeck
        )
        self.generator = MultivariateOrnsteinUhlenbeck(self.levels[level], random=self.random)

    def set_level(self, level):
        if level not in self.levels:
            raise f"Unknown level: {level}"

        self.generator.ou_params = self.levels[level]

    def value_at(self, time_clock):
        return self.generator.value_at(time_clock)


if __name__ == '__main__':

    random = np.random.RandomState(1234)

    print()
    print("Power Simulation")
    print("Creating generator at default level")
    power_sim = PowerSimulator(random=random)

    ticks = 100
    time = 0
    levels = list()
    values = list()
    for level in range(4):
        power_sim.set_level(level)
        for t in range(ticks):
            x = power_sim.value_at(time)
            levels.append(level)
            values.append(x)
            time += 1

    print("Simulating {4 * ticks} instants ({ticks} per each level)")
    print(levels)
    print(values)

    plt.cla()
    plt.title('Power Consumption')
    x_list = list(range(len(values)))
    plt.plot(x_list, values, label='Power Consumption')
    plt.legend()
    plt.show()

    print()
    print("Power-temperature Simulation")
    print("Creating generator at default level")
    powertemp_sim = PowerTemperatureSimulator(random=random)

    ticks = 100
    time = 0
    levels = list()
    values = list()
    for level in range(4):
        powertemp_sim.set_level(level)
        for t in range(ticks):
            x = powertemp_sim.value_at(time)
            levels.append(level)
            values.append(x.copy())
            time += 1

    print("Simulating {4 * ticks} instants ({ticks} per each level)")
    print(levels)
    print(values)

    power_values = [v[0] for v in values]
    temp_values = [v[1] for v in values]

    plt.cla()
    plt.title('Power Consumption vs Temperature')
    x_list = list(range(len(power_values)))
    plt.plot(x_list, power_values, label='Power Consumption')
    plt.plot(x_list, temp_values, label='Temperature')
    plt.legend()
    plt.show()
