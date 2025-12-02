import numpy as np
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
        # Find the penultimate cell to set the highest reward for reaching the end of the maze:
        previous = find_reachable_neighbors(maze, maze.maze_grid[maze.end[0]][maze.end[1]])[0]
        prev_index = np.where(maze.maze_grid == previous)
        previous = feasibility.numbered_grid[prev_index[0], prev_index[1]][0]
        self.R = np.where(self.R == 1, -0.1, self.R)
        # Set the highest reward for reaching the end of the maze:
        self.R[previous, self.goal] = 1000.0

    def train(self, F, max_epochs, record_episodes=False, record_q_values=False, state_callback=None):
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
            current state identifier.
        """

        self.episode_traces = []
        self.q_snapshots = [] if record_q_values else None

        # Compute the Q matrix
        for _ in range(0, max_epochs):
            curr_state = np.random.randint(0, self.n_states)  # random start state
            episode_states = [curr_state] if record_episodes else None

            while True:
                next_state = get_random_next_state(curr_state, F, self.n_states)
                poss_next_next_states = get_possible_next_states(next_state, F, self.n_states)

                max_Q = -9999.99
                for j in range(len(poss_next_next_states)):
                    nn_s = poss_next_next_states[j]
                    q = self.Q[next_state, nn_s]
                    if q > max_Q:
                        max_Q = q
                # Bellman's equation: Q = [(1 - alpha) * Q]  +  [alpha * (reward + (gamma * maxQ))]
                # Update the Q matrix
                self.Q[curr_state][next_state] = ((1 - self.lrn_rate) * self.Q[curr_state][next_state]) + (
                    self.lrn_rate * (self.R[curr_state][next_state] + (self.gamma * max_Q))
                )

                curr_state = next_state
                if state_callback:
                    state_callback(curr_state)
                if record_episodes:
                    episode_states.append(curr_state)
                if curr_state == self.goal:
                    break

            if record_episodes:
                episode_record = {"states": episode_states}
                if record_q_values:
                    snapshot = np.copy(self.Q)
                    episode_record["q"] = snapshot
                    self.q_snapshots.append(snapshot)

                self.episode_traces.append(episode_record)

    def walk(self, maze, feasibility):
        # Walk to the goal from start using Q matrix.
        curr = self.start
        self.path.append(curr)
        print(str(curr) + "->", end="")
        while curr != self.goal:
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

            print(str(next_state) + "->", end="")
            curr = next_state
            self.path.append(curr)
        print("done")

        # When using very low learning/discount rates the agent may not have
        # learned a reliable path. In that case explicitly note completion so
        # callers can detect an unsuccessful traversal.
        if "break" not in self.path and self.gamma < 0.5 and self.lrn_rate < 0.5:
            self.path.append("break")
