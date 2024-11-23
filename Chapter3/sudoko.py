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
    
def generate_domain(digit: SudokoDigit, grid: Board) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
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
    def satisfied(self, assignment: Dict[int, List[GridLocation]]) -> bool:
        #! Can't be the same digit in the row, column or the accompanying 3x3 box
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)        


test_board: Board = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0]
]
test_digit = SudokoDigit(name='5', row =0, column=0)
result = generate_domain(test_digit, test_board)

print(result)