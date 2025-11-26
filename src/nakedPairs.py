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
    Units
    ------
    Takes a sudoku puzzle, and defines the rows, columns,
    and boxes. Also creates IDs for each value in the puzzle 
    based on the row, column, and box each value belongs to.
    
    Parameters
    ___________
    sudoku : list[int]
        A list of 81 values that this function will make IDs
        for. If a value is 0, then we will assign candidate 
        numbers to it. 
    """
    rowList = []
    columnList = []
    boxList = []
    cellList = []
    for r in range(9):
        start = r * 9
        rowList.append([start + i for i in range(9)])
    for c in range(9):
        columnList.append([c + 9*i for i in range(9)])
    for b in range(9):
        boxRow = (b // 3)
        boxColumn = (b % 3)
        start = (boxRow * 3 * 9) + (boxColumn * 3)
        boxList.append([
            start + r*9 + c
            for r in range(3)
            for c in range(3)
        ])
    for cell in range(81):
        r = cell // 9
        c = cell % 9
        b = (r//3)*3 + (c//3)
        cellList.append((r, c, b))
    print(rowList, "AAAAAAAAAAAAAAAAA\n\n", columnList, "AAAAAAAAAAAAAAAAA\n\n", boxList, "AAAAAAAAAAAAAAAAA\n\n", cellList)
    print(cellList[9])
    print(cellList[79])
def buildConstraintGraph(sudoku):
    """
    This function takes the given sudoku puzzle and builds a constraint graph
    that can enforce the rules of sudoku.
    """
    constraintG = Graph()
    for i in sudoku:
        constraintG.addVertex()
    return constraintG
def nakedPairs(constraintG):
    pass


if __name__ == "__main__":
    sudoku = [5,3,4,6,7,8,9,1,2,
              6,7,2,1,9,5,3,4,8,
              1,9,8,3,4,2,5,6,7,
              8,5,9,7,6,1,4,2,3,
              4,2,6,8,5,3,7,9,1,
              7,1,3,9,2,4,8,5,6,
              9,6,1,5,3,7,2,8,4,
              2,8,7,4,1,9,6,3,5,
              3,4,5,2,8,6,1,7,9]
    units(sudoku)
    # sudoku = [1, 2, 3] #etc
    # pass



# backup code
# def units(sudoku):
#     rowList = []
#     columnList = []
#     boxList = []
#     cellList = []
#     for r in range(9):
#         start = r * 9
#         # rowID = [start + i for i in range(9)]
#         rowList.append([start + i for i in range(9)])
#         # rowList += rowID
#         # r = r + 1
#     for c in range(9):
#         # columnID = [c + 9*i for i in range(9)]
#         columnList.append([c + 9*i for i in range(9)])
#         # columnList += columnID
#         # c = c + 1
#     for b in range(9):
#         boxRow = (b // 3)
#         boxColumn = (b % 3)
#         start = (boxRow * 3 * 9) + (boxColumn * 3)
#         # boxID = [
#         #     start + r*9 + c
#         #     for r in range(3)
#         #     for c in range(3)
#         # ]
#         boxList.append([
#             start + r*9 + c
#             for r in range(3)
#             for c in range(3)
#         ])
#         # boxList += boxID
#         # b = b+1
#     for cell in range(81):
#         r = cell // 9
#         c = cell % 9
#         b = (r//3)*3 + (c//3)
#         cellList.append((r, c, b))
#     print(rowList, "AAAAAAAAAAAAAAAAA\n\n", columnList, "AAAAAAAAAAAAAAAAA\n\n", boxList, "AAAAAAAAAAAAAAAAA\n\n", cellList)
#     print(cellList[9])
#     print(cellList[79])
# def buildConstraintGraph(sudoku):
#     """
#     This function takes the given sudoku puzzle and builds a constraint graph
#     that can enforce the rules of sudoku.
#     """
#     constraintG = Graph()
#     for i in sudoku:
#         constraintG.addVertex()
#     return constraintG
# def nakedPairs(constraintG):
#     pass


# if __name__ == "__main__":
#     sudoku = [5,3,4,6,7,8,9,1,2,
#               6,7,2,1,9,5,3,4,8,
#               1,9,8,3,4,2,5,6,7,
#               8,5,9,7,6,1,4,2,3,
#               4,2,6,8,5,3,7,9,1,
#               7,1,3,9,2,4,8,5,6,
#               9,6,1,5,3,7,2,8,4,
#               2,8,7,4,1,9,6,3,5,
#               3,4,5,2,8,6,1,7,9]
#     units(sudoku)
#     # sudoku = [1, 2, 3] #etc
#     # pass