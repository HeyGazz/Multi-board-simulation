import math
import numpy as np

from dataclasses import dataclass
from typing import Union


# See http://www.turingfinance.com/random-walks-down-wall-street-stochastic-processes-in-python/
# for further explanations and other types of generators


@dataclass
class OUParameters:
    delta: float
    mu: Union[float, np.ndarray]
    sigma: Union[float, np.ndarray]
    theta: Union[float, np.ndarray]


class OrnsteinUhlenbeck:
    """
    Essentially, this class is a random number generator that produces a random walk according to the
    mean-reverting Ornstein-Uhlenbeck process
    """

    def __init__(self, ou_params, initial_value=None, random=None):
        self.ou_params = ou_params
        self.random = random
        if initial_value:
            self.value = initial_value
        else:
            self.value = ou_params.mu
        self.time_clock = 0

    def value_at(self, time_clock):
        """
        This method returns the rate levels of a mean-reverting Ornstein Uhlenbeck process.
        :param time_clock: the model parameters object
        :return: the value for the Ornstein Uhlenbeck process at the given time
        """

        assert time_clock >= self.time_clock, 'The OU generator cannot go back in time'

        # Update stochastic process, if required
        for i in range(self.time_clock, time_clock):
            sqrt_delta_sigma = math.sqrt(self.ou_params.delta) * self.ou_params.sigma
            randomness = self.random.normal(loc=0.0, scale=sqrt_delta_sigma)
            drift = self.ou_params.theta * (self.ou_params.mu - self.value) * self.ou_params.delta
            self.value += drift + randomness

        return self.value


class MultivariateOrnsteinUhlenbeck(OrnsteinUhlenbeck):
    """
    Same random number generator as its superclass, d-variate version
    :param delta: scalar
    :param mu: d vector
    :param sigma: d x d matrix
    :param theta: d x d matrix
    """

    def __init__(self, ou_params, initial_value=None, random=None):
        super().__init__(ou_params, initial_value, random)
        self.value = self.value.copy()
        self.mean = np.array([0.0] * self.ou_params.mu.shape[0])

    def value_at(self, time_clock):
        """
        This method returns the rate levels of a mean-reverting Ornstein Uhlenbeck process.
        :param time_clock: the model parameters object
        :return: the value for the Ornstein Uhlenbeck process at the given time
        """

        assert time_clock >= self.time_clock, 'The OU generator cannot go back in time'

        # Update stochastic process, if required
        for i in range(self.time_clock, time_clock):
            sqrt_delta_sigma = math.sqrt(self.ou_params.delta) * self.ou_params.sigma
            randomness = self.random.multivariate_normal(mean=self.mean, cov=sqrt_delta_sigma)
            drift = np.dot(self.ou_params.theta, (self.ou_params.mu - self.value)) * self.ou_params.delta
            self.value += drift + randomness

        return self.value
