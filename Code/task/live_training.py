"""Run training while streaming live updates to a Pygame viewer."""

import threading
from collections import deque

import numpy as np

from convert import Feasibility
from learn import Agent
from live_view import LiveMazeViewer
from maze import Maze


def prompt_for_value(prompt, caster, validator=lambda value: True, error_message="Invalid input"):
    while True:
        try:
            value = caster(input(prompt))
            if validator(value):
                return value
            print(error_message)
        except (ValueError, IndexError):
            print(error_message)


def main():
    dimensions = prompt_for_value(
        "Enter maze dimensions separated by a space (e.g. 4 4): ",
        lambda raw: [int(v) for v in raw.split()],
        lambda vals: len(vals) == 2 and all(v > 0 for v in vals),
        "Please provide two positive integers separated by a space.",
    )
    dimension1, dimension2 = dimensions

    start_coords = prompt_for_value(
        "Enter x and y coordinates of the maze start separated by a space: ",
        lambda raw: [int(v) for v in raw.split()],
        lambda vals: len(vals) == 2 and 0 <= vals[0] < dimension1 and 0 <= vals[1] < dimension2,
        "Start coordinates should be inside the maze. Numbering is zero-based.",
    )
    start_x, start_y = start_coords

    gamma = prompt_for_value(
        "Enter the gamma value (0, 1]: ",
        float,
        lambda val: 0 < val <= 1,
        "Gamma should be a number between 0 and 1.",
    )

    lrn_rate = prompt_for_value(
        "Enter the learning rate value (0, 1]: ",
        float,
        lambda val: 0 < val <= 1,
        "Learning rate should be a number between 0 and 1.",
    )

    max_epochs = 1000

    maze = Maze(dimension1, dimension2, [start_x, start_y])
    feasibility = Feasibility(maze)
    agent = Agent(feasibility, gamma, lrn_rate, maze, start_x, start_y)

    viewer = LiveMazeViewer(maze, feasibility)
    training_done = threading.Event()
    episode_metrics = []
    # Rolling window used for derived metrics. Recreated when starting a new
    # training run to ensure graphs begin fresh.
    rolling_window = 50
    rolling_metrics = deque(maxlen=rolling_window)

    def callback(state):
        viewer.enqueue_state(state)

    def on_episode(metrics):
        """Push raw and rolling metrics to the live viewer.

        The rolling window is capped at ``rolling_window`` episodes and is
        reset when a new training run starts (i.e., when this callback is
        redefined), ensuring the graphs stay consistent across runs.
        """

        episode_metrics.append(metrics)
        rolling_metrics.append(metrics)

        if rolling_metrics:
            rewards = [m.get("cumulative_reward", 0.0) for m in rolling_metrics]
            steps = [m.get("steps", 0) for m in rolling_metrics]
            successes = [bool(m.get("terminal", False)) for m in rolling_metrics]

            derived_metrics = {
                "reward (rolling avg)": float(np.mean(rewards)),
                "steps (rolling avg)": float(np.mean(steps)),
                "success ratio": float(np.mean(successes)),
            }
        else:
            derived_metrics = {}

        viewer.enqueue_metrics({**metrics, **derived_metrics})

    def training_task():
        agent.train(
            feasibility.F_matrix,
            max_epochs,
            record_episodes=False,
            record_q_values=False,
            state_callback=callback,
            episode_callback=on_episode,
        )
        agent.path = []
        agent.walk(maze, feasibility)
        solved_path = [state for state in agent.path if isinstance(state, (int, np.integer))]
        viewer.set_solved_path(solved_path)
        training_done.set()

    training_thread = threading.Thread(target=training_task, daemon=True)
    training_thread.start()

    viewer.run(completion_event=training_done)
    training_thread.join()


if __name__ == "__main__":
    main()
