from battleshipdata import No6, No5, No4, No2_3, No1  # Defines ship specifications (length and width)
from chessboardgenerator import chessbroadplayergenerate  # Function to generate a blank chessboard
import random ,time # Standard libraries for time measurement, random number generation, and Excel writing
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.signal import cwt, ricker
import seaborn as sns
import scipy.stats as stats

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
def strikerandom(cB,cBp):
    import random
    xx = random.randint(1, len(cB) - 1)
    yy = random.randint(0, len(cB) - 2)
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
        cBe[:14, 1:15] = np.round(cBe[:14, 1:15]/ permu,2)
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
def entropy_base_strik(cBe,cB,cBp):
    subarray = cBe[:14, 1:15]  # Extract subarray
    local_max_index = np.unravel_index(np.argmax(subarray), subarray.shape) # Extract the maximum probability
    global_max_index = (local_max_index[0], local_max_index[1] + 1)
    y,x = global_max_index
    #print(f"max_d:{global_max_index}")
    if cB[y][x] == 0:
        cB[y][x] = -2
        cBp[y][x] = -2
        hit_b = 0
        return False, hit_b, x, y, 0
    elif cB[y][x] == 1:
        cB[y][x] = -1
        cBp[y][x] = -1
        hit_b = 1
        return False, hit_b, x, y, 0

    else:
        return True, 0, None, None, 1
def entropy_formula_g(p):
    if p > 0:
        return -(p*np.log2(p)+(1-p)*(np.log2(1-p)))
    else:
        return 0
def graph_output(lists, name='local/global'):#plot the entropy vs. turns graph
    x_positions = np.arange(len(lists))  # [0, 1, 2, ..., len(values)-1]


    plt.plot(x_positions, lists, marker="o", linestyle="-", label="Entropy")


    for i, (x, v) in enumerate(zip(x_positions, lists)):
        if name == 'Local Entropy':
            if v != 0:
                plt.text(x, v, f"{v:.2f}", fontsize=10, ha="right")
        else:
            if i % 5 == 0:
                plt.text(x, v, f"{v:.2f}", fontsize=10, ha="right")

    plt.xticks(np.arange(0, len(lists), 5))

    plt.xlabel("Turns")
    plt.ylabel(name)
    plt.title(f"Line Plot of {name} in a game")
    plt.legend()
    plt.grid()

    plt.show()
def Wavelet_Transform_plot(lists, name="local/global"):#Wavelet Transform for Entropy Analysis
    widths = np.arange(1, 50)  # Setting different scales
    cwt_matrix = cwt(lists, ricker, widths)  # Calculate wavelet transform
    l = len(lists)
    # Draw the time-frequency diagram of wavelet transform
    plt.figure(figsize=(10, 6))
    plt.imshow(cwt_matrix, aspect='auto', extent=[0, l, 1, 50], cmap='coolwarm', interpolation='bilinear')
    plt.xlabel("Round Number")
    plt.ylabel("Scale (Frequency)")
    plt.title(f"Wavelet Transform (CWT) of {name} entropy using Scipy")
    plt.colorbar(label="Coefficient Magnitude")
    plt.grid()
    plt.show()
def get_ships_remaining_coordinates(ships):
    """
    Count the remaining coordinates of each ship and return the result list

    parameter:
        ships (list[dict]): list of ships, each dictionary must contain the 'coordinates' key

    return:
        list[int]: A list of the remaining coordinates of each ship, in the same order as the input list

    Exception handling:
        - If a ship does not have a 'coordinates' key, the ship counts 0 and prints a warning
        - If coordinates is not a list/tuple, the ship counts 0 and prints a warning
    """
    remaining_counts = []

    for index, ship in enumerate(ships, start=1):
        try:
            # Check if coordinates key exists
            if 'coordinates' not in ship:
                raise KeyError(f"ship {index} lack 'coordinates' ")

            # Get coordinate data and verify the type
            coords = ship['coordinates']
            if not isinstance(coords, (list, tuple)):
                raise TypeError(f"ship's {index} coordinates type should be list/tuple，actual: {type(coords)}")

            # count the number of coordinates
            count = len(coords)
            remaining_counts.append(count)

        except (KeyError, TypeError) as e:
            print(f"warning: {str(e)}")
            remaining_counts.append(0)  # 0 = no data

    return remaining_counts
