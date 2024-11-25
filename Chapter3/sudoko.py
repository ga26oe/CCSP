from typing import NamedTuple, List, Dict, Optional
from csp import CSP, Constraint

Board = List[List[int]]

class GridLocation(NamedTuple):
    row: int
    column: int
class SudokoDigit(NamedTuple):
    name: str
    row: int
    column: int
    
#* ---------- START: Helper Functions ---------- 
def get_box_number(row, col) -> int:
    box_row = row // 3
    box_col = col // 3
    box_number = box_row * 3 + box_col
    return box_number

def get_positions_in_same_row(position) -> List[GridLocation]:
    #current_position = GridLocation(position)  #! Don't Need the Line!, position is already in use
    available_row_positions = [GridLocation(position.row, col) for col in range(9) 
                               if col != position.column]
    return available_row_positions

def get_positions_in_same_column(position) -> List[GridLocation]:
    #current_position = GridLocation(position)  #! Don't Need the Line!, position is already in use
    available_col_positions = [GridLocation(row, position.col) for row in range(9) 
                               if row != position.row]
    return available_col_positions

def get_positions_in_same_box(position: GridLocation) -> List[GridLocation]:
    #current_position = GridLocation(position)  #! Don't Need the Line!, position is already in use
    box_number =  get_box_number(position.row, position.column)
    starting_row = (box_number // 3) * 3
    starting_col = (box_number % 3 ) * 3
    
    available_box_positions = [
        GridLocation(row, col)
        for row in range(starting_row, starting_row + 3)
        for col in range(starting_col, starting_col + 3)
        if GridLocation(row, col) != position   
    ]
    return available_box_positions
#* ---------- END: Helper Functions ----------
    
def generate_domain(digit: SudokoDigit, grid: Board) -> List[GridLocation]: #! Changed from List[List{GridLocation}]
    domain: List[GridLocation] = []
    board_row_size: int = len(grid)
    board_col_size: int = len(grid[0])
    #! The places in the board that have a 0 are assumed as empty!
    for row in range(board_row_size):
        for col in range(board_col_size):
            if grid[row][col] == 0:
                domain.append(GridLocation(row, col))
        
    return domain

#* ---------- Constraint sub-checks ----------

def check_row_constraint(self, assignment: Dict[int, List[GridLocation]]) -> bool:
    #! Check if any other assigned digit is in the same row
    for digit1, pos1 in assignment.items():
        row_neighbors = get_positions_in_same_row(pos1)
        for digit2, pos2 in assignment.items():
            if digit1 != digit2:
                if pos2 in row_neighbors:
                    return False
    return True
    

def check_col_constraint(self, assignment: Dict[int, List[GridLocation]]) -> bool:
    for digit1, pos1 in assignment.items():
        col_neighbors = get_positions_in_same_column(pos1)
        for digit2, pos2 in assignment.items():
            if digit1 != digit2:
                if pos2 in col_neighbors:
                    return False
    return True

def check_box_constraint(self, assignment: Dict[int, List[GridLocation]]) -> bool:
    for digit1, pos1 in assignment.items():
        box_neighbors = get_positions_in_same_box(pos1)
        for digit2, pos2 in assignment.items():
            if digit1 != digit2:
                if pos2 in box_neighbors:
                    return False
    return True
#* ---------- Constraint sub-checks ----------

class SudokoConstraint(Constraint[int, List[GridLocation]]):
    def __init__(self, digits: List[int]) -> None:
        super().__init__(digits)
        self.digits: List[int] = digits
        
    def satisfied(self, assignment: Dict[GridLocation, int]) -> bool: #? Changed from Dict[int, List[GridLocation]]
        #! Can't be the same digit in the row, column or the accompanying 3x3 box
        return check_col_constraint(assignment) and check_box_constraint(assignment) and check_row_constraint(assignment)
    

if __name__ == "__main__":
    # Test board (0 represents empty cells)
    test_board = [
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
    
    variables: List[int] = list(range(1,10)) #* Creates variables 1 through 9
    
    inital_assignment: Dict[int, List[GridLocation]] = {}
    for row in range(9): 
        for col in range (9):
            if test_board[row][col] != 0:
                digit = test_board[row][col]
                inital_assignment[digit] = GridLocation(row, col)
    
    constraints: List[Constraint[int, List[GridLocation]]] = []
    constraint = SudokoConstraint(variables)
    constraints.append(constraint)
    
    sudoko_csp: CSP[int, List[GridLocation]] = CSP(variables, constraints)
    
    print("Initial Board")
    for row in test_board:
        print(row)
    print("\nTesting initiial assignment satisfaction:")
    print(constraint.satisfied(inital_assignment))
    