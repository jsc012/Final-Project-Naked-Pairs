# This is the final project for CSCI 310.
For this project, I am making a program that, when given a sudoku puzzle, can build a constraint graph, and then run a strategy against the constraint graph.
In *fancy* terms, I'm modeling Sudoku as a constraint satisfaction problem[^1], where 

- the set of variables is a set of all cells on a Sudoku board, 

- the set of domains are sets of each unit,

- the set of constraints are the edges between cells in a unit.

## Overview
In a constraint graph, edges are created between two nodes if those nodes can't share a value.
Sudoku has 81 cells, and each cell belongs to a unit; that is, it's in a row, a column, and a box. Each cell also has to have a number from 1-9. Each number can only appear once in a unit.
We can treat each cell in Sudoku as a node, and each edge as two cells in the same unit that can't have the same number.

---
When the constraint graph is built, the program then needs to propagate the constraints and remove some candidate numbers (unsolved cells contain a list of possible solutions) from cells. 
My program, by default, sets each unsolved cell equal to a list containing the numbers 1-9. Solved cells on the Sudoku board constrain the possible values of unsolved cells.

---
When the program has propagated the initial candidates, it can then apply a strategy called Naked Pairs.
If two cells in a unit have only the same two candidate numbers remaining, then those two candidate numbers can be removed from every other cell in their shared unit.

---
This is a basic strategy, but I hope that I can later program more complex strategies to run against difficult Sudoku puzzles.

---
# Final code:
The program did not turn out as I had hoped. I did implement the naked singles strategy, but the function that executes naked pairs is very flawed.
In the code, there are two example puzzles.

---
The first example can successfully solve the puzzle using both naked singles and naked pairs.

---
The second example, the one in comments, is not solved. When the naked pairs function is called, it identifies about 6 naked pairs throughout the board. It is not recording the naked pairs and eliminating necessary candidates when the board has been completely searched, but it's instead eliminating candidates as soon as it finds a pair, then it continues looking through the board.
Also, I am not correctly using "and" throughout the function.

---
To fix it, the naked pairs function should be reorganized and refactored. The function should look through the board and, when it finds a naked pair, add the units of the connected vertices of cellA and cellB to a list. It should keep going through the board and repeating this process.
Then, the program should individually evaluate each pair and remove the candidates from the set intersetion of their connections (what cells are in both of their connections). Then, it should propagate the board again.
For following pairs, it should also check to see if the naked pair is still a naked pair, or if prior propagation has eliminated a candidate from the pair.

Documentation: https://jsc012.github.io/Final-Project-Naked-Pairs/
[^1]: [Constraint satisfaction problem](Constraint_satisfaction_problem)
