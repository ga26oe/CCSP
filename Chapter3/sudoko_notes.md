Sudoku Constraint Development Guide

## Required Sudoku Rules

1. Row Constraint

   - Each digit (1-9) must appear exactly once in each row
   - How will you track digits in the same row?

2. Column Constraint

   - Each digit (1-9) must appear exactly once in each column
   - How will you track digits in the same column?

3. 3x3 Box Constraint
   - Each digit (1-9) must appear exactly once in each 3x3 box
   - How will you determine which box a position belongs to?
   - How will you group positions by box?

## Implementation Questions to Consider

### Data Structure Questions

1. Is Dict[int, List[GridLocation]] the most appropriate structure?
   - What does each key represent in Sudoku?
     - Each Key represents the number
   - What should the values represent?
     - The values could represent the position in the board
   - Would a different structure make rule checking easier?
     - A 2D array is probably the best structure to represent the sudoko board and a
       a dictionay would be the best for listing potential locations since lookup is fast

### Algorithm Questions

1. How will you check all digits in the same row?

   - What data structure would make row checking efficient?
   - How do you handle partially filled rows?

2. How will you check all digits in the same column?

   - What data structure would make column checking efficient?
   - How do you handle partially filled columns?

3. How will you check 3x3 boxes?

   - How do you calculate which box a position belongs to?
   - How do you efficiently group positions by box?

4. How will you handle partial assignments?
   - What happens when not all positions are filled?
   - How do you validate rules with incomplete data?

## Key Differences from Word Search

1. Word Search:

   - Only needs to check for position overlaps
   - Doesn't care about relationships between positions
   - Each position can only be used once

2. Sudoku:
   - Must check position relationships (row/column/box)
   - Must validate digit uniqueness in groups
   - Must handle multiple constraints simultaneously

## Implementation Tips

1. Consider breaking down the satisfied() method into sub-methods:

   - check_rows()
   - check_columns()
   - check_boxes()

2. Think about helper functions:

   - get_box_number(row, col)
   - get_positions_in_same_row(position)
   - get_positions_in_same_column(position)
   - get_positions_in_same_box(position)
     - starting_row = (box_number // 3) \* 3
     - starting_col = (box_number % 3) \* 3
     - Division by 3 gives us the Row, and mod 3 gives us the column

3. Consider edge cases:
   - Empty grid
   - Partially filled grid
   - Invalid placements
   - Multiple solutions

## Testing Considerations

1. Test each constraint separately
2. Test combinations of constraints
3. Test with:
   - Empty grid
   - Partially filled grid
   - Valid complete grid
   - Invalid grid (breaking each rule)
   - Edge cases

## Next Steps

1. Choose a data structure for representing the board state
2. Implement helper functions for position grouping
3. Implement individual rule checks
4. Combine rule checks in satisfied() method
5. Add validation and error handling
6. Test with various scenarios
