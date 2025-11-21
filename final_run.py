from maze import Maze
from convert import Feasibility
from learn import Agent
import pandas as pd


def my_print(Q):
    labels = [str(x) for x in range(Q.shape[0])]
    df = pd.DataFrame(Q, columns=labels, index=labels)
    pd.set_option('display.max_rows', None)
    print(df.to_string())


if __name__ == "__main__":
    while True:
        try:
            dimensions = input('Enter maze dimensions separated by a space: ').split()
            dimension1, dimension2 = int(dimensions[0]), int(dimensions[1])
            if 0 < dimension1 and 0 < dimension2:
                break
            else:
                print("Maze dimensions cannot be 0.")
        except ValueError:
            print("Dimensions must be integers.")
        except IndexError:
            print("Please enter two numbers separated by a space.")

    while True:
        try:
            start = input('Enter x and y coordinates of the maze start separated by a space: ').split()
            start_x, start_y = int(start[0]), int(start[1])
            if start_x <= dimension1 and start_y <= dimension2:
                break
            else:
                print("Start coordinates should be inside the maze. Numbering is zero-based.")
        except ValueError:
            print("Start coordinates must be integers.")
        except IndexError:
            print("Please enter two numbers separated by a space.")

    while True:
        try:
            gamma = float(input('Enter the gamma value (0, 1]: '))
            if 0 < gamma <= 1:
                break
            else:
                print("Gamma should be a number between 0 and 1.")
        except ValueError:
            print("Gamma should be a number between 0 and 1.")

    while True:
        try:
            lrn_rate = float(input('Enter the learning rate value (0, 1]: '))
            if 0 < lrn_rate <= 1:
                break
            else:
                print("Learning rate should be a number between 0 and 1.")
        except ValueError:
            print("Learning rate should be a number between 0 and 1.")

    max_epochs = 1000

    # Create the Maze
    maze = Maze(dimension1, dimension2, [start_x, start_y])

    # Get the Feasibility Matrix
    feasibility = Feasibility(maze)

    # Initialize the agent:
    agent = Agent(feasibility, gamma, lrn_rate, maze, start_x, start_y)

    print("Analyzing maze with RL Q-learning")
    print("The F matrix:\n")
    my_print(feasibility.F_matrix)

    # Train the model:
    agent.train(feasibility.F_matrix, max_epochs)
    # train(feasibility.F_matrix, R_matrix, Q_matrix, gamma, lrn_rate, goal, n_states, max_epochs)
    print("Done ")

    print("The Q matrix is: \n ")
    my_print(agent.Q)

    print(f"Using Q to go from start to goal ({agent.goal})")

    agent.walk(maze, feasibility)
