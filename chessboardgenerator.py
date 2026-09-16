def chessbroadplayergenerate():
    import numpy as np
    cB = np.zeros([15, 15])
    for i in range(1, 15):
        cB[i - 1][0] = 15 - i
        cB[14][i] = i
    return cB

def chessbroadplayergenerate10():
    import numpy as np
    cB = np.zeros([11, 11])
    for i in range(1, 11):
        cB[i - 1][0] = 11 - i
        cB[10][i] = i
    return cB
