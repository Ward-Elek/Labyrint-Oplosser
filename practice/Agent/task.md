The heart of the program is the `train()` method of the `Agent` class, which computes the Q-matrix.
The Q stands for quality, with larger values meaning higher quality. The Q-matrix is built the same way as the F-matrix,
but its row indices are the "from" cells and the column indices are the "to" cells.

The Q-learning algorithm updates the equation below, which is based on the Bellman equation.
You don't need to fully understand the Bellman equation to use Q-learning, but if you're interested,
the [Wikipedia article](https://en.wikipedia.org/wiki/Bellman_equation) is a good place to start.

$$Q(s_t,a_t)=[(1 - \alpha)*Q(s_t,a_t)]+[\alpha * (r_t + \gamma * maxQ(s_{t+1},a) \forall a)]$$

where $Q(s_t,a_t)$ is the Q value of going from the current state to the next; 
$\alpha$ is the learning rate; $r_t$ is the reward for the transition; $\gamma$ is the discount factor, which influences the importance of future rewards.
This largest value, $maxQ$, will be used to update the Q-matrix. 


First we will need to define the `Agent` class. Complete the `__init__` method of the class
so that it has the following attributes:
- Gamma (`gamma`) – the discount factor (already defined).
- Learning rate (`lrn_rate`, already defined).
- `path` – a list (initially empty), which at the end of the training process will contain the optimal path – a sequence of cell numbers (already defined).
- `Q` – the Q-matrix. It should be of the same shape as the F-matrix and initially contain zeroes.
- `R` – the reward matrix. It should initially be a copy of the F-matrix.
- `start` – the number of the start cell. You can get it from the `numbered_grid` by the start coordinates.
- `goal` – the number of the goal cell. You can get it from the `numbered_grid` by the coordinates of the maze `end`.
- `n_states` – the number of possible states in the maze, which is equal to the number of cells.


Please make sure that the attributes you define have exactly the right names.
