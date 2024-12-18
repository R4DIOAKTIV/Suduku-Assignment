import random

class Variable:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.domain = list(range(1, 10))
        self.neighbors = self.get_neighbors(self)

    def __repr__(self):
        return f"Variable({self.row}, {self.col}, {self.domain})"
    
    def get_neighbors(self):
        neighbors = []
        for i in range(9):
            if i != self.col:
                neighbors.append(self.variables[var.row][i])
            if i != var.row:
                neighbors.append(self.variables[i][var.col])
        start_row, start_col = 3 * (var.row // 3), 3 * (var.col // 3)
        for i in range(3):
            for j in range(3):
                if start_row + i != var.row and start_col + j != var.col:
                    neighbors.append(self.variables[start_row + i][start_col + j])
        return neighbors

class Sudoku:
    def __init__(self):
        self.initialize_variables()
        self.generate_board()

    def initialize_variables(self):
        self.variables = [[Variable(row, col) for col in range(9)] for row in range(9)]

    def initialize_domains(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    self.variables[row][col].domain = [self.board[row][col]]

    def backtracking(self):
        empty = self.find_empty_location()
        if not empty:
            return True  # Puzzle solved. 
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.backtracking():
                    return True
                self.board[row][col] = 0  # Backtrack

        return False
    
    def is_valid(self, row, col, num):
    # Check if num is not in the current row, column, and 3x3 subgrid
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def find_empty_location(self):
    #any location with zero is empty 
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None    

    def is_consistent(self, var, value):
        # Check if value is not in the current row, column, and 3x3 subgrid
        for i in range(9):
            if self.board[var.row][i] == value or self.board[i][var.col] == value:
                return False
        start_row, start_col = 3 * (var.row // 3), 3 * (var.col // 3)
        for i in range(start_row + 3):
            for j in range(start_col + 3):
                if self.board[i][j] == value:
                    return False
        return True

    def arc_consistency(self):
        queue = [(var, neighbor) for row in self.variables for var in row for neighbor in self.get_neighbors(var)]
        while queue:
            var, neighbor = queue.pop(0)
            if self.revise(var, neighbor):
                if len(var.domain) == 0:
                    return False
                for neighbor in self.get_neighbors(var):
                    queue.append((neighbor, var))
        return True

    def revise(self, var, neighbor):
        """
        Revise the domain of a variable to ensure consistency with a neighboring variable.

        Args:
            var (Variable): The variable whose domain is to be revised.
            neighbor (Variable): The neighboring variable to check for consistency.

        Returns:
            bool: True if the domain of the variable was revised, False otherwise.
        """
        revised = False
        for value in var.domain:
            if not any(self.is_consistent(neighbor, value) for value in neighbor.domain):
                var.domain.remove(value)
                revised = True
        return revised

    def solve(self):
        if self.arc_consistency():
            for row in range(9):
                for col in range(9):
                    if len(self.variables[row][col].domain) == 1:
                        self.board[row][col] = self.variables[row][col].domain[0]
            return self.board
        else:
            return None
            
    def generate_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for _ in range(17):  # Fill 17 cells to ensure a unique solution
            # choose a random cell
            row, col = random.randint(0, 8), random.randint(0, 8)
            # make sure the generated cell is empty
            while self.board[row][col] != 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            # generate a random number between 1 and 9
            num = random.randint(1, 9)
            # make sure the generated number is consistent with the board
            while not self.is_consistent(Variable(row, col), num):
                num = random.randint(1, 9)
            self.board[row][col] = num
        self.initialize_domains()

if __name__ == "__main__":
    # sudoku = Sudoku()
    # solved_board = sudoku.backtracking(sudoku.board)
    # if solved_board:
    #     for row in solved_board:
    #         print(row)
    # else:
    #     print("No solution found.")
    baba =  Variable(0,0)
    print(baba.neighbors)

