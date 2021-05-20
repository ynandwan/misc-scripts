import numpy as np
import math

def is_correct(query,pred):
    return (match_query(query,pred) and is_safe_sudoku(pred))


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
