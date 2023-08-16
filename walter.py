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
    if n <=0:
        return False
    if H <=0:
        return False
    hp=np.full([n,n],0, dtype=int) #initialize hp memo
    protection=np.full([n,n], False) #initialize protection memo, if we can get to a spot with protection
    multiplier=np.full([n,n], False) #intiialize multiplier memo
    maxProt=np.full([n,n], 0) #max amount of damage taken that we could heal for while we have a token
    maxMult=np.full([n,n],0) # max amoutn of heal gained that we could heal for a certain segment
    hp[0][0]=H
    print(hp[0][0])
    for i in range(0,n):
        for j in range(0,n):
            if i == 0 and j == 0:
                continue
            upOption=np.NINF
            leftOption=np.NINF
            if i != 0:
                upOption=hp[i-1][j]
                if protection[i-1][j]:
                    upOption+=maxProt[i-1][j]
                if multiplier[i-1][j]:
                    upOption+=maxMult[i-1][j]
            if j != 0:
                leftOption=hp[i][j-1]
                if protection[i][j-1]:
                    leftOption+=maxProt[i][j-1]
                if multiplier[i][j-1]:
                    leftOption+=maxMult[i][j-1]
            if leftOption>upOption:
                hp[i][j]=hp[i][j-1]
                multiplier[i][j]=multiplier[i][j-1]
                protection[i][j]=protection[i][j-1]
                maxProt[i][j]=maxProt[i][j-1]
                maxMult[i][j]=maxMult[i][j-1]
            else:
                hp[i][j]=hp[i-1][j]
                multiplier[i][j]=multiplier[i-1][j]
                protection[i][j]=protection[i-1][j]
                maxProt[i][j]=maxProt[i-1][j]
                maxMult[i][j]=maxMult[i-1][j]
            tile=tile_types[i][j]
            value=tile_values[i][j]
            if tile == 0:
                if protection[i][j]:
                    maxProt[i][j]=max(maxProt[i][j],value) #ony update if we have powerup
                else:
                    maxProt[i][j]=-0
                hp[i][j]-=value
                if hp[i][j]<=0: #if need to use powerup use the larger one
                    if protection[i][j] and multiplier[i][j]:
                        if hp[i][j]+max(maxProt[i][j], maxMult[i][j]) <=0: #one is not enough
                            hp[i][j]+=maxProt[i][j]+maxMult[i][j]
                            protection[i][j]=False
                            multiplier[i][j]=False
                            maxProt[i][j]=0
                            maxMult[i][j]=0
                        elif maxProt[i][j]>maxMult[i][j]: #larger one
                            hp[i][j]+=maxProt[i][j]
                            protection[i][j]=False
                            maxProt[i][j]=0
                        else:
                            hp[i][j]+=maxMult[i][j]
                            multiplier[i][j]=False
                            maxMult[i][j]=0
                    elif protection[i][j]:
                        hp[i][j]+=maxProt[i][j]
                        protection[i][j]=False
                        maxProt[i][j]=0
                    elif multiplier[i][j]:
                        hp[i][j]+=maxMult[i][j]
                        multiplier[i][j]=False
                        maxMult[i][j]=0
                    if hp[i][j] == 0:
                        hp[i][j]=-10000000 #no matter what we did we still died
            elif tile == 1:
                hp[i][j]=hp[i][j]+value
                if multiplier[i][j]:
                    maxMult[i][j]=max(maxMult[i][j], value)
                else:
                    maxMult[i][j]=0
            elif tile == 2:
                if protection[i][j]: #to maximize use we consume the protection for max health
                    hp[i][j]+=maxProt[i][j]
                    maxProt[i][j]=0
                protection[i][j]=True
            elif tile == 3:
                if multiplier[i][j]:
                    hp[i][j]+=maxMult[i][j]
                    maxMult[i][j]=0
                multiplier[i][j]=True
    return hp[n-1][n-1]>0


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
