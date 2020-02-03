#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems


def sokoban_goal_state(state):
    '''
  @return: Whether all boxes are stored.
  '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def manhattan_distance(obj_one, obj_two):
    return abs(obj_one[0] - obj_two[0]) + abs(obj_one[1] - obj_two[1])


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    distance_sum = 0
    for box in state.boxes:
        distances = list()
        for storage in state.storage:
            curr_dis = manhattan_distance(box, storage)
            distances.append(curr_dis)
        if len(distances) > 0:
            distance_sum += min(distances)
    return distance_sum


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    heru_alt = 0
    # our cost consist of two components: the cost of the box in current position to our final storage +
    #                                     the cost of (closest) robert need to walk to position of the box
    if check_impossible(state):
        return float("inf")
    heru_alt += box_to_dest(state)
    heru_alt += rob_to_box(state)
    return heru_alt


def check_impossible(state):
    # impossible cases consists of two situations
    # (1)the box is in corner
    # (2)the box in on edge and no storage avaliable in edge
    # return True if state is impossible, False otherwise
    for box in state.boxes:
        possible_storage_positions = get_possible_storage(box, state)
        if box not in possible_storage_positions:
            if is_movable(box, state):
                return True
            if is_edged(box, state):
                return True
    return False


def is_movable(box_pos, state):
    # helper function for check_impossible
    # check if a block is cornered given the position of the block and the size of the map
    # obst_list includes other boxes
    obst_list = state.obstacles | state.boxes
    up_pos = (box_pos[0], box_pos[1]+1)
    down_pos = (box_pos[0], box_pos[1]-1)
    left_pos = (box_pos[0]-1, box_pos[1])
    right_pos = (box_pos[0]+1, box_pos[1])
    # first test if there are walls,then any consecutive boxes are immovable
    if box_pos[0] == 0:
        if box_pos[1] == 0:
            return True
        if box_pos[1] == state.height - 1:
            return True
        if up_pos in obst_list:
            return True
        if down_pos in obst_list:
            return True
        return False
    if box_pos[0] == state.width - 1:
        if box_pos[1] == 0:
            return True
        if box_pos[1] == state.height - 1:
            return True
        if up_pos in obst_list:
            return True
        if down_pos in obst_list:
            return True
        return False
    # no walls but surrounded by obstacles
    if up_pos in state.obstacles:
        if left_pos in state.obstacles:
            return True
        if right_pos in state.obstacles:
            return True
    if down_pos in state.obstacles:
        if left_pos in state.obstacles:
            return True
        if right_pos in state.obstacles:
            return True
    return False


def is_edged(box_pos, state):
    # if the box is on edge,and there is no storage along the side, then it is still an impossible position
    possible_storage_pos = get_possible_storage(box_pos, state)
    x_list = [pos[0] for pos in possible_storage_pos]
    y_list = [pos[1] for pos in possible_storage_pos]
    if box_pos[0] == 0:
        if not any(i == 0 for i in x_list):
            return True
    if box_pos[0] == (state.width - 1):
        if not any(i == (state.width - 1) for i in x_list):
            return True
    if box_pos[1] == (state.height - 1):
        if not any(i == state.height - 1 for i in y_list):
            return True
    if box_pos[1] == 0:
        if not any(i == 0 for i in y_list):
            return True
    return False


def num_obstacles(ori, dest, state):
    # return numbers of obstacles from ori to dest
    # robots on the way also considered as obstacles
    total = 0
    cast_rob = frozenset(state.robots)
    all_obs = state.obstacles|cast_rob
    for obst in all_obs:
        if max(dest[0], ori[0]) > obst[0] > min(ori[0], dest[0]):
            if max(dest[1], ori[1]) > obst[1] > min(ori[1], dest[1]):
                total += 1
    return total


def get_possible_storage(box, state):
    # see the storage is avaliable,
    # remove from the list if the any storage is already occupied.
    possible = []
    for place in state.storage:
        possible.append(place)
    if box in possible:
        return [box]
    for other_boxes in state.boxes:
        if box != other_boxes:
            if other_boxes in possible:
                possible.remove(other_boxes)
    return possible


def box_to_dest(state):
    # return value of the sum of box to its closest possible positions
    # add considerations of obstacles along the side
    cost = 0
    for box in state.boxes:
        possible_positions = get_possible_storage(box, state)
        cost_each_box = float("inf")
        for possibility in possible_positions:
            current_cost = manhattan_distance(possibility, box) + num_obstacles(box, possibility, state) * 2
            if current_cost < cost_each_box:
                cost_each_box = current_cost
        cost += cost_each_box
    return cost


def rob_to_box(state):
    # return value of sum of all robert to its closest box,
    # add considerations of obstacles along the side
    cost = 0
    for rob in state.robots:
        # find the distance of the closest storage for each robot
        closest = float("inf")
        for box in state.boxes:
            if (manhattan_distance(box, rob) + num_obstacles(rob, box, state) * 2) < closest:
                closest = manhattan_distance(box, rob) + num_obstacles(rob, box, state)*2
        cost += closest
    return cost
# ---------------------------------------------------------------------


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    fval = sN.gval + (weight * sN.hval)
    return fval


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    initial_time = os.times()[0]
    time_remaining = timebound
    engine = SearchEngine('custom', 'full')
    engine.init_search(initial_state, sokoban_goal_state, heur_fn, (lambda sN: fval_function(sN, weight)))
    # first search
    best_cost = float("inf")
    result = engine.search(time_remaining, costbound=(float("inf"), float("inf"), best_cost))
    time_remaining = timebound - (os.times()[0] - initial_time)
    if not result:  # no solution found
        return False
    else:
        best_cost = result.gval + heur_fn(result)

    # while still time and frontier is not empty
    while time_remaining > 0 and not engine.open.empty():
        better_result = engine.search(time_remaining, (float("inf"), float("inf"), best_cost))
        time_remaining = timebound - (os.times()[0] - initial_time)
        if better_result:  # better result found
            best_cost = better_result.gval + heur_fn(better_result)
            result = better_result
        else:
            break
    return result


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    search_engine = SearchEngine(strategy="best_first", cc_level="full")
    search_engine.init_search(initial_state, sokoban_goal_state, heur_fn)

    end_time = os.times()[0] + timebound

    result = False

    cost_bound = (float("inf"), float("inf"), float("inf"))
    time = 0
    while os.times()[0] <= end_time:
        final_state = search_engine.search(end_time - os.times()[0], cost_bound)
        if final_state:
            result = final_state
            # subtract one so search compares >= for costbound, not >
            # send in infinity for hval since solution.hval is always zero
            cost_bound = (result.gval - 1, float('inf'), float('inf'))
        else:
            break
        time += 1
    print("Searched {} times".format(time))
    return result
