from battleshipdata import No6, No5, No4, No2_3, No1  # Defines ship specifications (length and width)
from chessboardgenerator import chessbroadplayergenerate  # Function to generate a blank chessboard
import random ,time # Standard libraries for time measurement, random number generation, and Excel writing
import numpy as np  # Library for numerical calculations
from tabulate import tabulate
import matplotlib.pyplot as plt
import os
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
def update_ship_status(ships, hit_coordinate):
    """
        Updates the status of ships based on a hit coordinate.

        Parameters:
            ships (list): List of ships with their types and coordinates.
            hit_coordinate (tuple): The coordinate of the hit.

        Returns:
            str or None: The type of the ship sunk if applicable, otherwise None.
        """
    index = None
    for ship in ships:
        if hit_coordinate in ship["coordinates"]:
            ship["coordinates"].remove(hit_coordinate)
            if not ship["coordinates"]:  # if the coordinate of ship is empty
                ship["state"] = "sunk"
                print(f"Ship of type {ship['type']} has been {ship['state']}!")
                print(f"Direction of the sunk ship: {ship['direction']}")  # output direction
                ship["direction"] = None
                for i, sub_element in enumerate(ships):
                    print(f"sub element:{sub_element}")
                    print(f"ship type:{ship['type']}")
                    if ship['type'] == sub_element['type']:
                        index = i
                return ship["type"], index  # return ship type
    return None,None
def count_ship_directions(ships):
    horizontal_count = 0
    vertical_count = 0

    for ship in ships:
        if ship["direction"] == "horizontal":
            horizontal_count += 1
        elif ship["direction"] == "vertical":
            vertical_count += 1

    return horizontal_count, vertical_count
def get_ship_coordinate_distribution(ships):
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
def calculate_probability_global(ship_blocks, block_remain,hit_times):
    return (ship_blocks-hit_times) / block_remain
def permutaion_calculator(x_hit, y_hit,length,cBp):
    """
        Calculates possible ship placements based on hit coordinates.

        Parameters:
        - x_hit: List of x-coordinates where the ship has been hit.
        - y_hit: List of y-coordinates where the ship has been hit.
        - length: The required length of the ship.
        - cBp: 2D array representing the game board (0 = empty, other values = occupied).

        Returns:
        - The number of valid ship placements.
        """

    # Sort x and y coordinates to ensure structured processing
    x_hit.sort()
    y_hit.sort()

    # Initialize blocks (available spaces for ship placement)
    blocks = 0

    # If not enough hits are recorded, assume all hit positions are part of the ship
    if len(x_hit) < length:
        blocks = len(x_hit)

    # Initialize permutation counter (valid placements)
    permutation = 0

    # Define the front and back of the known hit area
    x_back, x_front = x_hit[-1], x_hit[0]

    # Ensure valid range check
    if x_hit[-1] != x_hit[0] or len(x_hit) == 1:
        for i in range(length - len(x_hit)):  # Check how much space remains
            # Check spaces to the right (+ direction)
            if x_back + (i + 1) < 15:  # Ensure within board limits
                if cBp[y_hit[-1]][x_back + (i + 1)] == 0:  # Check if space is unoccupied
                    blocks += 1
                else:
                    x_back = 10000  # Stop checking further right if blocked
            else:
                x_back = 10000  # Out of bounds

            # Check spaces to the left (- direction)
            if x_front - (i + 1) > 0:  # Ensure within board limits
                if cBp[y_hit[0]][x_front - (i + 1)] == 0:  # Check if space is unoccupied
                    blocks += 1
                else:
                    x_front = -10000  # Stop checking further left if blocked
            else:
                x_front = -10000  # Out of bounds

        # If enough space is available, calculate permutations
        if blocks >= length and length != 0:
            permutation = blocks - length + 1  # Number of valid horizontal placements

    # Store the number of horizontal permutations
    permutationH.append(permutation)

    # Reset variables for vertical check
    blocks = 0
    permutation = 0

    # Similar check for vertical placements
    if len(x_hit) < length:
        blocks = len(x_hit)

    y_back, y_front = y_hit[-1], y_hit[0]

    if y_hit[-1] != y_hit[0] or len(x_hit) == 1:
        for i in range(length - len(x_hit)):  # Check vertical spaces
            # Check downward (+ direction)
            if y_back + (i + 1) < 14:  # Ensure within board limits
                if cBp[y_back + (i + 1)][x_hit[-1]] == 0:  # Check if space is unoccupied
                    blocks += 1
                else:
                    y_back = 10000  # Stop checking further down if blocked
            else:
                y_back = 10000  # Out of bounds

            # Check upward (- direction)
            if y_front - (i + 1) >= 0:  # Ensure within board limits
                if cBp[y_front - (i + 1)][x_hit[0]] == 0:  # Check if space is unoccupied
                    blocks += 1
                else:
                    y_front = -10000  # Stop checking further up if blocked
            else:
                y_front = -10000  # Out of bounds

        # If enough space is available, calculate permutations
        if blocks >= length and length != 0:
            permutation += blocks - length + 1  # Number of valid vertical placements
            #print(f"permuV: {permutation}")  # Debugging output

    # Store the number of vertical permutations
    permutationV.append(permutation)

    return permutation
