from cspbase import *
import itertools
import traceback


def queensCheck(qi, qj, i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj
       respectively. Used to find satisfying tuples.
    '''
    return i != j and abs(i-j) != abs(qi-qj)

def nQueens(n):
    '''Return an n-queens CSP'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi+1, len(dom)):
            con = Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]])
            sat_tuples = []
            for t in itertools.product(dom, dom):
                if queensCheck(qi, qj, t[0], t[1]):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp

##Tests FC after the first queen is placed in position 1.
def test_simple_FC(stu_propagators):
    did_fail = False
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        stu_propagators.prop_FC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            if var_domain[i] != answer[i]:
                details = "Failed simple FC test: variable domains don't match expected results"
                did_fail = True
                break
        if not did_fail:
            score = 1
            details = ""
    except Exception:
        details = "One or more runtime errors occurred while testing simple FC: %r" % traceback.format_exc()

    return score,details


#@max_grade(1)
##Tests GAC after the first queen is placed in position 1.
def test_simple_GAC(stu_propagators):
    did_fail = False
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        stu_propagators.prop_GAC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            if var_domain[i] != answer[i]:
                details = "Failed simple GAC test: variable domains don't match expected results."
                did_fail = True
                break
        if not did_fail:
            score = 1
            details = ""

    except Exception:
        details = "One or more runtime errors occurred while testing simple GAC: %r" % traceback.format_exc()

    return score,details


def three_queen_GAC(stu_propagators):
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(4)
        curr_vars[2].assign(1)
        curr_vars[7].assign(5)
        stu_propagators.prop_GAC(queens)
        answer = [[4],[6, 7, 8],[1],[3, 8],[6, 7],[2, 8],[2, 3, 7, 8],[5]]
        var_vals = [x.cur_domain() for x in curr_vars]

        if var_vals != answer:
            details = "Failed three queens GAC test: variable domains don't match expected results"

        else:
            score = 1
            details = ""
    except Exception:
        details = "One or more runtime errors occurred while testing GAC with three queens: %r" % traceback.format_exc()

    return score,details


def three_queen_FC(stu_propagators):
    score = 0
    try:
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(4)
        curr_vars[2].assign(1)
        curr_vars[7].assign(5)
        stu_propagators.prop_FC(queens)

        answer = [[4],[6, 7, 8],[1],[3, 6, 8],[6, 7],[2, 6, 8],[2, 3, 7, 8],[5]]
        var_vals = [x.cur_domain() for x in curr_vars]

        if var_vals != answer:
            details = "Failed three queens FC test: variable domains don't match expected results"

        else:
            score = 1
            details = ""

    except Exception:
        details = "One or more runtime errors occurred while testing FC with three queens: %r" % traceback.format_exc()

    return score,details
	
def main(stu_propagators=None):
    total = 0

    if stu_propagators == None:
        import propagators as stu_propagators


    print("---starting test_simple_FC---")
    score,details = test_simple_FC(stu_propagators)
    total += score
    print(details)
    print("---finished test_simple_FC---\n")

    print("---starting test_simple_GAC---")
    score,details = test_simple_GAC(stu_propagators)
    total += score
    print(details)
    print("---finished test_simple_GAC---\n")

    print("---starting three_queen_FC---")
    score,details = three_queen_FC(stu_propagators)
    total += score
    print(details)
    print("---finished three_queen_FC---\n")

    print("---starting three_queen_GAC---")
    score,details = three_queen_GAC(stu_propagators)
    total += score
    print(details)
    print("---finished three_queen_GAC---\n")
    print("Total score %d/4\n" % total)
	
if __name__=="__main__":
    main()