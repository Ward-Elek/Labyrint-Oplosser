Implement the method `walk`, which will walk the 
Q-matrix to build the shortest path through the maze.
The method should fill `Agent.path` so that it stores the shortest path (a sequence of cell
numbers from start to goal, inclusively).

Remember that in the Q-matrix, row indices are "from" cells and column indices are "to" cells.
Starting from the row that corresponds to the starting cell, you need to find the next cell to move in to 
by finding the largest Q values in the given row. Repeat this until you reach the goal. 
The method assumes the goal state is reachable. 

It should also print this sequence so that it looks something like:

`0->1->4->3->6->7->8->5->2->done`

In case at some point it becomes impossible to determine a next cell from the Q matrix
(there is no maximum value in the row) it probably means that the algorithm did not find a way,
in which case append a string `'break'` to the `path`. You can also print a message like `"Path not found!"` or something like that.

<div class="hint">

You can make use of the function `np.argmax()`, which returns the index of the largest 
value of an input vector. For example, if a vector `vec` had values `(0, 10, 9, 23, 4)`, 
then `np.argmax(vec)` would return `3`. 
</div>
