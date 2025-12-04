"""
nakedPairs.py
====================================
This program uses a graph to create the Naked Pair Sudoku strategy.

| Author: Jack C
| Date: 2025 November 23
"""

from pythonds.graphs import Graph, Vertex

def units(sudoku):
    """
    units
    ------
    Defines the rows, columns, and boxes of a sudoku board.
    Also creates a tuple for each cell on the board,
    based on the row, column, and box each cell belongs to.
    Also brings in the actual sudoku puzzle, and makes a list
    of that, making candidates for cells that equal 0.

    Parameters
    ___________
    sudoku : list[int]
        A list of 81 values. This is the list that the program
        will edit to create candidate numbers for unsolved cells
        (cells that have a value of 0).
    
    Returns
    ________
    rowList : list
        A list of lists of the cells in each row.
    columnList : list
        A list of lists of the cells in each column.
    boxList : list
        A list of lists of the cells in each box.
    candidatedSudoku : list
        A list of values and candidate lists created from the
        given sudoku puzzle.
    cellUnitList : list
        A list of tuples that corresponds to the 81 value sudoku
        board. Each integer in the tuple corresponds to the cell's
        units; the row, column, and box it belongs to.
    
    Notes
    ------
    To be clear: each unit list is not making a list from the values
    of the given sudoku puzzle. It's making a list from the values of
    a sudoku board. The actual sudoku values will be assigned to vertices
    in the constraint graph.
    """
    rowList = []
    columnList = []
    boxList = []
    candidatedSudoku = []
    cellUnitList = []
    for r in range(9):
        start = r * 9
        rowList.append([start + i for i in range(9)])
    for c in range(9):
        columnList.append([c + 9*i for i in range(9)])
    for b in range(9):
        boxRow = (b // 3)
        boxColumn = (b % 3)
        start = (boxRow * 3 * 9) + (boxColumn * 3)
        boxList.append([start + r*9 + c for r in range(3) 
                                            for c in range(3)])
    for cell in range(81):
        r = cell // 9
        c = cell % 9
        b = (r//3)*3 + (c//3)
        cellUnitList.append((r, c, b))
    for value in sudoku:
        if value == 0:
            value = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        candidatedSudoku.append(value)
    # print("List of rows\n", rowList,
    #       "\n\nList of columns\n", columnList,
    #       "\n\nList of boxes\n", boxList,
    #       "\n\nList of cell values\n", candidatedSudoku,
    #       "\n\nList of each cells row, column, and box\n", cellUnitList)
    return rowList, columnList, boxList, candidatedSudoku, cellUnitList
def buildConstraintGraph(sudoku):
    """
    buildConstraintGraph
    ---------------------
    This function builds a graph of the sudoku board, adding information
    to each cell, telling it what units it belongs to, and if it has a value
    or candidate numbers.
    It then builds constraints in each unit, which effectively enforces the
    rules of sudoku.

    Parameters
    ___________
    sudoku : list[int]
        A list of 81 values. This list is passed through because candidatedSudoku,
        which is returned from the units function, was built from the sudoku puzzle.
    
    Returns
    ________
    constraintG : Graph()
        Returns the constraint graph.
    """
    rowList, columnList, boxList, candidatedSudoku, cellUnitList = units(sudoku)
    constraintG = Graph()
    for cell in range(81):
        constraintG.addVertex(cell)
        r, c, b = cellUnitList[cell]
        vertex = constraintG.getVertex(cell)
        vertex.row = r
        vertex.column = c
        vertex.box = b
        vertex.valOrCand = candidatedSudoku[cell]
    for aRow in rowList:
        for i in range(len(aRow)):
            for j in range(i+1, len(aRow)):
                cellA = aRow[i]
                cellB = aRow[j]
                constraintG.addEdge(cellA, cellB)
                constraintG.addEdge(cellB, cellA)
    for aColumn in columnList:
        for i in range(len(aColumn)):
            for j in range(i+1, len(aColumn)):
                cellA = aColumn[i]
                cellB = aColumn[j]
                constraintG.addEdge(cellA, cellB)
                constraintG.addEdge(cellB, cellA)
    for aBox in boxList:
        for i in range(len(aBox)):
            for j in range(i+1, len(aBox)):
                cellA = aBox[i]
                cellB = aBox[j]
                constraintG.addEdge(cellA, cellB)
                constraintG.addEdge(cellB, cellA)
    return constraintG

    # this is just some test code
    # print("test A\n")
    # for v in constraintG:
    #     print(v.id, "→", len(v.getConnections()))
    # print("test B\n")
    # for neighbor in constraintG.getVertex(3).getConnections():
    #     print(neighbor.id)
def candidatePropagation(constraintG):
    rowList, columnList, boxList, candidatedSudoku, cellUnitList = units(sudoku)
    for vertA in constraintG:
        constraintG.getVertex(vertA)
        if isinstance(vertA.valOrCand, int):
            for neighbor in vertA.getConnections():
                constraintG.getVertex(neighbor)
                if isinstance(neighbor.valOrCand, list):
                    for i in neighbor.valOrCand:
                        if i == vertA.valOrCand:
                            neighbor.valOrCand.remove(i)
    return constraintG
    # for cell in range(81):
    #     constraintG.getVertex(cell)
    #     if type(cell.valOrCand) is int:
    #         for neighbor in cell.getConnections():
    #             constraintG.getVertex(neighbor)
    #             if type(neighbor.valOrCand) is list:
    #                 for i in neighbor.valOrCand:
    #                     if i == cell.valOrCand:
    #                         neighbor.valOrCand.pop(i)
def nakedPairs(constraintG):
    pass
    
if __name__ == "__main__":
    # test for just row, column, and box lists code
    # sudoku = [5,3,4,6,7,8,9,1,2,
    #           6,7,2,1,9,5,3,4,8,
    #           1,9,8,3,4,2,5,6,7,
    #           8,5,9,7,6,1,4,2,3,
    #           4,2,6,8,5,3,7,9,1,
    #           7,1,3,9,2,4,8,5,6,
    #           9,6,1,5,3,7,2,8,4,
    #           2,8,7,4,1,9,6,3,5,
    #           3,4,5,2,8,6,1,7,9]

    # this is the level 1 daily puzzle for 11/26/25 from sudokuwiki.org 
    sudoku = [0,9,6,0,0,0,4,5,0,
              0,4,0,0,5,0,0,0,0,
              5,0,0,0,1,2,0,0,9,
              0,0,0,5,0,0,0,0,0,
              0,3,9,0,0,0,8,1,0,
              0,0,0,0,0,4,0,0,0,
              9,0,0,1,2,0,0,0,7,
              0,0,0,0,3,0,0,2,0,
              0,8,2,0,0,0,1,6,0]
    # this:
    constraintG = buildConstraintGraph(sudoku)
    # creates the initial constraint graph.
    # it should not be called again, because it would recreate the graph
    # using the inital puzzle. we don't want this

    # TODO
    # the problem here is that I want to be able to call strategies
    # multiple times. could i just keep passing constraintG into the function?
    # or do i need to redefine it each time it's called and the function runs?
    # if i need to redefine it, i could do so in a for loop.
    candidatePropagation(constraintG)
    constraintG = candidatePropagation(constraintG)
    for v in constraintG:
            print(v.valOrCand)
    # constraintG = buildConstraintGraph(sudoku)
    