def normal_distribution(lists):
    from scipy.stats import norm

    # mean and standard deviation
    mu, sigma = np.mean(lists), np.std(lists)

    # Generate theoretical values for a normal distribution
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 100)
    y = norm.pdf(x, mu, sigma)

    # plot
    plt.figure(figsize=(10, 6), dpi=200)
    # KDE curve
    sns.kdeplot(lists, color='blue', label='KDE')

    # Normal distribution
    plt.plot(x, y, color='red', linestyle='dashed', linewidth=2, label='Normal Distribution')

    # Histogram
    plt.hist(lists, bins=30, density=True, alpha=0.3, color='gray', label='Histogram')

    plt.xlabel('Turns for a round')
    plt.ylabel('Value')
    plt.title('Probability Base Algorithm Normal Distribution Plot')
    plt.legend()

    plt.show()
def comparing(a,b):


    time = np.arange(len(a))
    a,b = np.array(a),np.array(b)

    fig, ax1 = plt.subplots(figsize=(10, 5))


    ax1.set_xlabel("Time (Rounds)")
    ax1.set_ylabel("Global Entropy", color="tab:blue")
    ax1.plot(time, a, label="Global Entropy", color="tab:blue", linestyle="-")
    ax1.tick_params(axis="y", labelcolor="tab:blue")


    ax2 = ax1.twinx()
    ax2.set_ylabel("Local Entropy", color="tab:red")
    ax2.plot(time, b, label="Local Entropy", color="tab:red", linestyle="--")
    ax2.tick_params(axis="y", labelcolor="tab:red")


    plt.title("Global vs Local Entropy over Time")


    fig.tight_layout()
    plt.show()


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
    ship_length = get_ships_remaining_coordinates(ships) #change to update in each round
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
                ab, hit, x, y = strikerandom(cBg,playerBoard)  # Attack a block
            else:
                ab, hit, x, y, flagg = entropy_base_strik(entropyBoard,cBg,playerBoard)
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
                permutaion_calculator(x_hit, y_hit, ship_length[length],playerBoard)
            permutationnnnn = sum(permutationH)+sum(permutationV)
            print(sum(permutationH)+sum(permutationV))
            print(permutationH,permutationV)
            for j in range(len(ship_length)):
                numerator_calculator(x_hit, y_hit, ship_length[j], entropyBoard, permutationH[j], permutationV[j],
                                           playerBoard)

            print(f"numberator:\n{entropyBoard}")
            calculate_probability_local(entropyBoard, permutationnnnn)
            print("---------probability----------")
            print(tabulate(entropyBoard, tablefmt="grid"))

        ship_type, nOrder = update_ship_status(ships, hit_coordinate)
        if ship_type:
            ship_length[nOrder] = 0
            x_hit = []
            y_hit = []
            entropyBoard = chessbroadplayergenerate()
        if sum(ship_length) == 0:
            print(f"break turn: {i+1}")
            break
        print("----------------------entropy------------------------")

        H, entropyBoard_Temporary = entropy_sum(entropyBoard)
        entrolocal.append(H)
        print(tabulate(entropyBoard_Temporary, tablefmt="grid"))
        entroglbal.append(entropy_formula_g(calculate_probability_global(ship_blocks, blocks_remain,hit_times)))
        print(f"ship_blocks: {ship_blocks} blocks_reamin: {blocks_remain} hit_time: {hit_times} turns: {i+1}")
    if flagg ==0:
        turns.append(i+1)


    if flagg == 0:
        print(len(entrolocal),len(entroglbal))
        print(entrolocal)
        print(entroglbal)
        graph_output(entroglbal,'Global Entropy')
        graph_output(entrolocal,'Local Entropy')
        Wavelet_Transform_plot(entroglbal,"Global")
        Wavelet_Transform_plot(entrolocal,"Local")
        comparing(entroglbal, entrolocal)
#print(turns)
#normal_distribution(turns)