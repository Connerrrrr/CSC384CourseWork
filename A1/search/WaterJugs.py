'''
EXAMPLE STATESPACE WATERJUGS

States in the waterjugs problem can be represented by two integers, (gal3,gal4), where gal3 is the amount of water
in the 3 gallon jug, and gal4 is the amount of water in the 4 gallon jug.

To use the search routines we subclass the "StateSpace" class and implement specialized versions of
 __init__ (which must call StateSpace.__init__
 successors
 hashable_state
 print_state

Then we also implement some utility functions to ease the use of SearchEngine.search
In particular, we implement a way of specifying goal functions and a couple of heurstics.

Finally, for convience we specify a bunch of examples to run if the file executed by the python
intepreter.

'''

from search import *

class WaterJugs(StateSpace):

    def __init__(self, action, gval, gal3, gal4, parent = None):
        StateSpace.__init__(self, action, gval, parent)
        self.gal3 = gal3
        self.gal4 = gal4
        
    def successors(self):
        """We have x actions, (1) empty the gal3, (2) fill the gal3,
        (3) empty the gal4, (4) fill the gal4 (5) pour the
        gal3-->gal4, (6) pour the gal4-->gal3.  all actions have cost
        1.  in computing the list of successor states, however, make
        sure we don't return a state equal to self as this is a null
        transtion."""

        States = list()
        if self.gal3 > 0 :
            States.append( WaterJugs('Empty 3 Gallon', self.gval+1, 0, self.gal4, self) )
        if self.gal3 < 3 :
            States.append( WaterJugs('Fill 3 Gallon', self.gval+1, 3, self.gal4, self) )
        if self.gal4 > 0 :
            States.append( WaterJugs('Empty 4 Gallon', self.gval+1, self.gal3, 0, self) )
        if self.gal4 < 4 :
            States.append( WaterJugs('Fill 4 Gallon', self.gval+1, self.gal3, 4, self) )
        if self.gal4 < 4 and self.gal3 > 0:
            maxpour = min( 4 - self.gal4, self.gal3 ) #at most can only fill up 4 gallon
            States.append( WaterJugs('Pour 3 into 4', self.gval+1, self.gal3-maxpour, self.gal4+maxpour, self) )
        if self.gal3 < 3 and self.gal4 > 0:
            maxpour = min( 3 - self.gal3, self.gal4 ) #at most can only fill up 3 gallon
            States.append( WaterJugs('Pour 4 into 3', self.gval+1, self.gal3+maxpour, self.gal4-maxpour, self) )
        return States
    
    def hashable_state(self) :
        return (self.gal3, self.gal4)

    def print_state(self):
        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (3gal, 4gal) = ({},{}), (From S{})".format(self.action, self.index, self.gval, self.gal3, self.gal4, self.parent.index))
        else:
            print("Action=\"{}\", S{}, g-value = {}, (3gal, 4gal) = ({},{}), (Initial state)".format(self.action, self.index, self.gval, self.gal3, self.gal4))

#Some auxillary heuristic functions and goal test functions.

#We use this to store the current goal
#So that the heuristics functions can get access to it
WaterJugs.goal_state = False

def waterjugs_set_goal(gal3, gal4):
    '''set the current goal'''
    WaterJugs.goal_state = (gal3, gal4)

def waterjugs_goal_fn(state):
    '''test if the state is equal to the current goal,
    allow wild cards '*' in the goal state'''
    return ((WaterJugs.goal_state[0] == '*' or 
             state.gal3 == WaterJugs.goal_state[0]) and
            (WaterJugs.goal_state[1] == '*' or 
             state.gal4 == WaterJugs.goal_state[1]))

def waterjugs_h_sum_function(state):
    hval = 0
    if WaterJugs.goal_state[0] != '*':
        hval = hval + abs(WaterJugs.goal_state[0] - state.gal3)
    if WaterJugs.goal_state[1] != '*':
        hval = hval + abs(WaterJugs.goal_state[1] - state.gal4)
    return hval

def waterjugs_h_max_function(state):
    hval = 0
    if WaterJugs.goal_state[0] != '*':
        hval = abs(WaterJugs.goal_state[0] - state.gal3)
    if WaterJugs.goal_state[1] != '*':
        hval = max(hval,abs(WaterJugs.goal_state[1] - state.gal4))
    return hval

def waterjugs_h_total_diff_function(state):
    hval = 0
    if WaterJugs.goal_state[0] != '*':
        wsum = WaterJugs.goal_state[0]
    if WaterJugs.goal_state[1] != '*':
        wsum = wsum + WaterJugs.goal_state[1]
    return abs(state.gal3+state.gal4 - wsum)

if __name__ == "__main__":

    #sample runs 
    se = SearchEngine('astar', 'full')

    #If you want to trace the search, set trace_on.  Using Level 1 for illustration. Level 2 prints more detailed results.    
    se.trace_on(1)
    #se.trace_on(2)

    s0 = WaterJugs("START", 0, 0, 0)
    waterjugs_set_goal(2, 0)

    #Alternate goal for demonstration
    #s0 = WaterJugs("START", 0, 0, 0)
    #waterjugs_set_goal(0, 1)    

    print("=========Test 1. Astar with h_sum heuristic========")
    se.init_search(s0, waterjugs_goal_fn, waterjugs_h_sum_function)
    final = se.search()
    if final: final.print_path()
    print("===================================================")
    print("")

    print("=========Test 2. Astar with h_max heuristic========")
    se.init_search(s0, waterjugs_goal_fn, waterjugs_h_max_function)
    final = se.search()
    if final: final.print_path()        
    print("===================================================")
    print("")
    
    se.set_strategy('breadth_first')
    print("=========Test 3a. Breadth first (full cycle checking)==")
    se.init_search(s0, waterjugs_goal_fn)
    final = se.search()
    if final: final.print_path()    
    print("===================================================")
    print("")
    
    se.set_strategy('breadth_first', 'path')
    print("=========Test 3b. Breadth first with only path checking=====")
    se.init_search(s0, waterjugs_goal_fn)
    final = se.search()
    if final: final.print_path()    
    print("===================================================")
    print("")
    
    se.set_strategy('breadth_first', 'none')
    print("=========Test 3c. Breadth first with no cycle checking=====")
    se.init_search(s0, waterjugs_goal_fn)
    final = se.search()
    if final: final.print_path()    
    print("===================================================")
    print("")
    
    se.set_strategy('breadth_first', 'path')
    waterjugs_set_goal(2, 1)
    print("=========Test 4. Breadth first on unreachable goal with only path checking==")
    se.init_search(s0, waterjugs_goal_fn)
    final = se.search()
    if final: final.print_path()    
    print("========================================================")
    print("")
    
    se.set_strategy('breadth_first', 'full')
    waterjugs_set_goal(2, 1)
    print("=========Test 5. Breadth first on unreachable goal with full checking==")
    se.init_search(s0, waterjugs_goal_fn)
    final = se.search()
    if final: final.print_path()    
    print("========================================================")
    print("")
    
    se.set_strategy('depth_first')
    waterjugs_set_goal(2, 1)
    print("=========Test 6. Depth first on unreachable goal with path checking==")
    se.init_search(s0, waterjugs_goal_fn)
    final = se.search()
    if final: final.print_path()    
    print("========================================================")
    print("")