def numerator_calculator(x_hit, y_hit, length, cBentropy,permutationH,permutationV,playerCB):
    """Calculate the probability weight (entropy value) of a specific area on the board

    Parameters:
    x_hit (list): a set of x-coordinates of hit points (need to be sorted)
    y_hit (list): a set of y-coordinates of hit points (need to be sorted)
    length (int): target unit length (such as ship length)
    cBentropy (list): cumulative probability matrix (will be modified)
    permutationH (int): number of horizontal possibilities
    permutationV (int): number of vertical possibilities
    playerCB (list): player board state matrix, including:
    -2: detected no target
    -1: obstacle/unavailable
    0: not detected
    others: hit

    Return:
    list: updated cumulative probability matrix
    """
    state = 0 # Status flag used to control boundary search

    x_hit.sort()
    y_hit.sort()
    x_far = x_hit[0] # Take the leftmost hit point
    y_far = y_hit[0] # Take the top hit point
    #Horizontal:
    # Check if horizontal expansion is needed (hit points are discontinuous or single hit)
    if x_hit[-1] != x_hit[0] or len(x_hit) == 1:
        # Look for free space to the left (maximum expansion space = ship length - number of hit points)
        for i in range(length - len(x_hit)):
            # Check whether the left grid is available (must satisfy: state is 0 and coordinates>0)
            if playerCB[y_hit[0]][x_hit[0]-1-i] == 0 and x_hit[0]-1-i > 0 and state == 0:
                x_far = x_hit[0]-1-i # Update the left margin
            else:
                state = 1

        # Update the probability matrix based on the permutation possibility
        for j in range(permutationH):
            # Iterate through the possible horizontal positions that the ship can occupy
            for k in range(length):
                if playerCB[y_hit[0]][x_far + k] != -2 and playerCB[y_hit[0]][x_far + k] != -1:
                    cBentropy[y_hit[0]][x_far + k] += 1
            x_far += 1 # Move right one unit to try the next permutation
    state = 0
    #vertical: (same algorithm)
    if y_hit[-1] != y_hit[0] or len(x_hit) == 1:
        for i in range(length - len(x_hit)):
            if playerCB[y_hit[0] - 1 - i][x_hit[0]] == 0 and y_hit[0] - 1 - i > -1 and state == 0:
                y_far = y_hit[0] - 1 - i
            else:
                state = 1
        for j in range(permutationV):
            for k in range(length):
                if playerCB[y_far+k][x_hit[0]] != -2 and playerCB[y_far +k][x_hit[0]] != -1:
                    cBentropy[y_far+k][x_hit[0]] += 1
            y_far += 1
    return cBentropy
def calculate_probability_local(cBe,permu):
    if permu != 0:
        cBe[:14, 1:15] = np.round(cBe[:14, 1:15]/ permu,5)
    return cBe
