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

    def all_diff_checker(vals):
        for a in range(len(vals)):
            for b in range(a + 1, len(vals)):
                if vals[a] == vals[b]:
                    return False
        return True
    # DOMAIN
    dim = len(futo_grid)
    dom = []
    for i in range(dim):
        dom.append(i + 1)

    # VARIABLE
    variables = []
    var_num = 0
    matrix = []
    for row in futo_grid:
        temp_row = []
        var_row = []
        for element in row:
            if isinstance(element, int) and element:
                temp_row.append(element)
            # create variable
            if not element:
                var_num += 1
                variable = Variable('Grid{}'.format(var_num), dom)
                var_row.append(variable)
                variables.append(variable)
                temp_row.append(variable)
        matrix.append(temp_row)

    # CONSTRAINT
    cons = []
    # Get transpose of int matrix to check column all diff
    transpose_matrix = [list(i) for i in zip(*matrix)]

    def getAllDiff(mat, direction):
        for row_index in range(len(mat)):
            # Get all variables
            var_list = []
            for element in mat[row_index]:
                if not isinstance(element, int):
                    var_list.append(element)
            # Get all possible tuples
            sat_tuples = []
            for inner_row in itertools.product(dom, repeat=len(dom)):
                sat_tuple = []
                int_matched = True
                if all_diff_checker(inner_row):
                    for index in range(len(inner_row)):
                        if isinstance(mat[row_index][index], int):
                            if mat[row_index][index] != inner_row[index]:
                                int_matched = False
                        else:
                            sat_tuple.append(inner_row[index])
                    if int_matched:
                        sat_tuples.append(tuple(sat_tuple))
            # Create Constraint Object
            con = Constraint("{}{}".format(direction, row_index + 1), var_list)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    # AllDiff in row
    getAllDiff(matrix, "Row")

    # AllDiff in column
    getAllDiff(transpose_matrix, "Column")

    # Inequality Constraint
    inequality_count = 0
    for i in range(len(futo_grid)):
        for j in range(len(futo_grid[i])):
            if futo_grid[i][j] in ["<", ">"]:
                operand = futo_grid[i][j]
                left = futo_grid[i][j - 1]
                right = futo_grid[i][j + 1]
                # Get the variable object from matrix
                if right == 0:
                    right = matrix[i][(j + 1) // 2]
                if left == 0:
                    left = matrix[i][(j - 1) // 2]

                # Satisfying Tuples
                inequality_var_list = []
                inequality_count += 1
                sat_tuples = []
                # if two variables involve
                if not isinstance(left, int) and not isinstance(right, int):
                    inequality_var_list.append(left)
                    inequality_var_list.append(right)
                    # situation with var1 > var2
                    if operand == ">":
                        for tup in itertools.product(dom, repeat=2):
                            if tup[0] > tup[1]:
                                sat_tuples.append(tup)
                    # situation with var1 < var2
                    else:
                        for tup in itertools.product(dom, repeat=2):
                            if tup[0] < tup[1]:
                                sat_tuples.append(tup)
                    con = Constraint("Inequality{}".format(inequality_count), inequality_var_list)
                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)

                # right is variable
                elif not isinstance(right, int):
                    inequality_var_list.append(right)
                    # situation with int > var
                    if operand == ">":
                        for val in right.domain():
                            if left > val:
                                sat_tuples.append(tuple([val]))
                    # situation with int < var
                    else:
                        for val in right.domain():
                            if left < val:
                                sat_tuples.append(tuple([val]))
                    con = Constraint("Inequality{}".format(inequality_count), inequality_var_list)
                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)

                # left is variable
                else:
                    inequality_var_list.append(left)
                    # situation with var > int
                    if operand == ">":
                        for val in right.domain():
                            if val > right:
                                sat_tuples.append(tuple([val]))
                    # situation with var < int
                    else:
                        for val in right.domain():
                            if val < right:
                                sat_tuples.append(tuple([val]))
                    con = Constraint("Inequality{}".format(inequality_count), inequality_var_list)
                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)

    csp = CSP("Futoshiki", variables)
    for c in cons:
        csp.add_constraint(c)
    return csp, matrix
