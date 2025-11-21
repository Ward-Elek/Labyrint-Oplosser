import numpy as np


class Feasibility:
    def __init__(self, maze_):
        self.cells = maze_.maze_grid.shape[0] * maze_.maze_grid.shape[1]
        self.F_matrix = np.zeros(shape=[self.cells, self.cells], dtype=int)
        self.numbered_grid = np.arange(self.cells).reshape((maze_.maze_grid.shape[0], maze_.maze_grid.shape[1]))
