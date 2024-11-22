from typing import NamedTuple, List, Dict, Optional
from random import choice
from csp import CSP, Constraint


Board = List[List[str]]   # type alias for grids


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_circuit_board(rows: int, columns: int) -> Board:
    # initialize grid with random letters
    return [[" " for c in range(columns)] for r in range(rows)]

class MicroChip(NamedTuple):
    name: str
    rows: int
    columns: int


def display_circuit_board(grid: Board) -> None:
    for row in grid:
        print("".join(row))


def generate_domain(chip: MicroChip, grid: Board) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    board_height: int = len(grid)
    board_width: int = len(grid[0])
    
    # Try placing chip at each possible position
    for row in range(board_height - chip.rows + 1):
        for col in range(board_width - chip.columns + 1):
            # Generate all grid locations this chip would occupy
            chip_locations = []
            for r in range(chip.rows):
                for c in range(chip.columns):
                    chip_locations.append(GridLocation(row + r, col + c))
            domain.append(chip_locations)
    
    return domain

class CircuitBoardConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, chips: List[MicroChip]) -> None:
        super().__init__(chip.name for chip in chips)
        self.chips: List[MicroChip] = chips

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        all_locations = []
        for locations in assignment.values():
            all_locations.extend(locations)
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    # Create main circuit board
    circuit_board: Board = generate_circuit_board(9, 9)
    
    # Define chips with their dimensions
    chips = [
        MicroChip("1x6", 1, 6),
        MicroChip("2x2", 2, 2),
        MicroChip("5x2", 5, 2),
        MicroChip("4x4", 4, 4),
        MicroChip("3x3", 3, 3)
    ]
    
    # Generate possible locations for each chip
    locations: Dict[str, List[List[GridLocation]]] = {}
    for chip in chips:
        locations[chip.name] = generate_domain(chip, circuit_board)
    
    # Create and solve CSP
    csp: CSP[str, List[GridLocation]] = CSP([chip.name for chip in chips], locations)
    csp.add_constraint(CircuitBoardConstraint(chips))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    
    if solution is None:
        print("No solution found!")
    else:
        # Place chips on the board
        for chip_name, grid_locations in solution.items():
            # Mark all locations for this chip
            for loc in grid_locations:
                circuit_board[loc.row][loc.column] = chip_name[0]  # Use first letter of chip name
        display_circuit_board(circuit_board)