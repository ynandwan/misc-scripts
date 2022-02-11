import numpy as np
import math

def isValidSudoku(board: List[List[str]]) -> bool:
  """
  Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
Note:

A Sudoku board (partially filled) could be valid but is not necessarily solvable.
Only the filled cells need to be validated according to the mentioned rules.
Input: board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
  """
  
        def is_valid(x):
            a = set()
            for b in x:
                if b !=0 and b in a:
                    return False
                elif b!=0:
                    a.add(b)
            #
            return True
        
        def check_lists(row_list):
            for row in row_list:
                if not is_valid(row):
                    return False
            return True
           
        rows = [[int(cell) if cell !='.' else 0 for cell in row] for row in board]
        #print(rows)
        if not check_lists(rows):
            return False
        
        cols = list(zip(*rows))
        #print(cols)
        if not check_lists(cols):
            return False
        
        grids = [[rows[3*i+k][3*j+l]  for k in range(3) for l in range(3)  ] for i in range(3) for j in range(3)]
        #print(grids)
        if not check_lists(grids):
            return False
        
        return True
        

def is_correct(query,pred):
    return (match_query(query,pred) and is_safe_sudoku(pred))

def pointwise_accuracy(target,pred):
    return (target.astype(int) == pred.astype(int)).sum()/target.size
    

def match_query(query, pred):
    mask = (query>0)
    return np.array_equal(query[mask], pred[mask])

def is_safe_sudoku(x):
    block_shape_dict = {6: (2, 3),
                     8: (2, 4),
                     9: (3, 3),
                     10: (2, 5),
                     12: (2, 6),
                     14: (2, 7),
                     15: (3, 5),
                     16: (4, 4)}

    
    grid = x.astype(int)
    n = int(math.sqrt(grid.size))
    grid = grid.reshape(n,n)
    
    b_x, b_y = block_shape_dict[n]

    for i in range(n):
        if len(set(grid[i]))<n:
            return False 
        if len(set(grid[:,i]))<n:
            return False 

        b_row = i//b_x 
        b_col = i%b_x
#         if n!=9:
#             Pdb().set_trace()
        if len(set(grid[b_x*b_row:b_x*(b_row+1),b_y*b_col:b_y*(b_col+1)].flatten()))<n:
            return False 
    return True
