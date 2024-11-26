from typing import NamedTuple, List, Dict, Optional
from csp import CSP, Constraint

Board = List[List[int]]

class GridLocation(NamedTuple):
    row: int
    column: int

# Helper functions remain unchanged
def get_box_number(row, col) -> int:
    box_row = row // 3
    box_col = col // 3
    box_number = box_row * 3 + box_col
    return box_number

def get_positions_in_same_row(position) -> List[GridLocation]:
    available_row_positions = [GridLocation(position.row, col) for col in range(9) 
                             if col != position.column]
    return available_row_positions

def get_positions_in_same_column(position) -> List[GridLocation]:
    available_col_positions = [GridLocation(row, position.column) for row in range(9) 
                             if row != position.row]
    return available_col_positions

def get_positions_in_same_box(position: GridLocation) -> List[GridLocation]:
    box_number = get_box_number(position.row, position.column)
    starting_row = (box_number // 3) * 3
    starting_col = (box_number % 3) * 3
    
    available_box_positions = [
        GridLocation(row, col)
        for row in range(starting_row, starting_row + 3)
        for col in range(starting_col, starting_col + 3)
        if GridLocation(row, col) != position   
    ]
    return available_box_positions

def print_board(board: Board) -> None:
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(9):
            if j % 3 == 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print("|")

class SudokuConstraint(Constraint[GridLocation, int]):
    def __init__(self, board: Board) -> None:
        variables = [GridLocation(row, col) for row in range(9) for col in range(9)]
        super().__init__(variables)
        self.board = board

    def satisfied(self, assignment: Dict[GridLocation, int]) -> bool:
        # Create a current state of the board with both initial values and assignments
        current_state = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill in the initial values
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    current_state[row][col] = self.board[row][col]
        
        # Fill in the assignments
        for pos, digit in assignment.items():
            current_state[pos.row][pos.column] = digit
        
        # Check rows
        for row in range(9):
            nums = [current_state[row][col] for col in range(9) if current_state[row][col] != 0]
            if len(nums) != len(set(nums)):
                return False
        
        # Check columns
        for col in range(9):
            nums = [current_state[row][col] for row in range(9) if current_state[row][col] != 0]
            if len(nums) != len(set(nums)):
                return False
        
        # Check boxes
        for box_row in range(3):
            for box_col in range(3):
                nums = []
                for row in range(box_row * 3, (box_row + 1) * 3):
                    for col in range(box_col * 3, (box_col + 1) * 3):
                        if current_state[row][col] != 0:
                            nums.append(current_state[row][col])
                if len(nums) != len(set(nums)):
                    return False
        
        return True

if __name__ == "__main__":
    # Test board
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print("\nOriginal board:")
    print_board(board)
    
    # Create variables (all positions)
    variables = [GridLocation(row, col) for row in range(9) for col in range(9)]
    
    # Create domains (1-9 for empty cells, single value for filled cells)
    domains: Dict[GridLocation, List[int]] = {}
    for row in range(9):
        for col in range(9):
            pos = GridLocation(row, col)
            if board[row][col] == 0:
                domains[pos] = list(range(1, 10))
            else:
                domains[pos] = [board[row][col]]
    
    # Create CSP
    csp = CSP(variables, domains)
    
    # Add constraint
    constraint = SudokuConstraint(board)
    csp.add_constraint(constraint)
    
    # Solve
    solution = csp.backtracking_search()
    
    if solution:
        # Apply solution to board
        solved_board = [row[:] for row in board]
        for pos, digit in solution.items():
            solved_board[pos.row][pos.column] = digit
        
        print("\nSolved board:")
        print_board(solved_board)
    else:
        print("\nNo solution found!")