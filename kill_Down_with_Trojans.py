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

    Memo = [[None] * n for i in range(n)]

    def helper(n, row, col, H, tile_types, tile_values, protection, multiplier):
        if H < 0:
            return False
        if row == n or col == n:
            return False
        if row == n - 1 and col == n - 1:
            if (tile_types[row][col] == 0 and H - tile_values[row][col] < 0):
                Memo[row][col] = False
            else:
                Memo[row][col] = True
            return Memo[row][col]
        if Memo[row][col] is not None:
            return Memo[row][col]
        
        if tile_types[row][col] == 0:
            opt1 = helper(n, row, col + 1, H - tile_values[row][col] * (not protection), tile_types, tile_values, False, multiplier) \
                or helper(n, row + 1, col, H - tile_values[row][col] * (not protection), tile_types, tile_values, False, multiplier)
            opt2 = False
            if protection:
                opt2 = helper(n, row, col + 1, H - tile_values[row][col], tile_types, tile_values, True, multiplier) \
                or helper(n, row + 1, col, H - tile_values[row][col], tile_types, tile_values, True, multiplier)
            Memo[row][col] = opt1 or opt2

        elif tile_types[row][col] == 1:
            opt1 = helper(n, row, col + 1, H + tile_values[row][col] * (multiplier * 2), tile_types, tile_values, protection, 0) \
                or helper(n, row + 1, col, H + tile_values[row][col] * (multiplier * 2), tile_types, tile_values, protection, 0)
            opt2 = False
            if multiplier:
                opt2 = helper(n, row, col + 1, H + tile_values[row][col], tile_types, tile_values, protection, multiplier) \
                    or helper(n, row + 1, col, H + tile_values[row][col], tile_types, tile_values, protection, multiplier)
            Memo[row][col] = opt1 or opt2

        elif tile_types[row][col] == 2:
            Memo[row][col] = helper(n, row, col + 1, H, tile_types, tile_values, True, multiplier) \
                or helper(n, row + 1, col, H, tile_types, tile_values, True, multiplier)

        elif tile_types[row][col] == 3:
            Memo[row][col] = helper(n, row, col + 1, H, tile_types, tile_values, protection, True) \
                or helper(n, row + 1, col, H, tile_types, tile_values, protection, True)
        return Memo[row][col]

    return helper(n, 0, 0, H, tile_types, tile_values, False, False)


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
