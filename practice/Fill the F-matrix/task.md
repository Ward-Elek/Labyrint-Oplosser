To populate our `Feasibility` matrix with 0 and 1, we will now need to
complete the method `get_neighbors` of the `Feasibility` class in `convert.py`.
The method should accept a Maze `object` and, by iteratively checking each of
its cells for reachable neighbors (call the function we implemented in the previous step), 
replace `0`s in the `F_matrix` with `1`s on those intersections where it is possible to go from one cell to another.
Keep the `0` where there's a wall between the two cells.

This method should be called in the `__init__` of the class.

<div class="hint">

You can use the `numbered_grid` and a Numpy method `nditer()` to iterate over the numbers of cells in the grid,
get their indices, and access each particular cell in the `maze_maze_grid` using those indices to check if it has 
reachable neighbors.
</div>

<div class="hint">

For each reachable neighbor of each cell, you can access its number in the grid by its indices (`Cell.x`, `Cell.y`) and
then place a `1` in the `F_matrix` at the intersection of the number of the current cell and of its current neighbor.
</div>
