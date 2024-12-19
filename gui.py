import tkinter as tk
from tkinter import messagebox, ttk
from main import Sudoku

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_title()
        self.create_grid()
        self.create_buttons()
        self.create_difficulty_dropdown()
        self.create_history_display()
        self.mode = "solver"  # Modes: solver, user_input

    def create_title(self):
        title = tk.Label(self.root, text="Sudoku Solver", font=('Arial', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=9, pady=10)

    def create_grid(self):
        grid_frame = tk.Frame(self.root, bg='black')
        grid_frame.grid(row=1, column=0, columnspan=9, padx=10, pady=10)
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(grid_frame, width=2, font=('Arial', 18), justify='center', bd=1, relief='solid')
                entry.grid(row=row, column=col, padx=1, pady=1)
                entry.bind('<KeyRelease>', self.on_cell_change)
                self.entries[row][col] = entry

    def on_cell_change(self, event):
        if event.char.isdigit():
            self.validate_user_solution()

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=10, column=0, columnspan=9, pady=10)

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve, font=('Arial', 14), bg='lightblue')
        solve_button.grid(row=0, column=0, padx=5)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear, font=('Arial', 14), bg='lightblue')
        clear_button.grid(row=0, column=1, padx=5)

        generate_button = tk.Button(button_frame, text="Generate", command=self.generate, font=('Arial', 14), bg='lightblue')
        generate_button.grid(row=0, column=2, padx=5)

        show_domains_button = tk.Button(button_frame, text="Show Domains", command=self.show_domains, font=('Arial', 14), bg='lightblue')
        show_domains_button.grid(row=0, column=3, padx=5)

        show_history_button = tk.Button(button_frame, text="Show History", command=self.show_history, font=('Arial', 14), bg='lightblue')
        show_history_button.grid(row=0, column=4, padx=5)

        user_input_button = tk.Button(button_frame, text="User Input", command=self.user_input_mode, font=('Arial', 14), bg='lightblue')
        user_input_button.grid(row=0, column=5, padx=5)

        validate_button = tk.Button(button_frame, text="Validate", command=self.validate_user_solution, font=('Arial', 14), bg='lightblue')
        validate_button.grid(row=0, column=6, padx=5)

    def create_difficulty_dropdown(self):
        difficulty_label = tk.Label(self.root, text="Select Difficulty:", font=('Arial', 14))
        difficulty_label.grid(row=11, column=2, columnspan=2, pady=10)

        self.difficulty = tk.StringVar()
        self.difficulty.set("easy")  # default value
        difficulty_dropdown = ttk.Combobox(self.root, textvariable=self.difficulty, values=["easy", "medium", "hard"], font=('Arial', 14))
        difficulty_dropdown.grid(row=11, column=4, columnspan=2, pady=10)

    def create_history_display(self):
        history_frame = tk.Frame(self.root)
        history_frame.grid(row=12, column=0, columnspan=9, pady=10)

        self.step_label = tk.Label(history_frame, text="Step: 1", font=('Arial', 14))
        self.step_label.grid(row=0, column=0, padx=5)

        self.step_entry = tk.Entry(history_frame, width=5, font=('Arial', 14))
        self.step_entry.grid(row=0, column=1, padx=5)

        go_button = tk.Button(history_frame, text="Go", command=self.go_to_step, font=('Arial', 14), bg='lightblue')
        go_button.grid(row=0, column=2, padx=5)

        prev_button = tk.Button(history_frame, text="Previous", command=self.prev_grid_step, font=('Arial', 14), bg='lightblue')
        prev_button.grid(row=0, column=3, padx=5)

        next_button = tk.Button(history_frame, text="Next", command=self.next_grid_step, font=('Arial', 14), bg='lightblue')
        next_button.grid(row=0, column=4, padx=5)

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
        self.sudoku = Sudoku(board)
        if self.sudoku.solve_sudoku():
            self.set_board(self.sudoku.grid)
        else:
            messagebox.showerror("Error", "No solution found.")
        self.show_history()

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def generate(self):
        difficulty = self.difficulty.get()
        self.sudoku = Sudoku([[0]*9 for _ in range(9)])
        self.sudoku.generate_puzzle(difficulty)
        self.set_board(self.sudoku.grid)
        if self.mode == "user_input":
            # Create a copy of the user's board to solve
            self.correct_board = [row[:] for row in self.get_board()]
            self.correct_sudoku = Sudoku(self.correct_board)
            

    def show_domains(self):
        if hasattr(self, 'sudoku'):
            self.current_domain_step = 0
            self.domains_window = tk.Toplevel(self.root)
            self.domains_window.title("Domains History")
            self.domains_window.geometry("800x600")  # Set the window size
            self.domain_labels = [[tk.Label(self.domains_window, text="", width=20, font=('Arial', 8), justify='center') for _ in range(9)] for _ in range(9)]
            for row in range(9):
                for col in range(9):
                    self.domain_labels[row][col].grid(row=row, column=col, padx=15, pady=15)  # Increase padding
            self.step_label = tk.Label(self.domains_window, text=f"Step: {self.current_domain_step + 1}/{len(self.sudoku.domains_history)}", font=('Arial', 14))
            self.step_label.grid(row=10, column=0, columnspan=9, pady=10)
            self.update_domain_display()
            prev_button = tk.Button(self.domains_window, text="Previous", command=self.prev_domain_step)
            prev_button.grid(row=11, column=0, padx=5, pady=5)
            next_button = tk.Button(self.domains_window, text="Next", command=self.next_domain_step)
            next_button.grid(row=11, column=1, padx=5, pady=5)

    def update_domain_display(self):
        if self.sudoku:
            for row in range(9):
                for col in range(9):
                    domain = self.sudoku.domains_history[self.current_domain_step][row][col]
                    self.domain_labels[row][col].config(text=str(sorted(domain)))
            self.step_label.config(text=f"Step: {self.current_domain_step + 1}/{len(self.sudoku.domains_history)}")

    def prev_domain_step(self):
        if self.current_domain_step > 0:
            self.current_domain_step -= 1
            self.update_domain_display()

    def next_domain_step(self):
        if self.current_domain_step < len(self.sudoku.domains_history) - 1:
            self.current_domain_step += 1
            self.update_domain_display()

    def show_history(self):
        if hasattr(self, 'sudoku'):
            self.current_grid_step = 0
            self.update_grid_display()

    def update_grid_display(self):
        if self.sudoku:
            for row in range(9):
                for col in range(9):
                    self.entries[row][col].delete(0, tk.END)
                    value = self.sudoku.grid_history[self.current_grid_step][row][col]
                    if value != 0:
                        self.entries[row][col].insert(0, str(value))
            self.step_label.config(text=f"Step: {self.current_grid_step + 1}/{len(self.sudoku.grid_history)}")

    def prev_grid_step(self):
        if self.current_grid_step > 0:
            self.current_grid_step -= 1
            self.update_grid_display()

    def next_grid_step(self):
        if self.current_grid_step < len(self.sudoku.grid_history) - 1:
            self.current_grid_step += 1
            self.update_grid_display()

    def go_to_step(self):
        try:
            step = int(self.step_entry.get()) - 1
            if 0 <= step < len(self.sudoku.grid_history):
                self.current_grid_step = step
                self.update_grid_display()
            else:
                messagebox.showerror("Error", "Step number out of range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid step number.")

    def user_input_mode(self):
        self.mode = "user_input"
        self.clear()
        messagebox.showinfo("User Input Mode", "You can now enter your solution. ")


    def validate_user_solution(self, event=None):
        if self.mode == "user_input":
            user_board = self.get_board()
            self.sudoku = Sudoku(user_board)
            
            if self.correct_sudoku.solve_sudoku():
                consistent = True
                for i in range(len(user_board)):
                    for j in range(len(user_board[i])):
                        if user_board[i][j] != 0 and user_board[i][j] != self.correct_board[i][j]:
                            consistent = False
                            break
                    if not consistent:
                        break
                
                if consistent:
                    messagebox.showinfo("Validation", "Your solution is correct!")
                else:
                    messagebox.showerror("Validation", "Your solution is incorrect. Please try again.")
            else:
                messagebox.showerror("Validation", "The puzzle cannot be solved. Please check your input.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()