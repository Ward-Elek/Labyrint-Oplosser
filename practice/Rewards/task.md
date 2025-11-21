The R (reward) matrix defines rewards for moving from one cell to another for each pair of cells.
The R-matrix is built the same way as the Q-matrix:
its row indices are the "from" cells and the column indices are the "to" cells.
Most feasible moves give a negative reward of -0.1, 
which punishes the moves that don't make progress and therefore discourages going in circles or back and forth. For the example below, we would set one big reward R[5][2] = 1000.0, 
which moves you to the goal state.

<img src="maze_example.png" width="300">

You already predefined the R-matrix in the previous task. Now, you need to fill it with actual reward values.
No rewards are needed at the intersections of the cells that are not reachable from one another (keep the `0`s).
Every move gets a -0.1 reward except for the last one – reaching the goal – which gets 1000.0. 
Complete the method `set_rewards` so that it fills the `R` matrix according to the guidelines above.

Do not forget to call the method in the `__init__`.

<div class="hint">

You can use `numpy.where` to replace `1`s in the template (remember that they are the places where cells are reachable from one another)
with `-0.1`.
</div>

<div class="hint">

You will probably need to figure out the number of the penultimate cell 
and then set the value `R[number_of_penultimate_cell][number_of_goal_cell]` to `1000.0`.
</div>

<div class="hint">

You could use the function `find_reachable_neighbors` from the module convert.py to find the penultimate cell.
Our maze-building algorithm works in such a way that there will always be only one cell reachable from the goal.
</div>

<style>
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>