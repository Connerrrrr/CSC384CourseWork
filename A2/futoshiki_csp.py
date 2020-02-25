#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid: object) -> object:
    ##IMPLEMENT
    pass


def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT
    dim = len(futo_grid)
    dom = []
    for i in range(dim):
        dom.append(i + 1)
    print(dom)

    variables = []
    var_num = 0
    for row in futo_grid:
        for element in row:
            if not element:
                var_num += 1
                variables.append(Variable('Grid{}'.format(var_num), dom))
    print(variables)

    csp = CSP("Futoshiki", variables)
    return csp
