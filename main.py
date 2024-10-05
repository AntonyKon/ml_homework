from collections import defaultdict

import pandas as pd
import itertools

import matplotlib.pyplot as plt
import seaborn as sns

from kaggle_environments import make

from agents import copy_opponent_agent, inversed_copy_opponent_agent, rock_agent, paper_agent, scissors_agent, \
    strict_order_agent, random_agent, adaptive_agent, random_exclusive_agent, fibonacci_agent, sqrt_agent, \
    poisson_agent, action_map


def calculate_result_for_agents(action1, action2):
    diff = abs(action1 - action2)
    if diff == 1:
        return action1 - action2
    else:
        return -(action1 - action2) // 2


def process_step_results(steps):
    game_results = tuple(map(lambda step: calculate_result_for_agents(step[0]['action'], step[1]['action']), steps))
    return game_results.count(1), game_results.count(-1)


def format_func_name(name):
    return name.replace("_", "\n")


agents = [
    copy_opponent_agent,
    inversed_copy_opponent_agent,
    rock_agent,
    paper_agent,
    scissors_agent,
    strict_order_agent,
    random_agent,
    adaptive_agent,
    random_exclusive_agent,
    fibonacci_agent,
    sqrt_agent,
    poisson_agent
]

env = make(
    "rps",  # environment to use - no need to change
    configuration={"episodeSteps": 100}  # number of episodes
)
statistic = defaultdict(int)


for pair in itertools.combinations(agents, r=2):
    steps = env.run(pair)
    action_map.clear()
    agent1_wins, agent2_wins = process_step_results(steps)
    print(pair[0].__name__, pair[1].__name__, f'{agent1_wins}:{agent2_wins}')
    statistic[format_func_name(pair[0].__name__)] += agent1_wins
    statistic[format_func_name(pair[1].__name__)] += agent2_wins

statistic_frame = pd.DataFrame(statistic.items(), columns=['agent', 'wins'])
print(statistic_frame)

fig, ax = plt.subplots(figsize=(10, 7))

ax = sns.barplot(statistic_frame, x='agent', y='wins', hue='agent', palette='Paired', ax=ax)
ax.set_axisbelow(True)
ax.grid(visible=True, linestyle='-', axis='both', zorder=0)
ax.xaxis.set_tick_params(labelsize=7)

for i in ax.containers:
    ax.bar_label(i, )

ax.get_figure().savefig("result.png")
