# 🧩 Rubik's Cube Simulator (Tkinter)

This is a personal project I made while learning Python (about 1–2 months of experience).  
It's a basic 3x3 Rubik's Cube simulator with a GUI built using **Tkinter**, and includes:

- Manual face rotation via buttons  
- Scrambling with random moves  
- Reset to solved state  
- Kociemba-based solver (with external `kociemba` library)  
- Editable face stickers for custom states

> ⚠️ This is **not a polished app** – it was made as part of my Python self-learning journey.  
> The code structure, logic, and UI could definitely be improved and cleaned up.

---

## 🛠️ Requirements

- Python 3.8+  
- Modules:  
  - `tkinter` (usually built-in)  
  - `numpy`  
  - `kociemba`

Install dependencies (optional but recommended):

```bash
pip install numpy kociemba
```

---

## 🚀 How to Run

you can download the project as a ZIP file:
https://github.com/Willdrage/rubik-cube-interface-2D/archive/refs/heads/main.zip

Then extract the ZIP file, and open a terminal (or Command Prompt).

Navigate to the project folder using cd, for example:
```bash
cd rubik-cube-interface-2D-main
```

Just run the main file:
```bash
python cube_ui.py
```

---

## 📌 Notes

- This was my first time working with a GUI.
- The interface is functional but not very aesthetic.
- Rotations and scramble follow standard cube notation (e.g. `R`, `U'`, `L2`).
- You can click stickers (except centers) to assign a color if color change is enabled.

---

## ✅ To Improve (eventually)

- Better visuals / 3D or isometric view  
- Undo / redo move system  
- Keyboard shortcuts  
- Cleaner code separation (MVC style)

