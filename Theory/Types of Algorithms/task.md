## Reinforcement Learning Algorithms

In a Reinforcement Learning algorithm, the agent's policy can be of two types:

- In **on-policy** algorithms, the $𝑄(𝑠,𝑎)$ function is learned from the actions that we took using our current policy $𝜋(𝑎|𝑠)$.

- In **off-policy** algorithms, the $𝑄(𝑠,𝑎)$ function is learned from taking different actions (for example, random actions).


### Monte Carlo
Monte Carlo methods are a broad class of computational algorithms that rely on 
repeated random sampling to obtain numerical results. They can be either on- or off-policy.
The underlying concept is to use 
randomness to solve problems that might be deterministic in principle. Monte Carlo methods are mainly used in three problem 
classes: optimization, numerical integration, and generating draws from a probability 
distribution, and they are most useful when it is difficult or
impossible to use other approaches. Areas of application include physical sciences, engineering, climate science,
computational biology, computer graphics, and so on.

### Q-learning

Q-learning is a model-free off-policy reinforcement learning algorithm to learn the value of an 
action in a particular state. It does not require a model of the environment (hence 
"model-free"), and it can handle problems with stochastic transitions and rewards without 
requiring adaptations. Applications include gaming, robotics, automatic configuration of multi-tier web systems,
improved news recommendation systems, estimating optimal treatment strategies in personalized medicine, and so on.

- **Deep Q-learning** (DQN):
the [DeepMind](https://en.wikipedia.org/wiki/DeepMind) system uses a deep convolutional neural network, with layers of tiled convolutional 
filters to mimic the effects of receptive fields.


- **SARSA**
State–action–reward–state–action (SARSA) is an on-policy variation of Q-learning. 
The update equation for SARSA depends on the current state, current action, reward obtained, next state, and next action.
$$Q^{new}(s_{t},a_{t})\leftarrow Q(s_{t},a_{t})+\alpha [r_{t}+\gamma Q(s_{t+1},a_{t+1})-Q(s_{t},a_{t})]$$

>Compare this equation with the Q-learning update equation in the next task to understand the difference.


You can read more about the differences between on-policy and off-policy algorithms in this [article](https://www.cs.utexas.edu/users/pstone/Papers/bib2html-links/DeepRL16-hausknecht.pdf).
Value iteration and Policy iteration are another pair of very important concepts in RL, so if you would like to have
a clearer understanding of different approaches, we encourage you to read this [article](https://towardsdatascience.com/policy-and-value-iteration-78501afb41d2).

