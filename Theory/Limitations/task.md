## Limitations of Reinforcement Learning

When working with any kind of model, one must keep in mind its limitations.
One of the main limitations of RL is the slowness in convergence. Thus, several methods have been proposed and used to speed up RL. They all involve the incorporation
of prior knowledge or bias into RL. You can read more about it in [this article](https://hal.archives-ouvertes.fr/hal-00331752/document).

One aspect that makes training RL models particularly challenging is that the consequent 
model inputs depend on actions taken previously. This can lead to all sorts of problems and usually results in unstable 
learning behavior. Also, this sequence-dependence in RL creates a so-called delayed effect, which means that the action 
taken at a time step may result in a future reward appearing some arbitrary number of steps later. 

The standard Q-learning algorithm (using a $Q$ table) applies only to discrete action and state spaces. Discretization 
of these values leads to inefficient learning, largely due to the curse of dimensionality. However, there are adaptations of 
Q-learning that attempt to solve this problem, such as [Wire-fitted Neural Network Q-Learning](https://users.cecs.anu.edu.au/~rsl/rsl_papers/99ai.kambara.pdf).
