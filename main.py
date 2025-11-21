from maze import Maze
#from convert import Feasibility
from draw import draw_maze
import pandas as pd


# This function is needed to print a readable representation of the feasibility matrix.
def my_print(matrix):
    labels = [str(x) for x in range(matrix.shape[0])]
    df = pd.DataFrame(matrix, columns=labels, index=labels)
    pd.set_option('display.max_rows', None)
    print(df.to_string())


if __name__ == "__main__":
    while True:
        try:
            dimensions = input('Enter maze dimensions separated by a space: ').split()
            if len(dimensions) != 2:
                print("Please provide exactly two numbers for the maze dimensions.")
                continue
            dimension1, dimension2 = int(dimensions[0]), int(dimensions[1])
            if 0 < dimension1 and 0 < dimension2:
                break
            else:
                print("Maze dimensions cannot be 0.")
        except (ValueError, IndexError):
            print("Dimensions must be integers.")

    while True:
        try:
            start = input('Enter x and y coordinates of the maze start separated by a space: ').split()
            if len(start) != 2:
                print("Please provide exactly two numbers for the start coordinates.")
                continue
            start_x, start_y = int(start[0]), int(start[1])
            if 0 <= start_x < dimension1 and 0 <= start_y < dimension2:
                break
            else:
                print("Start coordinates should be inside the maze. Numbering is zero-based.")
        except (ValueError, IndexError):
            print("Start coordinates must be integers.")

    # Create the Maze
    maze = Maze(dimension1, dimension2, [start_x, start_y])

    # This will draw the maze and save it to the file maze.png
    draw_maze(maze)




