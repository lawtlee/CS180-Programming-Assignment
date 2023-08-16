import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.
    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.

    # By defualt we return False
    # TODO you should change this

    Memo = np.full([n,n,2,2], -1)

    Memo[0][0][0][0] = H

    for i in range(n):
        for j in range(n):

            left0, left1, left2, left3, top0, top1, top2, top3 = -1, -1, -1, -1, -1, -1, -1, -1

            if i == 0 and j == 0:
                continue
            if i > 0:
                ...
            if j > 0:
                left0 = Memo[i][j-1][0][0]
                left1 = Memo[i][j-1][0][1]
                left2 = Memo[i][j-1][1][1]
                left3 = Memo[i][j-1][1][0]
                if i > 0:
                    top0 = Memo[i-1][j][0][0]
                    top1 = Memo[i-1][j][0][1]
                    top2 = Memo[i-1][j][1][1]
                    top3 = Memo[i-1][j][1][0]
                if tile_types[i][j] == 0:
                    Memo[i][j][0][0] = max(max(left0, top0) - tile_values[i][j], top3, left3)
                    Memo[i][j][0][1] = max(top1,top2,left1,left2) - tile_values[i][j]
                    Memo[i][j][1][1] = max(left0, left2, top0, top2) - tile_values[i][j]
                    Memo[i][j][1][0] = max(max(left3, top3) - tile_values[i][j], left2, top2)
                if tile_types[i][j] == 1:
                    Memo[i][j][0][0] = max(left0, top0) + tile_values[i][j]
                    Memo[i][j][0][1] = max(top1,top2,left1,left2) + tile_values[i][j]
                    Memo[i][j][1][1] = max(left0, left2, top0, top2) + tile_values[i][j]
                    Memo[i][j][1][0] = max(left3, top3, left2, top2) + tile_values[i][j]
                if tile_types[i][j] == 2:
                    Memo[i][j][0][0] = max(left0, top0)
                    Memo[i][j][0][1] = max(top1,top2,left1,left2)
                    Memo[i][j][1][1] = max(left0, left2, top0, top2)
                    Memo[i][j][1][0] = max(left3, top3, left2, top2)
                if tile_types[i][j] == 3:
                    Memo[i][j][0][0] = max(left0, top0)
                    Memo[i][j][0][1] = max(top1,top2,left1,left2)
                    Memo[i][j][1][1] = max(left0, left2, top0, top2)
                    Memo[i][j][1][0] = max(left3, top3, left2, top2)


    return Memo[n-1][n-1][0][0] > 0 or Memo[n-1][n-1][0][1] > 0 or Memo[n-1][n-1][1][1] > 0 or Memo[n-1][n-1][1][0] > 0

def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