def entropy_formula(cBe):
    # Extract target sub-region
    target_region = cBe[:14, 1:15]

    # Create a mask of nonzero elements
    non_zero_mask = (target_region != 0)

    # Calculate entropy only for non-zero elements
    target_region[non_zero_mask] = np.round(-target_region[non_zero_mask] * np.log2(target_region[non_zero_mask]),2)

    return cBe
def entropy_sum(cBe):
    cBe_copy = cBe.copy()
    # Extract target sub-region
    target_region = cBe_copy[:14, 1:15]

    non_zero_mask = (target_region != 0)

    # Use np.clip to prevent probability values from exceeding [epsilon, 1-epsilon]
    epsilon = 1e-10 # Minimum value to avoid numerical errors
    clipped_values = np.clip(target_region[non_zero_mask], epsilon, 1 - epsilon)

    # Calculate entropy value (including positive and negative probabilities)
    entropy_values = -(
            clipped_values * np.log2(clipped_values) +
            (1 - clipped_values) * np.log2(1 - clipped_values)
    )

    entropy_values = np.round(entropy_values, 5)

    # Update target area
    target_region[non_zero_mask] = entropy_values

    # Total entropy calculation
    total_entropy = np.sum(entropy_values)

    return cBe_copy
def get_ships_remaining_coordinates(ships):
    """
    统计每只船剩余坐标数量并返回结果列表

    参数:
        ships (list[dict]): 船只列表，每个字典需包含'coordinates'键

    返回:
        list[int]: 每只船剩余坐标数量的列表，顺序与输入列表一致

    异常处理:
        - 如果船只没有'coordinates'键，该船计数为0并打印警告
        - 如果coordinates不是列表/元组，该船计数为0并打印警告
    """
    remaining_counts = []

    for index, ship in enumerate(ships, start=1):
        try:
            # 检查是否存在coordinates键
            if 'coordinates' not in ship:
                raise KeyError(f"船只 {index} 缺少 'coordinates' 字段")

            # 获取坐标数据并验证类型
            coords = ship['coordinates']
            if not isinstance(coords, (list, tuple)):
                raise TypeError(f"船只 {index} 的coordinates类型应为list/tuple，实际是 {type(coords)}")

            # 统计坐标数量
            count = len(coords)
            remaining_counts.append(count)

        except (KeyError, TypeError) as e:
            print(f"警告: {str(e)}")
            remaining_counts.append(0)  # 用0表示无效数据

    return remaining_counts
def player_strike(cB,cBp):
    xx = int(input("enter a x coodinate"))
    yy = 14- int(input("enter a y coodinate"))
    if xx > 14 or xx < 1 or yy > 13 or yy < 0:
        return True, 0, None, None
    if cB[yy][xx] == 0:
        cB[yy][xx] = -2
        cBp[yy][xx] = -2
        hit_b = 0
        return False, hit_b, xx, yy
    elif cB[yy][xx] == 1:
        cB[yy][xx] = -1
        cBp[yy][xx] = -1
        hit_b = 1
        return False, hit_b, xx, yy

    else:
        return True, 0, None, None
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
def suggest_entropy_strike(cBe):
    # 提取有效区域
    subarray = cBe[:14, 1:15]

    # 找最大值
    max_value = np.max(subarray)

    # 找到所有最大值位置（局部）
    local_max_indices = np.argwhere(subarray == max_value)

    suggestions = []

    print(f"建议打击坐标（熵值最大为 {max_value:.5f}）：")

    for row, col in local_max_indices:
        # 将 row 映射为符合常识坐标的 Y 值：第 0 行是 y=14，第 13 行是 y=1
        y_coord = 14 - row
        # 将 col 映射为 X 值（第 1 列是 x=1）
        x_coord = col + 1
        suggestions.append((x_coord, y_coord))
        print(f" -> 坐标: ({x_coord}, {y_coord})")

    return suggestions
