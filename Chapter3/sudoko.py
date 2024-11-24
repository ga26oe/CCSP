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
    
#* ---------- Helper Functions ---------- 
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
 

#* ---------- Helper Functions ----------
    
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
    def satisfied(self, assignment: Dict[GridLocation, int]) -> bool: #? Changed from Dict[int, List[GridLocation]]
        #! Can't be the same digit in the row, column or the accompanying 3x3 box
        #todo -- Need different sub-methods - check_rows(); check_columns(); check_boxes();
        pass      


test_board: Board = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0]
]
test_digit = SudokoDigit(name='5', row =0, column=0)
result = generate_domain(test_digit, test_board)

print(result) 