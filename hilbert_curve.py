from driver import AxiCLI
import numpy as np

def rotate(centered_array, orientation):
    rotate_mat = np.array([
        [0, -1],
        [1,  0],
    ])
    result = centered_array
    for _ in range(orientation):
        result = result @ rotate_mat
    return result

def corners_for_piece(center, orientation, length):
    # rotates pi / 2 left
    rotate_mat = np.array([
        [0, -1],
        [1,  0],
    ])
    # centered around 0
    corners = np.array([
        [-length, -length],
        [-length,  length],
        [ length,  length],
        [ length, -length],
    ]) / 2
    # re-center
    corners = rotate(corners, orientation) + np.array(center)
    return list(map(tuple, [corners[0], corners[1], corners[2], corners[3]]))

def iterate(center, orientation, length, depth = 0):
    if depth == 0:
        return corners_for_piece(center, orientation, length)

    edge_length = length / 2
    centers = np.array([
        [-length, -length],
        [-length,  length],
        [ length,  length],
        [ length, -length],
    ]) / 2

    centers = rotate(centers, orientation) + np.array(center)
    corners = []
    corners += list(reversed(iterate(centers[0], 1 + orientation, edge_length, depth = depth - 1)))
    corners +=               iterate(centers[1], 0 + orientation, edge_length, depth = depth - 1)
    corners +=               iterate(centers[2], 0 + orientation, edge_length, depth = depth - 1)
    corners += list(reversed(iterate(centers[3], 3 + orientation, edge_length, depth = depth - 1)))
    return corners

height, width = 3600, 3600
center = (height / 2, width / 2)
axi = AxiCLI()

for i in range(4):
    corners = iterate(center, 2, width / 3, depth = i)
    deltas = [(int(corners[i+1][0]-corners[i][0]), int(corners[i+1][1]-corners[i][1])) for i in range(len(corners)-1)]
    # move from center to first corner
    axi.line(int(corners[0][0] - center[0]), int(corners[0][1] - center[1]))
    axi.pen_down()
    for delta in deltas:
        axi.line(*delta)
    axi.pen_up()
    axi.line(int(center[0] - corners[-1][0]), int(center[1] - corners[-1][1]))
axi.close()
