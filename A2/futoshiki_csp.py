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


def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
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
        for element in row:
            if isinstance(element, int):
                var_num += 1
                # create variable
                if element:
                    variable = Variable('Grid{}'.format(var_num), [element])
                else:
                    variable = Variable('Grid{}'.format(var_num), dom)
                variables.append(variable)
                # temp row for var matrix
                temp_row.append(variable)
        matrix.append(temp_row)

    # Constraint
    cons = []
    # Transpose matrix for column pair-wise
    transpose_matrix = [list(i) for i in zip(*matrix)]

    def getbinaryconstraints(mat):
        for mat_row in mat:
            for a in range(len(mat_row)):
                for b in range(a + 1, len(mat_row)):
                    # For every binary constraint
                    sat_tuples = []
                    for possible_tup in itertools.product(dom, repeat=2):
                        if possible_tup[0] != possible_tup[1]:
                            sat_tuples.append(possible_tup)
                    # Create row-wise binary constraint and add tuples to it
                    con = Constraint("C(Q{},Q{})".format(mat_row[a], mat_row[b]), [mat_row[a], mat_row[b]])
                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)

    # row-wise binary constraint
    getbinaryconstraints(matrix)

    # column-wise binary constraint
    getbinaryconstraints(transpose_matrix)

    # Inequality Constraint
    inequality_count = 0
    for i in range(len(futo_grid)):
        for j in range(len(futo_grid[i])):
            if futo_grid[i][j] in ["<", ">"]:
                operand = futo_grid[i][j]
                # Get the variable object from matrix
                right = matrix[i][(j + 1) // 2]
                left = matrix[i][(j - 1) // 2]

                # Satisfying Tuples
                inequality_var_list = []
                inequality_count += 1
                sat_tuples = []

                # Get var list ready
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

                # Create Constrain object and append it to constraint list
                con = Constraint("Inequality{}".format(inequality_count), inequality_var_list)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # CSP obejct
    csp = CSP("Futoshiki-Model1", variables)
    for c in cons:
        csp.add_constraint(c)
    return csp, matrix


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
        for element in row:
            if isinstance(element, int):
                var_num += 1
                # create variable
                if element:
                    variable = Variable('Grid{}'.format(var_num), [element])
                else:
                    variable = Variable('Grid{}'.format(var_num), dom)
                variables.append(variable)
                # temp row for var matrix
                temp_row.append(variable)
        matrix.append(temp_row)

    # CONSTRAINT
    cons = []
    # Get transpose of int matrix to check column all diff
    transpose_matrix = [list(i) for i in zip(*matrix)]

    def getAllDiff(mat, direction):
        '''Create row-wise and column-wise AllDiff constraint and append them into constraint list'''
        for row_index in range(len(mat)):
            # Get all variables
            var_list = []
            for elem in mat[row_index]:
                var_list.append(elem)
            # Get all possible tuples
            sat_tuples = []
            for possible_tup in itertools.product(dom, repeat=len(dom)):
                if all_diff_checker(possible_tup):
                    # check if domain matches
                    domain_matched = True
                    for index in range(len(possible_tup)):
                        if possible_tup[index] not in mat[row_index][index].domain():
                            domain_matched = False
                    if domain_matched:
                        sat_tuples.append(possible_tup)
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
                # Get the variable object from matrix
                right = matrix[i][(j + 1) // 2]
                left = matrix[i][(j - 1) // 2]

                # Satisfying Tuples
                inequality_var_list = []
                inequality_count += 1
                sat_tuples = []

                # Get var list ready
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

                # Create Constrain object and append it to constraint list
                con = Constraint("Inequality{}".format(inequality_count), inequality_var_list)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    csp = CSP("Futoshiki-Model2", variables)
    for c in cons:
        csp.add_constraint(c)
    return csp, matrix
