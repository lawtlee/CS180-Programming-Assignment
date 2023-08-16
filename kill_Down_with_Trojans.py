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

    n = len(tile_types)

    # No token
    dp_h = [[-float('inf')] * n for _ in range(n)]
    # Protection token
    dp_h_p = [[-float('inf')] * n for _ in range(n)]
    # Multiplier token
    dp_h_m = [[-float('inf')] * n for _ in range(n)]
    # Both tokens
    dp_h_p_m = [[-float('inf')] * n for _ in range(n)]

    if H < 0:
        return False

    dp_h[0][0] = H
    

    for row in range(n):
        for col in range(n):
            v = tile_values[row][col]
            if row == 0 and col == 0:
                continue
            
            # Damage
            if tile_types[row][col] == 0:
                # Best health of no tokens = Previously no tokens or use protection token
                temp = max(dp_h[row - 1][col] - v, dp_h[row][col - 1] - v, dp_h_p[row - 1][col], dp_h_p[row][col - 1])
                dp_h[row][col] = temp if temp >= 0 else -float('inf')
                # Best health of only protection token = Protection token and choose not to use
                temp = max(dp_h_p[row - 1][col] - v, dp_h_p[row][col - 1] - v)
                dp_h_p[row][col] = temp if temp >= 0 else -float('inf')
                # Best health of only multiplier token = Previously multiplier token or had both and use protection token
                temp = max(dp_h_m[row - 1][col] - v, dp_h_m[row][col - 1] - v, dp_h_p_m[row - 1][col], dp_h_p_m[row][col - 1])
                dp_h_m[row][col] = temp if temp >= 0 else -float('inf')
                # Best health of having both tokens = previously have multiplier and protection tokens, and don't use
                temp =  max(dp_h_p_m[row - 1][col] - v, dp_h_p_m[row][col - 1] - v)
                dp_h_p_m[row][col] = temp if temp >= 0 else -float('inf')

            # Healing
            if tile_types[row][col] == 1:
                # Best health of no tokens = Previously no tokens or use multiplier token 
                dp_h[row][col] = max(dp_h[row - 1][col] + v, dp_h[row][col - 1] + v, dp_h_m[row - 1][col] + (v * 2), dp_h_m[row][col - 1] + (v * 2))
                # Best health of only multiplier token = Multiplier token and choose not to use
                dp_h_m[row][col] = max(dp_h_m[row - 1][col] + v, dp_h_m[row][col - 1] + v)
                # Best health of only protection token = Previously protection token or had both and use multiplier token
                dp_h_p[row][col] = max(dp_h_p[row - 1][col] + v, dp_h_p[row][col - 1] + v, dp_h_p_m[row - 1][col] + (v * 2), dp_h_p_m[row][col - 1] + (v * 2))
                # Best health of having both tokens = previously have multiplier and protection tokens, and don't use
                dp_h_p_m[row][col] = max(dp_h_p_m[row - 1][col] + v, dp_h_p_m[row][col - 1] + v)

            # Protection
            if tile_types[row][col] == 2:
                # Health of current tile with protection tile is just best health without protection tiles
                dp_h_p[row][col] = max(dp_h[row - 1][col], dp_h[row][col - 1], dp_h_p[row-1][col], dp_h_p[row][col-1])
                # Health of current tile with protection tile and multiplier tile is just best health with only multiplier tile
                dp_h_p_m[row][col] = max(dp_h_m[row - 1][col], dp_h_m[row][col - 1], dp_h_p_m[row-1][col], dp_h_p_m[row][col-1])
                 # Else no tokens = default 0
           
           # Multiplier
            if tile_types[row][col] == 3:
                # Health of current tile with multiplier tile is just best health without multiplier tiles
                dp_h_m[row][col] = max(dp_h[row - 1][col], dp_h[row][col - 1], dp_h_m[row-1][col], dp_h_m[row][col-1])
                # Health of current tile with multiplier tile and multiplier tile is just best health with only protection tile
                dp_h_p_m[row][col] = max(dp_h_p[row - 1][col], dp_h_p[row][col - 1], dp_h_p_m[row-1][col], dp_h_p_m[row][col-1])
                if row == 0 and col == 2:
                    print(dp_h[row][col-1])
                # Else no tokens = default 0

    return dp_h[-1][-1] >= 0 or dp_h_p[-1][-1] >= 0 or dp_h_p_m[-1][-1] >= 0 or dp_h_m[-1][-1] >= 0


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
