"""
cube_data.py - Contains the cube state, color maps, face layout info,
and the conversion logic for Kociemba solving.
"""
from tkinter import *
from random import randint
import copy
import numpy as np
import kociemba

cube = {
        "U": np.full((3, 3), 'W'), 
        "D": np.full((3, 3), 'Y'),  
        "L": np.full((3, 3), 'O'), 
        "R": np.full((3, 3), 'R'), 
        "F": np.full((3, 3), 'G'), 
        "B": np.full((3, 3), 'B')  
}

faces_list = ["U", "D", "L", "R", "F", "B"]
origin_cube=copy.deepcopy(cube)

# Mapping cube letters to colors and Tkinter backgrounds
color_map = {
    'W': 'White',
    'Y': 'Yellow',
    'O': 'OrangeRed',
    'R': 'Red',
    'G': 'Green',
    'B': 'Blue'
}
face_to_color={
    'L':'O',
    'R':'R',    
    'U':'W',
    'D':'Y',
    'F':'G',
    'B':'B'
}
color_to_face={
    'W': 'U',  
    'Y': 'D',  
    'O': 'L',  
    'R': 'R', 
    'G': 'F',  
    'B': 'B'   
}

# Coordinates used for layout positioning in GUI
faces_color_map = {
    'U': color_map['W'],  # Up
    'D': color_map['Y'],  # Down
    'L': color_map['O'],  # Left
    'R': color_map['R'],  # Right
    'F': color_map['G'],  # Front
    'B': color_map['B']   # Back
}

faces_coordinates = {
    'U': (1,1),
    'D': (3,1),
    'L': (2,0),
    'R': (2,2),
    'F': (2,1),
    'B': (2,3),
}
color_coordinate = {
    'U': (1,0),
    'D': (1,1),
    'L': (1,2),
    'R': (2,0),
    'F': (2,1),
    'B': (2,2),
}

# List to store the solution moves and history of moves
solutionlist=[]
history_moves = []

def convert_to_kociemba(cube):
    """
    Converts the cube state to a Kociemba-formatted string and computes the solution.
    The solution is stored in history_moves using standard cube notation.
    """
    try:
        solutionlist.clear()
        history_moves.clear()
        
        kb_order = ['U', 'R', 'F', 'D', 'L', 'B']  #Kociemba order

        # Convert the cube to a Kociemba-compatible format
        kb_face_order = [cube[face].flatten() for face in kb_order]  
        kb_face_list = ''.join([''.join(color_to_face[color] for color in face) for face in kb_face_order])
        
        #check if already solved
        if kb_face_list=='UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB':
            history_moves.append("Cube already solved")
            return
        
        # Use Kociemba's algorithm to find the solution and store it in solutionList
        solution = kociemba.solve(kb_face_list,max_depth=20)
        for c in solution:
            if c == " ":
                continue
            solutionlist.append(c)

        #Parses the result into history_moves
        i=0
        while i<len(solutionlist):
            move=solutionlist[i]
            nextmove=solutionlist[i+1] if i+1 < len(solutionlist) else '' 
            if nextmove=="2"or nextmove=="'":
                history_moves.append(move+nextmove+'')
                i+=2
            else:
                history_moves.append(move)
                i+=1
        

    except ValueError as e:
        history_moves.append("Resolution Error: " + str(e))
    
        
    
    

    
