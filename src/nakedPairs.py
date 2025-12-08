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
        vertex.residence = (r, c, b)
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
def constraintPropagation(constraintG):
    """
    constraintPropagation
    ---------------------
    This function takes the constraint graph, constraintG, and removes
    candidate numbers from unsolved cells using the defined constraints.

    Parameters
    ___________
    constraintG : Graph()
        The constraint graph created in the buildConstraintGraph function.
        This could be the initial graph, or it could have previously been
        propagated.
    
    Returns
    ________
    constraintG : Graph()
        Returns the propagated graph so strategies can operate on it.
    """
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
def nakedSingles(constraintG):
    """
    nakedSingles
    -------------
    This function looks for a vertex on the graph, and if the type of
    the vertex's valOrCand attribute is type list, and the list is of
    length 1, then it sets the valOrCand attribute equal to the sole
    candidate in that list.

    Parameters
    ___________
    constraintG : Graph()
        The constraint graph created in the buildConstraintGraph function.
        This has been propagated through the constraintPropagation function.
        It may have been run through other strategies or propagated further
        than it initially was.
    
    Returns
    ________
    constraintG : Graph()
        Returns the edited graph so it can be used by other functions.
    """
    for vertA in constraintG:
        constraintPropagation(constraintG)
        constraintG.getVertex(vertA)
        if isinstance(vertA.valOrCand, list):
            if len(vertA.valOrCand) == 1:
                print("Naked Single Found:\n",vertA.residence)
                vertA.valOrCand = vertA.valOrCand.pop()
    constraintPropagation(constraintG)
    print("UPDATED BOARD:\n")
    for v in constraintG:
        print(v.valOrCand)
    return constraintG
def nakedPairs(constraintG):
    """
    nakedPairs
    -----------
    This function finds a pair of cells in the same unit that share two
    remaining candidate numbers. It then removes those candidates from other cells
    in their shared unit.

    Parameters
    ___________
    constraintG : Graph()
        The constraint graph created in the buildConstraintGraph function.
        This has been propagated through the constraintPropagation function.
        It may have been run through other strategies or propagated further
        than it initially was.

    Returns
    ________
    constraintG : Graph()
        Returns the edited graph so it can be used by other functions.
    """
    for vertA in constraintG:
        constraintG.getVertex(vertA)
        if isinstance(vertA.valOrCand, list):
            if len(vertA.valOrCand) == 2:
                for neighbor in vertA.getConnections():
                    constraintG.getVertex(neighbor)
                    if isinstance(neighbor.valOrCand, list): 
                        if len(neighbor.valOrCand) == 2:
                            if neighbor.valOrCand == vertA.valOrCand:
                                print("Naked Pair Found:\n", vertA.residence, neighbor.residence, vertA.valOrCand, neighbor.valOrCand)
                                if vertA.row == neighbor.row:
                                    for anyVert in vertA.getConnections() and neighbor.getConnections():
                                        constraintG.getVertex(anyVert)
                                        if isinstance(anyVert.valOrCand, list):
                                            if anyVert.row == vertA.row and anyVert.residence != vertA.residence and anyVert.residence != neighbor.residence:
                                                for i in anyVert.valOrCand[:]:
                                                    if i in vertA.valOrCand:
                                                        anyVert.valOrCand.remove(i)
                                                        
                                if vertA.column == neighbor.column:
                                    for anyVert in vertA.getConnections() and neighbor.getConnections():
                                        constraintG.getVertex(anyVert)
                                        if isinstance(anyVert.valOrCand, list):
                                            if anyVert.column == vertA.column and anyVert.residence != vertA.residence and anyVert.residence != neighbor.residence:
                                                for i in anyVert.valOrCand[:]:
                                                    if i in vertA.valOrCand:
                                                        anyVert.valOrCand.remove(i)  
                                                        
                                if vertA.box == neighbor.box:
                                    for anyVert in vertA.getConnections() and neighbor.getConnections():
                                        constraintG.getVertex(anyVert)
                                        if isinstance(anyVert.valOrCand, list):
                                            if anyVert.box == vertA.box and anyVert.residence != vertA.residence and anyVert.residence != neighbor.residence:
                                                for i in anyVert.valOrCand[:]:
                                                    if i in vertA.valOrCand:
                                                        anyVert.valOrCand.remove(i)
                                                        
                                if vertA.row and vertA.box == neighbor.row and neighbor.box:
                                    for anyVert in vertA.getConnections() and neighbor.getConnections():
                                        constraintG.getVertex(anyVert)
                                        if isinstance(anyVert.valOrCand, list):
                                            if (anyVert.row and anyVert.box == vertA.row and vertA.box) and anyVert.residence != vertA.residence and anyVert.residence != neighbor.residence:
                                                for i in anyVert.valOrCand[:]:
                                                    if i in vertA.valOrCand:
                                                        anyVert.valOrCand.remove(i)
                                                        
                                if vertA.column and vertA.box == neighbor.column and neighbor.box:
                                    for anyVert in vertA.getConnections() and neighbor.getConnections():
                                        constraintG.getVertex(anyVert)
                                        if isinstance(anyVert.valOrCand, list):
                                            if (anyVert.column and anyVert.box == vertA.column and vertA.box) and anyVert.residence != vertA.residence and anyVert.residence != neighbor.residence:
                                                for i in anyVert.valOrCand[:]:
                                                    if i in vertA.valOrCand:
                                                        anyVert.valOrCand.remove(i)
                                                        
    constraintPropagation(constraintG)
    print("UPDATED BOARD:\n")
    for v in constraintG:
        print(v.valOrCand)
    return constraintG
if __name__ == "__main__":
    # The program can solve this puzzle. I think the program is able to handle
        # less naked pairs.
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
    constraintG = buildConstraintGraph(sudoku)
    constraintPropagation(constraintG)
    for v in constraintG:
        print(v.valOrCand)
    nakedSingles(constraintG)
    nakedPairs(constraintG)
    nakedSingles(constraintG)
    nakedSingles(constraintG)
    nakedSingles(constraintG)
    nakedSingles(constraintG)
    nakedSingles(constraintG)
    nakedSingles(constraintG)
    nakedSingles(constraintG)
    #####################################

    # This is an example of the code NOT working. I need to re-examine how the
        # nakedPairs code works. I did not use "and" correctly. The program was likely
        # overwhelmed by the amount of naked pairs it found, and removed incorrect candidates
    # To fix this, I need to refactor the algorithm so it checks the set intersection of each pair cells candidates.
        # That way, it ONLY removes from the correct connections.
    ################### UNCOMMENT:
    # # this is the level 1 daily puzzle for 12/8/25 from sudokuwiki.org
    # sudoku = [0,0,0,0,0,4,0,0,5,
    #           9,0,0,0,2,0,0,8,3,
    #           0,0,2,9,0,0,0,0,0,
    #           0,0,5,0,0,8,0,0,0,
    #           0,0,6,2,0,1,4,0,0,
    #           0,0,0,6,0,0,9,0,0,
    #           0,0,0,5,0,6,7,0,0,
    #           5,4,0,0,7,0,0,0,1,
    #           7,0,0,1,0,0,0,0,0]
    # constraintG = buildConstraintGraph(sudoku) # initialize the graph
    # constraintPropagation(constraintG) # initial constraint propagation
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedPairs(constraintG) ################ optionally, uncomment up to here to see first error.
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedPairs(constraintG)
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    # nakedSingles(constraintG)
    #######################################