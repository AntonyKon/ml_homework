import random
from collections import defaultdict
from math import sqrt, floor
import numpy as np

# Rock = 0, Paper = 1, Scissors = 2

random.seed("rps")
np.random.seed(1452342)


def rock_agent(observation, configuration):
    return 0


def paper_agent(observation, configuration):
    return 1


def scissors_agent(observation, configuration):
    return 2


def copy_opponent_agent(observation, configuration):
    if observation.step > 0:
        return observation.lastOpponentAction
    else:
        return random.randrange(0, configuration.signs)


def inversed_copy_opponent_agent(observation, configuration):
    if observation.step > 0:
        return (observation.lastOpponentAction + 1) % configuration.signs
    else:
        return random.randrange(0, configuration.signs)


def strict_order_agent(observation, configuration):
    previous_agent_step = observation.step % configuration.signs
    return previous_agent_step


def random_agent(observation, configuration):
    return random.randrange(0, configuration.signs)


action_map = defaultdict(int)


def adaptive_agent(observation, configuration):
    if observation.step == 0:
        return 0
    else:
        action_map[observation.lastOpponentAction] += 1
        most_used_action = max(action_map.items(), key=lambda item: item[1])[0]
        opposite_action = (most_used_action + 1) % configuration.signs
        return opposite_action


def random_exclusive_agent(observation, configuration):
    if observation.step == 0:
        return 0
    used_action = observation.lastOpponentAction
    list_of_actions: list[int] = list(range(0, configuration.signs))
    list_of_actions.remove(used_action)
    print(list_of_actions)
    return random.choice(list_of_actions)


def fibonacci_agent(observation, configuration):
    def fibonacci(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return a

    return fibonacci(observation.step) % configuration.signs


def sqrt_agent(observation, configuration):
    return floor(sqrt(observation.step) % configuration.signs)


def poisson_agent(observation, configuration):
    return int(
        np.random.poisson(configuration.signs, configuration.episodeSteps + 1)[observation.step] % configuration.signs
    )
