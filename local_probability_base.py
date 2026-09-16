from battleshipdata import No6, No5, No4, No2_3, No1  # Defines ship specifications (length and width)
from chessboardgenerator import chessbroadplayergenerate  # Function to generate a blank chessboard
import random ,time # Standard libraries for time measurement, random number generation, and Excel writing
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.signal import cwt, ricker
import seaborn as sns
import scipy.stats as stats
import battleRelateFunction as ef
def ship_generator_ai1(long, tran, cBAI, direc,type,horizontalsize):
    cB = np.zeros([15, 15])
    max_attempts = 100
    attempt = 0
    ship_coordinates = []

    # Determine whether a valid position is found
    while attempt < max_attempts:
        attempt += 1
        valid = True # Assume the position is valid

        yy = len(cB) - random.randint(1, len(cB) - 1) - 1
        xx = random.randint(2, len(cB)) - 1

        # Coordinates and boundaries to determine whether the direction is allowed
        if direc == 0:  # Longitudinal Ship Generation
            for i in range(long):
                for j in range(tran):
                    if yy - i < 0 or xx + j > 14 or cBAI[yy - i][xx + j] != 0:
                        valid = False
                        break
                if not valid:
                    break

        elif direc == 1:  # Horizontal generation ship
            for i in range(tran):
                for j in range(long):
                    if yy - i < 0 or xx + j > 14 or cBAI[yy - i][xx + j] != 0:
                        valid = False
                        break
                if not valid:
                    break

        else:  # Alternate Direction
            for j in range(long):
                if xx + j > 14 or cBAI[yy][xx + j] != 0:
                    valid = False
                    break

        # If a valid position is found, fill the matrix
        if valid:
            if direc == 0:  # Longitudinal ship
                for i in range(long):
                    for j in range(tran):
                        cB[yy - i][xx + j] = 1
                        ship_coordinates.append((xx + j, yy - i))
                direction = "vertical"
            elif direc == 1:  # Horizontal Ship
                for i in range(tran):
                    for j in range(long):
                        cB[yy - i][xx + j] = 1
                        ship_coordinates.append((xx + j, yy - i))
                direction = "horizontal"
            else:  # spare
                for j in range(long):
                    cB[yy][xx + j] = 1
                    ship_coordinates.append((xx + j, yy))
                direction = "default"
            ships.append({"type": type, "coordinates": ship_coordinates,"direction": direction, "state": "Survive", "HorizontalSize": horizontalsize})
            return cB

    # If the maximum number of attempts is exceeded, None is returned, indicating that no valid location was found.
    return None
def generate():
    """
        Generates a complete game board with ships placed according to predefined sizes and types.

        Returns:
            2D array: The fully initialized game board with all ships placed.
        """
    ai1 = chessbroadplayergenerate()
    for i in range(0, 5):
        if i == 0:
            long, tran = No1.long, No1.width
            type_ship = "No.1"
            horizontalsize = No1.long
        elif i == 1 or i == 2:
            long, tran = No2_3.long, No2_3.width
            if i == 1:
                type_ship = "No.2"
            else:
                type_ship = "No.3"
            horizontalsize = No2_3.long
        elif i == 3:
            long, tran = No4.long, No4.width
            type_ship = "No.4"
            horizontalsize = No4.long
        elif i == 4:
            long, tran = No5.long, No5.width
            type_ship = "No.5"
            horizontalsize = No5.long
        elif i == 5:
            long, tran = No6.long, No6.width
            type_ship = "No.6"
        ai1 = ai1 + ship_generator_ai1(long, tran, ai1, random.randint(0, 1),type_ship,horizontalsize)
    return ai1


turns = []
for j in range(0,1):
    ships = []  # List to store ship information
    entropyBoard = chessbroadplayergenerate()
    playerBoard = chessbroadplayergenerate()
    flagg = 0
    cBg = generate()
    entropyBoard_Temporary = []
    entrolocal = []
    entroglbal = []
    probabilitylocal = []
    probabilityglobal = []
    x_hit = []
    y_hit = []
    ship_length = ef.get_ships_remaining_coordinates(ships) #change to update in each round
    print(ship_length)
    permutationH =[]
    permutationV = []
    ship_blocks = sum(ship_length)
    hit_times = 0
    blocks_remain = 196
    #main program
    for i in range(0, 196):

        while True:
            if not x_hit:
                ab, hit, x, y = ef.strikerandom(cBg,playerBoard)  # Attack a block
            else:
                ab, hit, x, y, flagg = ef.entropy_base_strik(entropyBoard,cBg,playerBoard)
            if ab == False:# If attack is valid (not mean hit)
                if hit == 1:
                    x_hit.append(x)
                    y_hit.append(y)
                    hit_times += 1
                print(f"HitPRINT{x_hit}")
                hit_coordinate = (x, y)
                break
            elif flagg == 1:
                break
            else:
                continue
        if flagg == 1:
            break
        print(f"player board:\n{playerBoard}")
        blocks_remain -= 1

        if hit == 1 or x_hit[:]:
            entropyBoard = chessbroadplayergenerate()
            permutationH = []
            permutationV = []
            for length in range(len(ship_length)):
                ef.permutaion_calculator(x_hit, y_hit, ship_length[length],playerBoard,permutationH,permutationV)
            permutationnnnn = sum(permutationH)+sum(permutationV)
            print(sum(permutationH)+sum(permutationV))
            print(permutationH,permutationV)
            for j in range(len(ship_length)):
                ef.numerator_calculator(x_hit, y_hit, ship_length[j], entropyBoard, permutationH[j], permutationV[j],
                                           playerBoard)

            print(f"numberator:\n{entropyBoard}")
            ef.calculate_probability_local(entropyBoard, permutationnnnn)
            print("---------probability----------")
            print(tabulate(entropyBoard, tablefmt="grid"))

        ship_type, nOrder = ef.update_ship_status(ships, hit_coordinate)
        if ship_type:
            ship_length[nOrder] = 0
            x_hit = []
            y_hit = []
            entropyBoard = chessbroadplayergenerate()
        if sum(ship_length) == 0:
            print(f"break turn: {i+1}")
            break
        print("----------------------entropy------------------------")

        H, entropyBoard_Temporary = ef.entropy_sum(entropyBoard)
        entrolocal.append(H)
        print(tabulate(entropyBoard_Temporary, tablefmt="grid"))
        entroglbal.append(ef.entropy_formula_g(ef.calculate_probability_global(ship_blocks, blocks_remain,hit_times)))
        print(f"ship_blocks: {ship_blocks} blocks_reamin: {blocks_remain} hit_time: {hit_times} turns: {i+1}")
    if flagg ==0:
        turns.append(i+1)


    if flagg == 0:
        print(len(entrolocal),len(entroglbal))
        print(entrolocal)
        print(entroglbal)
        ef.graph_output(entroglbal,'Global Entropy')
        ef.graph_output(entrolocal,'Local Entropy')
        ef.Wavelet_Transform_plot(entroglbal,"Global")
        ef.Wavelet_Transform_plot(entrolocal,"Local")
        ef.comparing(entroglbal, entrolocal)
#print(turns)
#normal_distribution(turns)