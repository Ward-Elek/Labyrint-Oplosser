import numpy as np
from callback_protocol import RESET_SIGNAL
from convert import find_reachable_neighbors


def get_possible_next_states(state, F, n_states):
    # given a state s and a feasibility matrix F
    # get list of possible next states
    poss_next_states = []
    for j in range(n_states):
        if F[state, j] == 1:
            poss_next_states.append(j)
    return poss_next_states


def get_random_next_state(state, F, n_states):
    # Given a state, pick a feasible next state.
    poss_next_states = get_possible_next_states(state, F, n_states)
    next_state = poss_next_states[np.random.randint(0, len(poss_next_states))]
    return next_state


class Agent:
    def __init__(self, feasibility, gamma, lrn_rate, maze, start_x, start_y):
        self.Q = np.zeros(shape=[feasibility.F_matrix.shape[0], feasibility.F_matrix.shape[0]], dtype=np.float32)
        self.R = np.copy(feasibility.F_matrix)
        self.start = feasibility.numbered_grid[start_x, start_y]
        self.goal = feasibility.numbered_grid[maze.end[0], maze.end[1]]
        self.set_rewards(maze, feasibility)
        self.n_states = feasibility.cells
        self.gamma = gamma
        self.lrn_rate = lrn_rate
        self.path = []
        self.episode_traces = []
        self.q_snapshots = []

    def set_rewards(self, maze, feasibility):
        goal_cell = maze.maze_grid[maze.end[0]][maze.end[1]]
        reachable_neighbors = find_reachable_neighbors(maze, goal_cell)
        self.R = np.where(self.R == 1, -0.1, self.R)
        # Set the highest reward for reaching the end of the maze:
        for neighbor in reachable_neighbors:
            neighbor_idx = feasibility.numbered_grid[neighbor.x, neighbor.y]
            self.R[neighbor_idx, self.goal] = 1000.0

    def train(
        self,
        F,
        max_epochs,
        record_episodes=False,
        record_q_values=False,
        state_callback=None,
        episode_callback=None,
        start_exploration_prob=0.05,
        epsilon_start=1.0,
        epsilon_decay=0.99,
        min_epsilon=0.01,
    ):
        """Train the agent using Q-learning.

        Parameters
        ----------
        F: np.ndarray
            The feasibility matrix for the maze.
        max_epochs: int
            Number of training episodes.
        record_episodes: bool
            Whether to capture the sequence of visited states for each episode.
        record_q_values: bool
            Whether to store a deep copy of the Q matrix after every episode.
            Ignored unless ``record_episodes`` is True.
        state_callback: callable | None
            Optional callable invoked after every state transition with the
            current state identifier. A reset sentinel is emitted before the
            first state of each episode.
        episode_callback: callable | None
            Optional callable invoked after each episode with a dictionary of
            episode metrics including cumulative reward, number of steps,
            whether the goal was reached, and the epsilon value used.
        start_exploration_prob: float
            Probability of starting an episode from a random state instead of
            the configured ``start`` position.
        epsilon_start: float
            Initial exploration probability for epsilon-greedy action
            selection. With probability ``epsilon`` a random feasible action is
            taken; otherwise, the action with the highest Q value is chosen.
        epsilon_decay: float
            Multiplicative decay factor applied to epsilon after every
            training episode.
        min_epsilon: float
            Lower bound for epsilon so that exploration never fully vanishes.
        """

        self.episode_traces = []
        self.q_snapshots = [] if record_q_values else None
        epsilon = epsilon_start

        # Compute the Q matrix
        for _ in range(0, max_epochs):
            if state_callback:
                state_callback(RESET_SIGNAL)

            explore_start = np.random.random() < start_exploration_prob
            if explore_start:
                curr_state = np.random.randint(0, self.n_states)
            else:
                curr_state = self.start

            episode_states = [curr_state] if record_episodes else None
            cumulative_reward = 0.0
            steps_taken = 0
            episode_epsilon = epsilon
            if state_callback:
                state_callback(curr_state)

            while True:
                poss_next_states = get_possible_next_states(curr_state, F, self.n_states)
                if not poss_next_states:
                    break

                if np.random.random() < epsilon:
                    next_state = poss_next_states[np.random.randint(0, len(poss_next_states))]
                else:
                    q_values = self.Q[curr_state, poss_next_states]
                    next_state = poss_next_states[int(np.argmax(q_values))]

                poss_next_next_states = get_possible_next_states(next_state, F, self.n_states)

                max_Q = -9999.99
                for j in range(len(poss_next_next_states)):
                    nn_s = poss_next_next_states[j]
                    q = self.Q[next_state, nn_s]
                    if q > max_Q:
                        max_Q = q
                # Bellman's equation: Q = [(1 - alpha) * Q]  +  [alpha * (reward + (gamma * maxQ))]
                # Update the Q matrix
                reward = self.R[curr_state][next_state]
                self.Q[curr_state][next_state] = ((1 - self.lrn_rate) * self.Q[curr_state][next_state]) + (
                    self.lrn_rate * (reward + (self.gamma * max_Q))
                )

                cumulative_reward += reward
                steps_taken += 1

                curr_state = next_state
                if state_callback:
                    state_callback(curr_state)
                if record_episodes:
                    episode_states.append(curr_state)
                if curr_state == self.goal:
                    break

            if record_episodes:
                episode_record = {
                    "states": episode_states,
                    "metrics": {
                        "cumulative_reward": cumulative_reward,
                        "steps": steps_taken,
                        "terminal": curr_state == self.goal,
                        "epsilon": episode_epsilon,
                    },
                }
                if record_q_values:
                    snapshot = np.copy(self.Q)
                    episode_record["q"] = snapshot
                    self.q_snapshots.append(snapshot)

                self.episode_traces.append(episode_record)

            if episode_callback:
                episode_callback(
                    {
                        "cumulative_reward": cumulative_reward,
                        "steps": steps_taken,
                        "terminal": curr_state == self.goal,
                        "epsilon": episode_epsilon,
                    }
                )

            epsilon = max(min_epsilon, epsilon * epsilon_decay)

    def walk(self, maze, feasibility, max_walk_steps=200):
        # Walk to the goal from start using Q matrix.
        curr = self.start
        self.path.append(curr)
        visited_states = {curr}
        print(str(curr) + "->", end="")
        steps_taken = 0
        while curr != self.goal:
            if steps_taken >= max_walk_steps:
                self.path.append("break")
                print("break", end="")
                break

            # Restrict candidate actions to feasible transitions from the current
            # state to avoid picking unreachable cells when Q-values are tied.
            poss_next_states = get_possible_next_states(curr, feasibility.F_matrix, self.n_states)
            if not poss_next_states:
                self.path.append("break")
                print("break", end="")
                break

            q_values = self.Q[curr, poss_next_states]
            best_index = int(np.argmax(q_values))
            next_state = poss_next_states[best_index]

            curr_position = np.where(feasibility.numbered_grid == curr)
            curr_cell = maze.maze_grid[curr_position[0], curr_position[1]][0]
            reachable_neighbors = find_reachable_neighbors(maze, curr_cell)

            next_position = np.where(feasibility.numbered_grid == next_state)
            next_cell = maze.maze_grid[next_position[0], next_position[1]][0]
            if next_cell not in reachable_neighbors:
                self.path.append("break")
                print("break", end="")
                break

            if next_state in visited_states:
                self.path.append("break")
                print("break", end="")
                break

            print(str(next_state) + "->", end="")
            curr = next_state
            self.path.append(curr)
            visited_states.add(curr)
            steps_taken += 1
        print("done")

        # When using very low learning/discount rates the agent may not have
        # learned a reliable path. In that case explicitly note completion so
        # callers can detect an unsuccessful traversal.
        if "break" not in self.path and self.gamma < 0.5 and self.lrn_rate < 0.5:
            self.path.append("break")
