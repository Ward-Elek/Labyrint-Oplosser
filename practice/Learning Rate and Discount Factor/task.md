Take a look at the code in `final_run.py`. This code will ask for your input, generate a maze, and 
run the Q-learning algorithm we implemented to find the shortest path. It will then output 
the path.

As you might remember from the equation we discussed earlier,
Q-learning has two parameters: the learning rate ($\alpha$) and gamma ($\gamma$). Larger values 
of the learning rate increase the influence of both current rewards and future 
rewards (explore) at the expense of past rewards (exploit). The value of the discount factor 
influences the importance of future rewards. 
These values must be determined by trial and error, but using 0.5 is typically a good starting place.
Optimal parameter values in this problem will differ depending on how large the maze is.

Your task is now to find the combinations of parameters that work. When the algorithm works for too long and doesn't seem to be able to 
find a path – maybe a different value combination is needed. With a large maze, you might need to wait 
a little for the algorithm to solve it. If you end up receiving a `'Path not found!'` (or whatever you programmed)
message from `walk()` - maybe you should also try a different combination of the parameters (generally, for 
larger mazes greater gamma and learning rate values are needed). It can also be caused by a problem with your implementation though.

<div class="hint">
Suggested working combinations (try others as well, these are not necessarily optimal):

- 3 x 3 maze, start anywhere, gamma = 0.5, lrn_rate = 0.5
- 5 x 5 maze, start anywhere, gamma = 0.9, lrn_rate = 0.5
- 10 x 10 maze, start anywhere, gamma = 1, lrn_rate = 0.5 (could take more than a minute)

</div>
