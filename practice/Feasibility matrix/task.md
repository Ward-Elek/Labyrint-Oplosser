In the `convert.py` file, complete the definition of the `__init__` method of the `Feasibility` class.
You will need to define two more attributes. 

The first one, `numbered_grid`, should be a NumPy array of the same shape as the maze grid, and
it should contain the numbers of all the cells in the grid
(for example, for a 3x3 grid, it would be an array `[[0, 1, 2], [3, 4, 5], [6, 7, 8]]`).

The second one, `F_matrix`, should for now be just an array of zeroes of shape n x n, where n is the number of cells in the grid.
For example, for a 3x3 maze, this would be an array of zeroes of shape (9, 9).

Please make sure that the attributes you define have **exactly** the right names.

