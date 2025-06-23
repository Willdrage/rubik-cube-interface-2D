"""
cube_ui.py - Main GUI interface for the Rubik's Cube.
Built with Tkinter. Handles cube display, color editing, user controls, and move execution.
"""
import tkinter as tk
from tkinter import END
from cube_data import color_coordinate, faces_color_map, faces_coordinates, faces_list, color_map, cube,face_to_color, history_moves
from cube_mouv import *
import time

root = tk.Tk()
root.title("Rubik's Cube")


class RubikApp():
    def __init__(self):
        self.selected_color = 'W' 
        self.allow_color_change = tk.BooleanVar()

        # Create the visual grid that holds all cube faces
        self.cube_frame = tk.Frame(root, bg='gray', padx=10, pady=10, bd=3, relief="solid")
        self.cube_frame.grid(row=0, column=0,rowspan=3, padx=(0,10), pady=(0,5))
        for row in range(3):
            self.cube_frame.grid_rowconfigure(row,weight=1)
        self.cube_frame.grid_columnconfigure(0,weight=6)
        for col in range(1,3):
            self.cube_frame.grid_columnconfigure(col,weight=2)

        self.labels = {}  # Stores references to each label for updating colors
        self.frames = {face: tk.Frame(self.cube_frame) for face in faces_list}
        self.init_cube()
        self.create_control()

        # User input entry for move history or manual move sequence
        self.movehistory=tk.Entry(root,bg="grey",font=("Arial", 16))
        self.movehistory.grid(row=4,sticky="ew",padx=5, pady=5)
        
    def init_cube(self):
        """
        Initializes the display of all 6 cube faces using colored Labels.
        Center labels are not interactive (face reference).
        """
        def create_face(frame, face):
            """
            create the 3*3 patern of a cube face.
            9 labels of face color.
            """
            for i in range(3):
                for j in range(3):
                    color = color_map[cube[face][i, j]] #map the letter to the color
                    label = tk.Label(frame, bg=color, width=8, height=4, borderwidth=2, relief="solid")
                    label.grid(row=i, column=j)
                    self.labels[(face, i, j)] = label  # Stock label for update
                    if not (i== 1 and j == 1):
                        # Bind the label to change color on click, except for the center label
                        label.bind("<Button-1>", lambda event, l=label,i=i,j=j,f=face: self.change_label_color(l,i,j,f))
                    

        for face in faces_coordinates: #create the 6 faces on different coordinates
            self.frames[face].grid(row=faces_coordinates[face][0], column=faces_coordinates[face][1])

        for face in faces_list: #create all labels
            create_face(self.frames[face], face)
            self.frames[face].grid_configure(padx=5, pady=5)

    def change_label_color(self, label, i, j, face):
        """
        Updates the cube data and label color when clicked (if color change is allowed).
        """
        if self.allow_color_change.get(): 
            label.config(bg=color_map[self.selected_color])
            cube[face][i, j] = self.selected_color
                                

    def history(self):
        """
        Displays the current move history (from cube_data.history_moves) in the entry.
        """
        self.movehistory.delete(0,END)
        self.movehistory.insert(0,history_moves)
   


    def create_control(self):
        """
        Builds all control buttons: scramble, reset, solve, manual moves.
        Rotation buttons call check_move() with clock direction.
        """
        def create_rotation_btn(frame,face,sup,bg,activebg,action,clock):
            def on_click():
                action(face, clock)
                self.update_faces()
            tk.Button(
                frame, 
                text=f"{face}{sup}",
                bg=bg, 
                activebackground=activebg,
                command=on_click,
                font=("Arial", 12),
                relief=tk.GROOVE, 
                width=5,height=2,bd=2, 
                ).grid(
                    row=faces_coordinates[face][0], 
                    column=faces_coordinates[face][1]
                    ) 
            
        def create_frame(parent, row, column, text):
            frame =tk.Frame(parent, 
                            bd=3,bg='gray', relief="solid", 
                            padx=5,pady=5, height=207,width=234)
            frame.grid(row=row, column=column, padx=(0, 5), pady=(0,5),sticky="nesw")
            frame.grid_propagate(False)
            tk.Label(frame,
                     text=text,bg='gray',font=("Arial", 18)
                     ).grid(row=0, column=0, columnspan=4, pady=5)
            return frame
        
        def change_selected_color(face):
            self.selected_color = face_to_color[face]
            colorlabel.config(bg=color_map[self.selected_color])

            
        # Configure rows and columns in the clock and counterclock frames
        clock_frame = create_frame(root, 0, 1, "Clockwise ↻")
        counterclock_frame = create_frame(root, 0, 2, "Counter ↺")

        
        
        # Create the main control frames
        control_frame = create_frame(root, 1, 1, "Controls")
        control_frame.grid_columnconfigure(0, weight=1)

        control_frame_2 = create_frame(root, 1, 2, "Controls 2")
        control_frame_2.grid_columnconfigure(0, weight=1) 

        # Configure rows in control_frame for buttons
        for row in range(1,4):
            control_frame.grid_rowconfigure(row, weight=1)
        for row in range(1,4):
            control_frame_2.grid_rowconfigure(row, weight=1)

        # Create buttons for cube controls
        tk.Button(control_frame, text="Scramble Cube", 
                  command=lambda: [scramble_cube(), self.update_faces(),self.history()]
                  ).grid(row=1,pady=0,sticky="nesw")
        
        tk.Button(control_frame, text="Reset Cube", 
                  command=lambda: [reset_cube(), self.update_faces(),self.history()]
                  ).grid(row=2,pady=0,sticky="nesw")
        
        tk.Button(control_frame, text="Kociemba Solution", 
                  command=lambda: [convert_to_kociemba(cube),self.history()]
                  ).grid(row=3,pady=0,sticky="nesw")

        tk.Button(control_frame_2, text="Move in label", 
                  command=lambda: [move_in_label(self.movehistory),self.update_faces()]
                  ).grid(row=1,pady=0,sticky="nesw")

        color_frame = create_frame(root, 2, 1, "Colors")
        for row in range(1,3):
            color_frame.grid_rowconfigure(row,weight=1)
        for col in range(3):
            color_frame.grid_columnconfigure(col,weight=1)

        # Create rotation and color selection buttons for each face
        for face in faces_list:
            create_rotation_btn(clock_frame,face,"",'#4CAF50',faces_color_map[face],check_move,1)
            create_rotation_btn(counterclock_frame,face,"\'",'#f44336',faces_color_map[face],check_move,-1)
            tk.Button(color_frame,
                      text=None,
                      bg=faces_color_map[face],activebackground=faces_color_map[face],
                      bd=2,
                      command=lambda f=face:change_selected_color(f)
                      ).grid(row=color_coordinate[face][0],column=color_coordinate[face][1],sticky="nesw")

        # Create buttons for color selection
        selected_color_frame = create_frame(root, 2, 2, "Selected color")
        selected_color_frame.grid_columnconfigure(0, weight=1)
        selected_color_frame.grid_rowconfigure(1, weight=9)
        selected_color_frame.grid_rowconfigure(2, weight=1)
        colorlabel=tk.Label(selected_color_frame,text=None,bg=color_map[self.selected_color])
        colorlabel.grid(row=1,column=0,sticky="nesw")
        tk.Checkbutton(selected_color_frame, text="Autorise color change",
               variable=self.allow_color_change, bg='gray', font=("Arial", 12)
               ).grid(row=2, pady=5, sticky="nesw")
     


        

        

    def update_faces(self):
        """
        Updates the GUI labels to reflect the current state of the cube data.
        """
        self.movehistory.configure(bg='grey')

        for face in faces_list:
            for i in range(3):
                for j in range(3):
                    self.labels[(face, i, j)].config(bg=color_map[cube[face][i, j]])
    
if __name__ == "__main__":
    app=RubikApp()
    root.mainloop()
    
