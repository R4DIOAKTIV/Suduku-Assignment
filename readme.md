# Sudoku Solver

This project is a Sudoku solver implemented in Python. It includes a `Sudoku` class that represents a Sudoku puzzle and provides methods to solve it, using arc consistency and backtracking.

## Arc Consistency
Arc consistency is a concept used in constraint satisfaction problems (CSP). It is a property of binary constraints, which are constraints involving two variables. A CSP is arc-consistent if for every variable (X) and every value (x) in the domain of (X), there is some value (y) in the domain of another variable (Y) such that the binary constraint between (X) and (Y) is satisfied.

The constraint in our problem is the existance of the number itself where if X is in domain of variable one at least one of the variables in the domain of variable two should not be X.

## Backtracking
Backtracking is a general algorithmic technique used for solving constraint satisfaction problems, combinatorial optimization problems, and other problems that require searching through a large set of possible solutions. It incrementally builds candidates to the solutions and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot possibly be completed to a valid solution.
## Sudoku Class

The `Sudoku` class represents a Sudoku puzzle and provides methods to initialize and manipulate the puzzle.

### Attributes

- `grid`: A 9x9 list representing the Sudoku grid. A value of `0` indicates an empty cell.
- `domains`: A 9x9 list of sets, where each set represents the possible values for each variable in the grid.
- `arcs`:  An arc connects two cells, indicating that the values in those cells
        cannot be the same. This ensures that each row, column, and 3x3 subgrid
        has unique values.
### Code Implementation:
```python
def apply_arc_consistency(self):
        """
        Applies Arc Consistency to the Sudoku grid.

        """
        changed = True
        # Loop until no domain updates
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

```

# Case Studies
## Case 1 Easy
![alt text](image-1.png)
Solution:
![alt text](image-2.png)
steps: 1 arc consistency 
Solved in 0.0085 seconds.
# Domains 
Step 1
![alt text](image-3.png)
Step 2
![alt text](image-4.png)
## Case 2 Mid
![alt text](image-5.png)
Solution:
![alt text](image-6.png)
steps: 19 arc consistency and tracking 
Solved in 0.0628 seconds.
# Domains 
Step 1
![alt text](image-7.png)
Step 2
![alt text](image-8.png)
...
Step 19
![alt text](image-9.png)
Step 20
![alt text](image-10.png)
## Case 3 Hard
![alt text](image-14.png)
Solution:
![alt text](image-15.png)
steps: 65 arc consistency and tracking 
Solved in 0.1796 seconds.
# Domains 
Step 1
![alt text](image-16.png)
Step 2
![alt text](image-17.png)
Step 3
![alt text](image-18.png)
...
Step 65
![alt text](image-19.png)
Step 66
![alt text](image-20.png)