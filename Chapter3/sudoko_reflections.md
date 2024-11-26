# CSP Sudoku Implementation Reflection

## What I Learned

- What were the key concepts I understood after completing this project?

  - This was my first major ish python project, so I learned a lot of python syntax. I was introduced to ...
    - List comprehension
    - Python Typing
    - Helper Functions

- What insights did I gain about Constraint Satisfaction Problems?
  - Really make sure you completely understand what your variables and domains are, and don't mix them up when implementing them
- What did I learn about choosing the right data structures?
  - Make sure whatever you are using matches what other functions require when they use that data structure for their own parameters

## What Was Challenging

- What was the hardest part of implementing the solution?
  - Organizing Code and making sure the data structure used were consistent
- Which bugs took the longest to figure out?
  - The bug that took the longest to figure out was the issue of the solver not comlpleting all the squares. I realized that the domain and
    variables were switched around. My implementation that was not working correctly had the variables as the numbers, and the domain as the
    potental grid locations. This is not intuitive, since generally it is not how you approach solving the sudoko puzzle. (You are not choosing numbers and assigning them to a position. Instead you are choosing the locations, and then assigning them a number) So the variables are the locations in the Grid, and the domain are the numbers

## General Questions

- What would make this implementation better?
  - Soon I will like to add constant propogation

## Code Examples Worth Remembering

```python
class SudokuConstraint(Constraint[GridLocation, int]): vs. class SudokuConstraint(Constraint[int, GridLocation]): where class SudokuConstraint(Constraint[V, D]):

```
