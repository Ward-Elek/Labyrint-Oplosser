## Key Definitions

**Environment**: the entire maze. It is simply a set of cells with walls between some of them. We can also say that the environment is a set of states (see further). The environment is typically stated in the form of a [Markov decision process](https://en.wikipedia.org/wiki/Markov_decision_process) (MDP).

**State**: a single element in the environment. In our case, a state is a cell. 

**Agent**: an entity that can interact with the environment via actions. The agent exists in a state. Our agent is visualized as the blue dot in the example in the previous task.

**Action**: a function an agent can invoke from a given state to move to another state. Our possible actions are move up, move down, move left, and move right. 

**Reward** (positive or negative) is the *reinforcement* received under each transition.

A RL agent tries to **learn a policy**, i.e., by trial and error to select
actions that maximize its expected discounted future rewards for state-action
pairs represented by the action values.

**[Q-learning](https://en.wikipedia.org/wiki/Q-learning)** is a common form of RL,
where the optimal policy is learned implicitly in the form of a **Q-function**. The optimal action-value function $Q^∗$
is known to be the unique solution to the **[Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation)**.

A **Q-table** records the expected value of a state when an action is taken. It records that for all state and action combinations. 
In other words, a Q-table maps a reward to every (state, action) pair. To start the Q-learning algorithm, we set all Q-values to 0. As the algorithm runs and the agent explores the states, we update the Q-table.