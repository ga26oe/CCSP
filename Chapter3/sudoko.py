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
    available_col_positions = [GridLocation(row, position.column) for row in range(9) 
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

def create_initial_assignment(board: Board) -> Dict[int, List[GridLocation]]:
    assignment: Dict[int, List[GridLocation]] = {}
    
    # Scan the board and record positions of each digit
    for row in range(9):
        for col in range(9):
            value = board[row][col]
            if value != 0:  # Only process non-empty cells
                pos = GridLocation(row=row, column=col)
                if value in assignment:
                    assignment[value].append(pos)
                else:
                    assignment[value] = [pos]
    
    # Initialize empty lists for any digits not found
    for digit in range(1, 10):
        if digit not in assignment:
            assignment[digit] = []
            
    return assignment

def verify_initial_assignment(board: Board, assignment: Dict[int, List[GridLocation]]) -> None:
    print("\nVerifying Initial Assignment:")
    # Print the actual board values
    print("\nBoard positions for each digit:")
    for digit in range(1, 10):
        positions = []
        for row in range(9):
            for col in range(9):
                if board[row][col] == digit:
                    positions.append(f"({row},{col})")
        print(f"Digit {digit} appears in board at: {positions}")

    # Print the assignment values
    print("\nAssigned positions for each digit:")
    for digit, positions in assignment.items():
        pos_str = [f"({p.row},{p.column})" for p in positions]
        print(f"Digit {digit} assigned to: {pos_str}")

    # Check for mismatches
    print("\nChecking for mismatches:")
    mismatches = False
    for digit, positions in assignment.items():
        for pos in positions:
            board_value = board[pos.row][pos.column]
            if board_value != digit:
                print(f"Mismatch: Board has {board_value} but assignment has {digit} at position ({pos.row},{pos.column})")
                mismatches = True
    
    if not mismatches:
        print("No mismatches found - assignments match the board!")


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



class SudokoConstraint(Constraint[int, List[GridLocation]]):
    def __init__(self, digits: List[int]) -> None:
        super().__init__(digits)
        self.digits: List[int] = digits
        
        #* ---------- Constraint sub-checks ----------

    def check_row_constraint(self, assignment: Dict[int, List[GridLocation]]) -> bool:
         #! Check if any other assigned digit is in the same row
        for digit1, positions1 in assignment.items():
            for pos1 in positions1:
                row_neighbors = get_positions_in_same_row(pos1)
                for digit2, pos2 in assignment.items():
                    if digit1 != digit2:
                        if pos2 in row_neighbors:
                            return False
        return True
    

    def check_col_constraint(self, assignment:  Dict[int, List[GridLocation]]) -> bool:
        for digit1, positions1 in assignment.items():
            for pos1 in positions1: #* Iterate through each position for digit1
                col_neighbors = get_positions_in_same_column(pos1) #* pass a single GridLocation
                for digit2, pos2 in assignment.items():
                    if digit1 != digit2:
                        if pos2 in col_neighbors:
                            return False
        return True

    def check_box_constraint(self, assignment:  Dict[int, List[GridLocation]]) -> bool:
        for digit1, positions1 in assignment.items():
            for pos1 in positions1:
                box_neighbors = get_positions_in_same_box(pos1)
                for digit2, pos2 in assignment.items():
                    if digit1 != digit2:
                        if pos2 in box_neighbors:
                            return False
        return True
    #* ---------- Constraint sub-checks ----------
        
    def satisfied(self, assignment: Dict[int, List[GridLocation]]) -> bool: #? Changed from Dict[int, List[GridLocation]]
        #! Can't be the same digit in the row, column or the accompanying 3x3 box
        return (self.check_col_constraint(assignment) and self.check_box_constraint(assignment) and self.check_row_constraint(assignment))    

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
    
    variables: List[int] = list(range(1,10)) 
    
    #* Create the Domain 
    domain: Dict[int, List[GridLocation]] = {}
    empty_locations: List[GridLocation] = []
    
    #* Find all empty locations
    for row in range(9): 
        for col in range (9):
            if test_board[row][col] == 0:
                empty_locations.append(GridLocation(row, col))
    
    #* For each digit 1-9, its domain is all the empty locations
    for digit in variables:
        domain[digit] = empty_locations.copy() #! Using copy to avoid shared references
        
    #* create initial assignment for pre-filled cells
    inital_assignment = create_initial_assignment(test_board)
    verify_initial_assignment = verify_initial_assignment(test_board, inital_assignment)
        
    #? constraints: List[Constraint[int, List[GridLocation]]] = []
    constraint = SudokoConstraint(variables)
    #? constraints.append(constraint)
    sudoko_csp: CSP[int, List[GridLocation]] = CSP(variables, domain)
    sudoko_csp.add_constraint(constraint)
    
    
    
    print("Initial Board")
    for row in test_board:
        print(row)
    print("\nInitial Assignment:")
    for digit, pos in inital_assignment.items():
        print(f"digit {digit} at position {pos}")
    print("\nTesting initiial assignment satisfaction:")
    
    # Verify assignments match the board
    print("\nVerifying assignments against board:")
    for digit, positions in inital_assignment.items():
        for pos in positions:
            board_value = test_board[pos.row][pos.column]
            if board_value != digit:
                print(f"Mismatch: Board has {board_value} but assignment has {digit} at position {pos}")
    
    result = constraint.satisfied(inital_assignment)
    
    print(f"Row constraint: {constraint.check_row_constraint(inital_assignment)}")
    print(f"Column constraint: {constraint.check_col_constraint(inital_assignment)}")
    print(f"Box constraint: {constraint.check_box_constraint(inital_assignment)}")
    print(f"Overall satisfaction: {result}")
