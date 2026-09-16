from battleshipdata import No6, No5, No4, No2_3, No1  # Defines ship specifications (length and width)
from chessboardgenerator import chessbroadplayergenerate  # Function to generate a blank chessboard
import random ,time # Standard libraries for time measurement, random number generation, and Excel writing
import numpy as np  # Library for numerical calculations
import os
from tabulate import tabulate
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
def get_ship_coordinate_distribution(sh
import matplotlib.pyplot as pltips):
    """
    Count the number of surviving ships with at least k coordinates, and generate an array sorted in ascending order by k.
    Force counting to start at k=2, even if the actual minimum number of coordinates is less than 2.
    """
    # Screening for surviving ships (those that were not sunk)
    surviving_ships = [ship for ship in ships if ship["state"] == "Survive"]
    if not surviving_ships:
        return []

    # Get the coordinates of all surviving ships
    coord_counts = [ship["HorizontalSize"] for ship in surviving_ships]
    print(f"horizontal size: {coord_counts}")

    # Determine the level range: force it to start from k=2 to the maximum number of coordinates
    min_k = 2  # Forced to start from 2 according to demand
    max_k = max(coord_counts)

    # Generate a statistical array, each element represents the number of ships with at least k coordinates
    distribution = []
    for k in range(min_k, max_k + 1):
        count = sum(1 for cnt in coord_counts if cnt >= k)
        distribution.append(count)
    return distribution
playerBoard = chessbroadplayergenerate()
gBprobability = chessbroadplayergenerate()
ships = []
ship_length = [3,4,4,5,6]
permu = 0
def calculate_probability_local(cBe,permu):
    if permu != 0:
        cBe[:14, 1:15] = np.round(cBe[:14, 1:15]/ permu,10)
    return cBe
def entropy_sum(cBe):
    cBe_copy = cBe.copy()
    # Extract target sub-region
    target_region = cBe_copy[:14, 1:15]

    non_zero_mask = (target_region != 0)

    # Use np.clip to prevent probability values from exceeding [epsilon, 1-epsilon]
    epsilon = 1e-10  # Minimum value to avoid numerical errors
    clipped_values = np.clip(target_region[non_zero_mask], epsilon, 1 - epsilon)

    # Calculate entropy value (including positive and negative probabilities)
    entropy_values = -(
            clipped_values * np.log2(clipped_values) +
            (1 - clipped_values) * np.log2(1 - clipped_values)
    )

    entropy_values = np.round(entropy_values, 2)

    # Update target area
    target_region[non_zero_mask] = entropy_values

    # Total entropy calculation
    total_entropy = np.sum(entropy_values)

    return total_entropy, cBe_copy
def global_real_permuatations(ship_length,playerBoard,gBprobability):
    permutations = 0
    for i in range(1,15):
        for j in range(0,14):
            abbbx = 0
            abbby = 0
            x, y = i,j
            if playerBoard[y][x] == 0:
                if x + ship_length-1 <= 14:
                    for z in range(ship_length):
                        if playerBoard[y][x + z] == 0:
                            abbbx = 0
                        else:
                            abbbx = None
                            break
                    if abbbx == 0:
                        permutations += 1
                        for z in range (ship_length):
                            if playerBoard[y][x+z] == 0:
                                gBprobability[y][x+z] = gBprobability[y][x+z]+1
                            else:
                                break
                if y + ship_length - 1 <= 13:
                    for b in range(ship_length):
                        if playerBoard[y+b][x] == 0:
                            abbby = 0
                        else:
                            abbby = None
                            break
                    if abbby == 0:
                        permutations += 1
                        for b in range (ship_length):
                            if playerBoard[y+b][x] == 0:
                                gBprobability[y+b][x] = gBprobability[y+b][x] + 1
                            else:
                                break
    return gBprobability, permutations
def show_entropy_heatmap_region(gBprobability, title="Entropy Heatmap [Region 0:14,1:15]"):
    # 提取游戏有效区域 [0:14][1:15] → shape (14,14)
    sub_region = gBprobability[:14, 1:15]

    plt.figure(figsize=(8, 7))

    # 热力图，origin='upper' 让 y=14 在上方
    plt.imshow(sub_region, cmap='viridis', interpolation='nearest', origin='upper')

    # 添加颜色条
    plt.colorbar(label="Entropy Level")

    # 设置 x=1~14，y=14~1，符合常识坐标系
    plt.xticks(np.arange(14), labels=[str(i) for i in range(1, 15)])  # x轴为1~14
    plt.yticks(np.arange(14), labels=[str(14 - i) for i in range(14)])  # y轴为14~1

    # 在非零位置上标注数值
    for row in range(14):
        for col in range(14):
            val = sub_region[row][col]
            if val != 0:
                plt.text(col, row, f"{val:.5f}", ha='center', va='center', fontsize=7, color='white')

    plt.title(title, fontsize=14)
    plt.xlabel("X", fontsize=12)
    plt.ylabel("Y", fontsize=12)
    plt.grid(False)
    plt.tight_layout()
    plt.show()
def show_entropy_heatmap_region(
    gBprobability,
    title="Entropy Heatmap [Region 0:14,1:15]",
    save=False,
    round_number=None,
    folder="entropy_frames"
):
    # 提取有效区域 [0:14][1:15] → shape (14,14)
    sub_region = gBprobability[:14, 1:15]

    plt.figure(figsize=(8, 7))

    # 绘制热力图，origin='upper' 让 y=14 在上方
    plt.imshow(sub_region, cmap='viridis', interpolation='nearest', origin='upper')

    # 添加颜色条
    plt.colorbar(label="Entropy Level")

    # 设置坐标轴：x=1~14，y=14~1，模拟现实世界坐标
    plt.xticks(np.arange(14), labels=[str(i) for i in range(1, 15)])
    plt.yticks(np.arange(14), labels=[str(14 - i) for i in range(14)])

    # 在每个非零位置标注熵值
    for row in range(14):
        for col in range(14):
            val = sub_region[row][col]
            if val != 0:
                plt.text(col, row, f"{val:.5f}", ha='center', va='center', fontsize=7, color='white')

    plt.title(title, fontsize=14)
    plt.xlabel("X", fontsize=12)
    plt.ylabel("Y", fontsize=12)
    plt.grid(False)
    plt.tight_layout()

    # 保存功能
    if save and round_number is not None:
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, f"entropy_round_{round_number:03d}.png")
        plt.savefig(filename, bbox_inches='tight')
        plt.close()  # 不显示图，只保存
    else:
        plt.show()


for i in range(len(ship_length)):
    if ship_length[i] != 0:
        gBprobability, permutation = global_real_permuatations(ship_length[i],playerBoard,gBprobability)
        permu += permutation
        print(permu)
print(gBprobability)
calculate_probability_local(gBprobability,permu)
entropy_sum(gBprobability)
show_entropy_heatmap_region(gBprobability, "Entropy Distribution Thermal graph")
