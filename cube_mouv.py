"""
cube_mouv.py - Handles cube logic: scramble, reset, and move transformations.
Applies real Rubik's Cube logic with correct face rotations and side effects.
"""

from cube_data import *
import numpy as np

def reset_cube():
    """
    Resets cube state to the original solved position.
    Clears history.
    """
    for face in cube:
        cube[face][:] = origin_cube[face]
    history_moves.clear()

def scramble_cube():
    """
    Applies a randomized sequence of 25-40 moves and logs them in history_moves.
    Uses standard notation with ' and 2 suffixes.
    """

    number_shuffle = randint(25,40)
    
    # create the move list for display
    history_moves.clear()
    for i in range(number_shuffle):
        alea_move = randint(0, 5)
        move = faces_list[alea_move]

        # random clock, anticlock and double move
        shuffle_type = randint(0, 4)
        if shuffle_type == 0:
            check_move(move, -1)
            history_moves.append(move + "'")
        elif shuffle_type == 4:
            check_move(move, 1)
            check_move(move, 1)
            history_moves.append(move + "2")
        else:
            check_move(move, 1)
            history_moves.append(move)
    
    return history_moves



def move_in_label(history):
    """
    Parses the move string from the entry, validates it,
    and applies moves sequentially if valid.
    Handles notation: single (R), inverse (R'), and double (R2).
    """

    moves=history.get().upper()
    valid_moves = ['U', 'D', 'F', 'R', 'B', 'L', ' ', "'", '2']

    v=0
    while v<len(moves):
        if moves[v] not in valid_moves:
            history.configure(bg='red')
            return
        v+=1
    i=0

    while i<len(moves):
        move=moves[i]
        next_move = moves[i+1] if i+1 < len(moves) else ''
        if move == ' ':
            i += 1
            continue
        if next_move==("'"):
            check_move(move, -1)
            i += 2
        elif next_move==("2"):
            check_move(move, 1)
            check_move(move, 1)
            i += 2
        else:
            check_move(move, 1)
            i += 1

def check_move(face,clock):
    """
    Selects the proper rotation function based on face and direction.
    Inverts direction internally to match numpy's .rot90 convention.
    Example: check_move('R', 1) will rotate the R face counterclockwise visually.
    """
    clock = -1 if clock == 1 else 1 
    face_moves = {
                'L': (rota_x, ['D', 'F', 'U', 'B'], [0, 2]),
                'R': (rota_x, ['U', 'F', 'D', 'B'], [2, 0]),
                'U': (rota_y, ['L', 'F', 'R', 'B'], 0),
                'D': (rota_y, ['R', 'F', 'L', 'B'], 2),
                'F': (rota_z, ['U', 'R', 'D', 'L'], [2, 0]),
                'B': (rota_z, ['U', 'R', 'D', 'L'], [0, 2])
            }

    if face in face_moves:
        func,adj_face,row_column=face_moves[face]
        #adj_face== list of the 4 adjacent faces affected by the rotation
        #row_column== list of adj_face row and column affected
        func(face,adj_face,row_column,clock)
    



def rota_x(face, adj_face, columns, clock):
    """
    Rotates the left/right face and shifts the adjacent face columns accordingly.
    """

    cube[face] = np.rot90(cube[face], clock) # 90° rotation of the face

    col1, col2 = columns[0], columns[1]

    # Copy the column from the first adjacent face to a temporary slice
    temp_slice = cube[adj_face[0]][:, col1].copy()

    if clock == -1: 
        # Rotate counterclockwise
        # Shift slices of adjacent faces
        cube[adj_face[0]][:, col1] = cube[adj_face[1]][:, col1]
        cube[adj_face[1]][:, col1] = cube[adj_face[2]][:, col1]
        cube[adj_face[2]][:, col1] = np.flip(cube[adj_face[3]][:, col2])
        cube[adj_face[3]][:, col2] = np.flip(temp_slice)
    else:
        # Rotate clockwise
        # Shift slices of adjacent faces
        cube[adj_face[0]][:, col1] = np.flip(cube[adj_face[3]][:, col2])
        cube[adj_face[3]][:, col2] = np.flip(cube[adj_face[2]][:, col1])
        cube[adj_face[2]][:, col1] = cube[adj_face[1]][:, col1]
        cube[adj_face[1]][:, col1] = temp_slice

def rota_y(face, adj_face, row, clock):
    """
    Rotates the up/down face and shifts the adjacent face rows accordingly.
    """

    cube[face] = np.rot90(cube[face], clock) # 90° rotation of the face

    # Copy the row from the first adjacent face to a temporary slice
    temp_slice = cube[adj_face[0]][row, :].copy()

    if clock == -1:
        # Rotate counterclockwise
        # Shift slices of adjacent faces
        cube[adj_face[0]][row, :] = cube[adj_face[1]][row, :]
        cube[adj_face[1]][row, :] = cube[adj_face[2]][row, :]
        cube[adj_face[2]][row, :] = cube[adj_face[3]][row, :]
        cube[adj_face[3]][row, :] = temp_slice
    else:
        # Rotate clockwise
        # Shift slices of adjacent faces
        cube[adj_face[0]][row, :] = cube[adj_face[3]][row, :]
        cube[adj_face[3]][row, :] = cube[adj_face[2]][row, :]
        cube[adj_face[2]][row, :] = cube[adj_face[1]][row, :]
        cube[adj_face[1]][row, :] = temp_slice



def rota_z(face, adj_face, row_col, clock):
    """
    Rotates the front/back face and handles row/column shifts across adjacent sides.
    Special case: back face rotation needs flip to maintain correct orientation.
    """

    cube[face] = np.rot90(cube[face], clock) # 90° rotation of the face

    rc1, rc2 = row_col[0], row_col[1]

    # Copy the row from the first adjacent face to a temporary slice
    temp_slice = cube[adj_face[0]][rc1, :].copy()

    # Special case for handling the back face clockwise rotation, Back face is inversed
    if (face == 'F' and clock == -1) or (face == 'B' and clock == 1):
        # Rotate counterclockwise for F, clock for B
        # Shift slices of adjacent faces
        cube[adj_face[0]][rc1, :] = np.flip(cube[adj_face[3]][:, rc1])
        cube[adj_face[3]][:, rc1] = cube[adj_face[2]][rc2, :]
        cube[adj_face[2]][rc2, :] = np.flip(cube[adj_face[1]][:, rc2])
        cube[adj_face[1]][:, rc2] = temp_slice
    else:
        # Rotate clockwise for F, counter for B
        # shift slices of adjacent faces
        cube[adj_face[0]][rc1, :] = cube[adj_face[1]][:, rc2]
        cube[adj_face[1]][:, rc2] = np.flip(cube[adj_face[2]][rc2, :])
        cube[adj_face[2]][rc2, :] = cube[adj_face[3]][:, rc1]
        cube[adj_face[3]][:, rc1] = np.flip(temp_slice)


