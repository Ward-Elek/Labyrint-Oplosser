import numpy as np


class Feasibility:
    def __init__(self, maze_):
        self.cells = maze_.maze_grid.shape[0] * maze_.maze_grid.shape[1]
        self.F_matrix = np.zeros(shape=[self.cells, self.cells], dtype=int)
        self.numbered_grid = np.arange(self.cells).reshape((maze_.maze_grid.shape[0], maze_.maze_grid.shape[1]))
        self.get_neighbors(maze_)

    def get_neighbors(self, maze):
        for index, cell_num in np.ndenumerate(self.numbered_grid):
            curr_cell = maze.maze_grid[index]
            reachable = find_reachable_neighbors(maze, curr_cell)
            for neighbor in reachable:
                neighbor_num = self.numbered_grid[neighbor.x, neighbor.y]
                self.F_matrix[int(cell_num), neighbor_num] = 1


def find_reachable_neighbors(maze, cell):
    neighbors = []
    for direction, (dx, dy) in maze.delta.items():
        neighbor_x, neighbor_y = cell.x + dx, cell.y + dy
        if (0 <= neighbor_x < maze.nx) and (0 <= neighbor_y < maze.ny):
            if not cell.walls[direction]:
                neighbors.append(maze.cell_at(neighbor_x, neighbor_y))
    return neighbors