def show_entropy_heatmap_region(
    gBprobability,
    title="Entropy Heatmap (Magnified 1000 times)",
    save=False,
    round_number=None,
    folder="entropy_frames"
):
    # 提取有效区域 [0:14][1:15] → shape (14,14)
    sub_region = gBprobability[:14, 1:15]

    plt.figure(figsize=(8, 7),dpi=300)

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
ships = []  # List to store ship information
ProbabilityBoard = chessbroadplayergenerate()
playerBoard = chessbroadplayergenerate()
flagg = 0
cBg = generate()
print(cBg)
entropyBoard_Temporary = []
entrolocal = []
entroglbal = []
probabilitylocal = []
probabilityglobal = []
x_hit = []
y_hit = []
ship_length = get_ships_remaining_coordinates(ships) #change to update in each round
print(ship_length)
permutationH =[]
permutationV = []
ship_blocks = sum(ship_length)
hit_times = 0
blocks_remain = 196
permuuu = 0
for i in range(len(ship_length)):
    ProbabilityBoard, permutations = global_real_permuatations(ship_length[i], playerBoard, ProbabilityBoard)
    permuuu += permutations
    calculate_probability_local(ProbabilityBoard, permuuu)
print(tabulate(ProbabilityBoard, tablefmt="grid"))
for i in range(0,196):
    turnssss = i + 1
    print(f"player board:\n{playerBoard}")
    while True:
        suggest_entropy_strike(ProbabilityBoard)
        ab, hit, x, y = player_strike(cBg,playerBoard)
        if ab == False:
            if hit == 1:
                x_hit.append(x)
                y_hit.append(y)
            print(f"HitPRINT{x_hit}")
            hit_coordinate = (x, y)
            break
        else:
            print("Invalid input")
            continue
    if hit == 1 or x_hit[:]:
        ProbabilityBoard = chessbroadplayergenerate()
        permutationH = []
        permutationV = []
        for length in range(len(ship_length)):
            permutaion_calculator(x_hit, y_hit, ship_length[length], playerBoard)
        permutationnnnn = sum(permutationH) + sum(permutationV)
        print(sum(permutationH) + sum(permutationV))
        print(permutationH, permutationV)
        for j in range(len(ship_length)):
            numerator_calculator(x_hit, y_hit, ship_length[j], ProbabilityBoard, permutationH[j], permutationV[j], playerBoard)
        print(f"numberator:\n{ProbabilityBoard}")
        calculate_probability_local(ProbabilityBoard, permutationnnnn)
        print("---------probability----------")
        print(tabulate(ProbabilityBoard, tablefmt="grid"))
        ship_type, nOrder = update_ship_status(ships, hit_coordinate)
        if ship_type:
            ship_length[nOrder] = 0
            x_hit = []
            y_hit = []
            for i in range(len(ship_length)):
                if ship_length[i] != 0:
                    ProbabilityBoard, permutations = global_real_permuatations(ship_length[i], playerBoard, ProbabilityBoard)
                    permuuu += permutations
            calculate_probability_local(ProbabilityBoard, permuuu)
        if sum(ship_length) == 0:
            print(f"break turn: {turnssss}")
            break
        print("----------------------entropy------------------------")

        entropyBoard_Temporary = entropy_sum(ProbabilityBoard)
        print(tabulate(entropyBoard_Temporary, tablefmt="grid"))
    else:
        permuuu = 0
        ProbabilityBoard = chessbroadplayergenerate()
        entropyBoard = chessbroadplayergenerate()
        for i in range(len(ship_length)):
            if ship_length[i] != 0:
                ProbabilityBoard,permutations = global_real_permuatations(ship_length[i], playerBoard, ProbabilityBoard)
                permuuu += permutations
            print(permuuu)
        calculate_probability_local(ProbabilityBoard, permuuu)
        entropyBoard = entropy_sum(ProbabilityBoard)
        show_entropy_heatmap_region(
            entropyBoard,
            title="Entropy Heatmap [Region 0:14,1:15]",
            save=True,
            round_number=turnssss,
            folder="entropy_frames2"
        )
        print("---------entropyBoard----------")
        print(tabulate(entropyBoard, tablefmt="grid"))
