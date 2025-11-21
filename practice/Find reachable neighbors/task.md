To populate our `Feasibility` matrix with 0 and 1, we will first need to 
write a function `find_reachable_neighbors` that accepts a maze and a cell in that maze and returns a list of neighbors:
`Cell` objects that are accessible from the given cell
(that is, do not have a shared wall with it).

Complete the implementation of this function in `convert.py`.

<div class="hint">

To fill the list `neighbors` with accessible neighbor Cell objects for a given cell, 
you can iterate over the `maze.delta` dictionary to get each potential neighbor and then check if it 
actually exists within the maze bounds. If it does, check if the
wall is absent between the two cells (you might want to use the `cell.walls` dictionary). 
If so, append the neighbor cell object to the list.

</div>