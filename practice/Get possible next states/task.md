To train our agent, we will need to fill the Q-matrix with some values describing the 'quality' of making a particular move 
in the context of our overall goal - reaching the end of the maze in the smallest number of steps.
We will be using the `train` method of the `Agent` class for that.

The `train` method will need a couple of helper functions first.
The first one, `get_possible_next_states`, uses the F-matrix to determine which states (cells) can be reached
from a given state and returns those states as a list. 
For example, given the maze below, if `s = 5`, the returned list is `[2, 8]`.

<img src="maze_example.png" width="300">

### Task
Complete the implementation of the function `get_possible_next_states` in `learn.py`.

<style>
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>