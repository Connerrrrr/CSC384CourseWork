#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    if not newVar:
        return True, []

    def prop_FCCheck(C, x):
        '''Return False if DWO, and True otherwise'''
        domain = x.cur_domain()
        for d in domain:
            # assign d to provided var
            x.assign(d)
            # get all the vals for vars
            vals = []
            vars = C.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            # if falsifies, prune current value
            if not C.check(vals):
                x.prune_value(d)
            x.unassign()
        if x.cur_domain_size() == 0:
            return False
        return True

    for c in csp.get_cons_with_var(newVar):
        DWOoccured = False

        if c.get_n_unasgn() == 1:
            # get only one unassigned variable x
            x = c.get_unasgn_vars()[0]

            if not prop_FCCheck(c, x):
                DWOoccured = True
                break

            if DWOoccured:
                return False, []
    return True, []


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    for var in csp.get_all_vars():
        print(var, var.cur_domain())
    print()
    if newVar:
        GACQueue = csp.get_cons_with_var(newVar)
    else:
        GACQueue = csp.get_all_cons()
    nGACQueue = []
    # GAC Enforce helper
    def prop_GAC_Enforce():
        '''Return False if DWO, and True otherwise'''
        while len(GACQueue) > 0:
            c = GACQueue.pop(0)
            for v in c.get_scope():
                for d in v.cur_domain():
                    if not c.has_support(v, d):
                        print("Pruned value {} for {}".format(d, v))
                        v.prune_value(d)
                        if v.cur_domain_size == 0:
                            GACQueue.clear()
                            print(False)
                            return False
                        else:
                            for c_prime in nGACQueue:
                                if v in c_prime.get_scope():
                                    GACQueue.append(c)
                                    nGACQueue.remove(c)
        print(True)
        return True

    # if not newVar:
    #     return True, []

    v = ord_mrv(csp)
    curDom = v.domain()
    print(curDom)
    for d in curDom:

        prune_list = []
        for val in curDom:
            if val != d:
                prune_list.append(val)

        for c in nGACQueue:
            if v in c.get_scope():
                GACQueue.append(c)
                nGACQueue.remove(c)

        if prop_GAC_Enforce():
            prop_GAC(csp)
    return True, []


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    vars = csp.get_all_unasgn_vars()
    smallest_dom_size = float("inf")
    result = None
    for var in vars:
        if var.cur_domain_size() < smallest_dom_size:
            smallest_dom_size = var.cur_domain_size()
            result = var
    return result
