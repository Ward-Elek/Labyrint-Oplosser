import numpy as np
from convert import find_reachable_neighbors


def get_poss_next_states(state, F, n_states):
    # given a state s and a feasibility matrix F
    # get list of possible next states
    poss_next_states = []
    for j in range(n_states):
        if F[state, j] == 1:
            poss_next_states.append(j)
    return poss_next_states


def get_rnd_next_state(state, F, n_states):
    # Given a state, pick a feasible next state.
    poss_next_states = get_poss_next_states(state, F, n_states)
    next_state = poss_next_states[np.random.randint(0, len(poss_next_states))]
    return next_state


class TestAgent:
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

    def set_rewards(self, maze, feasibility):
        step_cost = 0.1
        goal_reward = 1000.0
        density_scale = 1.0

        rewards = np.zeros_like(self.R, dtype=np.float32)
        goal_x, goal_y = maze.end

        for (x_idx, y_idx), state_idx in np.ndenumerate(feasibility.numbered_grid):
            curr_cell = maze.maze_grid[x_idx, y_idx]
            curr_distance = abs(goal_x - x_idx) + abs(goal_y - y_idx)
            reachable_neighbors = find_reachable_neighbors(maze, curr_cell)

            for neighbor in reachable_neighbors:
                neighbor_idx = feasibility.numbered_grid[neighbor.x, neighbor.y]
                neighbor_distance = abs(goal_x - neighbor.x) + abs(goal_y - neighbor.y)

                if neighbor_idx == self.goal:
                    reward = goal_reward
                else:
                    shaping = density_scale * (curr_distance - neighbor_distance)
                    reward = -step_cost + shaping

                rewards[state_idx, neighbor_idx] = reward

        self.R = rewards

    def train(self, F, max_epochs):
        # Compute the Q matrix
        for i in range(0, max_epochs):
            curr_state = np.random.randint(0, self.n_states)  # random start state

            step_count = 0
            step_limit = self.n_states * 4

            while True:
                if step_count >= step_limit:
                    break

                next_state = get_rnd_next_state(curr_state, F, self.n_states)
                poss_next_next_states = get_poss_next_states(next_state, F, self.n_states)

                max_Q = -9999.99
                for j in range(len(poss_next_next_states)):
                    nn_s = poss_next_next_states[j]
                    q = self.Q[next_state, nn_s]
                    if q > max_Q:
                        max_Q = q
                # Bellman's equation: Q = [(1-a) * Q]  +  [a * (rt + (g * maxQ))]
                # Update the Q matrix
                self.Q[curr_state][next_state] = ((1 - self.lrn_rate) * self.Q[curr_state][next_state]) + (
                        self.lrn_rate * (self.R[curr_state][next_state] + (self.gamma * max_Q)))

                step_count += 1
                curr_state = next_state
                if curr_state == self.goal:
                    break

    def walk(self, maze, feasibility):
        # Walk to the goal from start using Q matrix.
        curr = self.start
        self.path.append(curr)
        step_limit = self.n_states * 4
        steps = 0
        # print(str(curr) + "->", end="")
        while curr != self.goal and steps < step_limit:
            curr_position = np.where(feasibility.numbered_grid == curr)
            curr_cell = maze.maze_grid[curr_position[0], curr_position[1]][0]

            next_ = np.argmax(self.Q[curr])
            next_position = np.where(feasibility.numbered_grid == next_)
            next_cell = maze.maze_grid[next_position[0], next_position[1]][0]

            # if next_ not in find_reachable_neighbors(maze, curr_cell_obj):
            reachable_neighbors = find_reachable_neighbors(maze, curr_cell)
            if next_cell not in reachable_neighbors:
                # print('Path not found!')
                self.path.append('break')
                break
            # print(str(next_) + "->", end="")
            curr = next_
            self.path.append(curr)
            steps += 1
        # print("done")
