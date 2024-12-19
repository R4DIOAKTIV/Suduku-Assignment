from dokusan import generators
import copy
import numpy as np
class Sudoku:
    """
    Represents a Sudoku puzzle.

    Attributes:
        grid (list): A 9x9 list representing the Sudoku grid.
                    0 indicates an empty cell.
        domains (list): A 9x9 list of sets, where each set represents
                       the possible values for a cell in the grid.
    """
    def __init__(self, grid=None):
        """
       Initializes the Sudoku grid and domains.

       Args:
           grid (list, optional): A pre-filled Sudoku grid. If not
                                  provided, a new empty grid is created.
                                  Defaults to None.
       """
        # Initialize the Sudoku grid and domains
        self.grid = grid if grid else [[0] * 9 for _ in range(9)]
        self.domains = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
        self.initialize_domains()
        self.arcs = self.define_arcs()  # Get all arcs
        self.grid_history = [copy.deepcopy(self.grid)]
        self.domains_history = [copy.deepcopy(self.domains)]

    def initialize_domains(self):
        """
        Initializes the domains for each cell in the grid.

        - If a cell has a pre-filled value, its domain is set to that value only.
        - If a cell is empty, its domain is set to all possible values (1-9).
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.domains[i][j] = {self.grid[i][j]}
                else:
                    self.domains[i][j] = set(range(1, 10))

    def define_arcs(self):
        """
        Defines all the arcs (constraints) in the Sudoku grid.

        An arc connects two cells, indicating that the values in those cells
        cannot be the same. This ensures that each row, column, and 3x3 subgrid
        has unique values.

        Returns:
            list: A list of tuples representing the arcs in the grid.
        """
        arcs = []
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if j != k:
                        arcs.append(((i, j), (i, k)))
                for k in range(9):
                    if i != k:
                        arcs.append(((i, j), (k, j)))
        for box_row in range(3):
            for box_col in range(3):
                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            for l in range(3):
                                if (i, j) != (k, l):
                                    arcs.append(((box_row * 3 + i, box_col * 3 + j), (box_row * 3 + k, box_col * 3 + l)))
        return arcs

    def apply_arc_consistency(self):
        """
        Applies Arc Consistency to the Sudoku grid.

        Arc Consistency ensures that no cell has a value in its domain that
        already exists in a related cell (connected by an arc). This reduces
        the number of possible values for each cell, potentially leading to
        faster solving.
        """
        changed = True
        while changed:
            changed = False
            for (xi, xj) in self.arcs:
                if self.revise(xi, xj):
                    changed = True
        self.update_grid()
        self.grid_history.append(copy.deepcopy(self.grid))
        self.domains_history.append(copy.deepcopy(self.domains))

    def revise(self, xi, xj):
        """
        Revises the domain of cell xi based on the constraints with cell xj.

        This function checks if any value in the domain of xi can be eliminated
        because it can't form a pair with values in xj. If such a value is found, it's
        removed from the domain of xi.

        Args:
            xi (tuple): Coordinates of cell xi (row, col).
            xj (tuple): Coordinates of cell xj (row, col).

        Returns:
            bool: True if the domain of xi was revised, False otherwise.
        """
        revised = False
        for value in list(self.domains[xi[0]][xi[1]]):
            if not any(value != v for v in self.domains[xj[0]][xj[1]]):
                self.domains[xi[0]][xi[1]].remove(value)
                revised = True
        return revised

    def get_degree(self, row, col):
        """Calculates the degree of a cell in a Sudoku grid."""
        degree = 0
        for i in range(9):
            if self.grid[row][i] == 0 and i != col:  # Check row
                degree += 1
            if self.grid[i][col] == 0 and i != row:  # Check column
                degree += 1

        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.grid[i][j] == 0 and (i, j) != (row, col):  # Check box
                    degree += 1
        return degree
    

    # def solve_sudoku(self):
    #     """Recursive arc consistency backtracking solver with MRV and Degree Heuristic."""
    #     self.apply_arc_consistency()
    #     return self.solve_sudoku_recursive()

    def solve_sudoku(self):
        """Recursive arc consistency backtracking solver with MRV and Degree Heuristic."""
        self.apply_arc_consistency()
        if any(len(self.domains[i][j]) == 0 for i in range(9) for j in range(9)):
            return False  # Base case: Empty domain, no solution possible
        mrv_cell = self.get_mrv()
        if not mrv_cell:
            return True  # Base case: No empty cells, puzzle solved
        else:
            row, col = mrv_cell

        for num in list(self.domains[row][col]):  # Iterate through a copy of the domain
            if self.is_valid(self.grid, num, (row, col)):
                self.grid[row][col] = num
                original_domains = copy.deepcopy(self.domains)  # Store the original domains
                for i in range(9):  # Update the domains of the related cells
                    if num in self.domains[row][i] and i != col:
                        self.domains[row][i].discard(num)
                    if num in self.domains[i][col] and i != row:
                        self.domains[i][col].discard(num)
                box_x = col // 3
                box_y = row // 3
                for i in range(box_y * 3, box_y * 3 + 3):
                    for j in range(box_x * 3, box_x * 3 + 3):
                        if num in self.domains[i][j] and (i, j) != (row, col):
                            self.domains[i][j].discard(num)
                self.domains[row][col] = {num}  # Update the domain of the current cell
                self.grid_history.append(copy.deepcopy(self.grid))
                self.domains_history.append(copy.deepcopy(self.domains))
                if self.solve_sudoku():  # Recursive call
                    return True

                self.grid[row][col] = 0  # Backtrack
                self.domains = original_domains  # Restore the original domains
        return False
    
    def is_valid(self, grid, num, pos):
        """Checks if placing 'num' at 'pos' is valid."""
        # Check row
        for i in range(len(grid[0])):
            if grid[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(grid)):
            if grid[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def get_mrv(self):
        """Gets the cell with the Minimum Remaining Values."""
        min_remaining = 10  # Start with a value greater than any possible domain size
        mrv_cell = None

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    remaining_values = len(self.domains[i][j])
                    if remaining_values < min_remaining:
                        min_remaining = remaining_values
                        mrv_cell = (i, j)
                    elif remaining_values == min_remaining and mrv_cell is not None:
                        if self.get_degree(i, j) > self.get_degree(mrv_cell[0], mrv_cell[1]):
                            mrv_cell = (i, j)
        return mrv_cell

    def update_grid(self):
        for i in range(9):
            for j in range(9):
                if len(self.domains[i][j]) == 1:
                    self.grid[i][j] = next(iter(self.domains[i][j]))

    def print_domains(self):
        # Print the current domains for each cell
        print("Current Domains:")
        for i in range(9):
            print([sorted(list(self.domains[i][j])) for j in range(9)])
        print()

    def print_grid(self):
        # Print the Sudoku grid
        for row in self.grid:
            print(" ".join(str(num) if num != 0 else "_" for num in row))
        print()
        
    def generate_puzzle(self, difficilty):
            if difficilty == "easy":
                puzzle = str(generators.random_sudoku(avg_rank=50))
            elif difficilty == "mid": 
                puzzle = str(generators.random_sudoku(avg_rank=100))
            elif difficilty == "hard":
                puzzle = str(generators.random_sudoku(avg_rank=150))
            else:
                puzzle = str(generators.random_sudoku(avg_rank=250))
            self.grid = [list(map(int, puzzle[i:i+9])) for i in range(0, 81, 9)]
            self.initialize_domains()


# if __name__ == "__main__":
#     # grid3 = [[0, 5, 0, 1, 0, 9, 0, 0, 0],
#     #         [0, 9, 0, 2, 0, 0, 0, 0, 7],
#     #         [6, 2, 4, 0, 5, 7, 0, 0, 0],
#     #         [0, 0, 8, 0, 0, 0, 6, 7, 0],
#     #         [0, 0, 0, 5, 0, 0, 0, 2, 0],
#     #         [0, 7, 0, 0, 0, 0, 0, 3, 0],
#     #         [0, 8, 2, 0, 4, 1, 0, 0, 0],
#     #         [0, 0, 5, 7, 3, 0, 0, 0, 1],
#     #         [0, 3, 0, 0, 0, 0, 0, 0, 0]]
#     sudoku = Sudoku()
#     sudoku.generate_puzzle("mid")
#     # print("Puzzle:", sudoku.grid)
#     print("Solving:")
#     sudoku.print_grid()
#     if sudoku.solve_sudoku():
#         print("Solution:")
#         for row in sudoku.grid:
#             print(row)
#     else:   
#         print("No solution found.")
#     print("\n")
#     for grid in sudoku.grid_history:
#         for row in grid:
#             print(row)
#         print()


