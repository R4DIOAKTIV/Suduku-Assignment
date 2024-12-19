import tkinter as tk
from tkinter import messagebox, ttk
from main import Sudoku

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()
        self.create_difficulty_dropdown()

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=3, columnspan=3, pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear)
        clear_button.grid(row=10, column=3, columnspan=3, pady=10)

        generate_button = tk.Button(self.root, text="Generate", command=self.generate)
        generate_button.grid(row=11, column=3, columnspan=3, pady=10)

    def create_difficulty_dropdown(self):
        self.difficulty = tk.StringVar()
        self.difficulty.set("easy")  # default value
        difficulty_label = tk.Label(self.root, text="Select Difficulty:")
        difficulty_label.grid(row=12, column=2, columnspan=2, pady=10)
        difficulty_dropdown = ttk.Combobox(self.root, textvariable=self.difficulty, values=["easy", "medium", "hard"])
        difficulty_dropdown.grid(row=12, column=4, columnspan=2, pady=10)

    def get_board(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.entries[row][col].get()
                if value == '':
                    current_row.append(0)
                else:
                    current_row.append(int(value))
            board.append(current_row)
        return board

    def set_board(self, board):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if board[row][col] != 0:
                    self.entries[row][col].insert(0, str(board[row][col]))

    def solve(self):
        board = self.get_board()
        sudoku = Sudoku(board)
        if sudoku.solve_sudoku():
            self.set_board(sudoku.grid)
        else:
            messagebox.showerror("Error", "No solution found.")

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def generate(self):
        difficulty = self.difficulty.get()
        sudoku = Sudoku([[0]*9 for _ in range(9)])
        sudoku.generate_puzzle(difficulty)
        self.set_board(sudoku.grid)

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()