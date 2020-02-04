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

# TODO
def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    heur_alt = 0
    if check_impossible(state):
        return float("inf")

    # Box to storage
    for box in state.boxes:
        possible_positions = get_possible_storage(box, state)
        cost_each_box = float("inf")
        for possibility in possible_positions:
            current_cost = manhattan_distance(possibility, box) + num_obstacles(box, possibility, state) * 2
            if current_cost < cost_each_box:
                cost_each_box = current_cost
        heur_alt += cost_each_box

    # Robot to box
    for rob in state.robots:
        # find the distance of the closest storage for each robot
        closest = float("inf")
        for box in state.boxes:
            if (manhattan_distance(box, rob) + num_obstacles(rob, box, state) * 2) < closest:
                closest = manhattan_distance(box, rob) + num_obstacles(rob, box, state) * 2
        heur_alt += closest
    return heur_alt


def check_impossible(state):
    # (1)the box is in corner
    # (2)the box in on edge and no storage avaliable in edge
    # return True if state is impossible, False otherwise
    for box in state.boxes:
        possible_storage_positions = get_possible_storage(box, state)
        if box not in possible_storage_positions:
            if box_against_corner(box, state):
                return True
            if box_against_corner_of_obs_or_consec_boxes(box, state):
                return True
            if edge_without_storage(box, state):
                return True
    return False


def box_against_corner(box, state):
    (x, y) = box
    # if the box is at left top or left bottom corner
    if x == 0 and (y == 0 or y == state.height - 1):
        return True
    # if the box is at left top or left bottom corner
    if x == state.width - 1 and (y == 0 or y == state.height - 1):
        return True
    return False


def box_against_corner_of_obs_or_consec_boxes(box, state):
    # For this function, obstacles contains original obstacles and other boxes
    # Two Major situations:
    # (1) box against the corner of the wall and obstacles
    # (2) box against the corner of the two original obstacles
    obstacles = state.obstacles.union(state.boxes)
    (x, y) = box
    up = (x, y + 1)
    down = (x, y - 1)
    left = (x - 1, y)
    right = (x + 1, y)
    # Situation (1)
    #  if box is against left-most wall, scenario like this: ⌈ or ⌊
    if x == 0 and ((up in obstacles) or (down in obstacles)):
        return True
    #  if box is against right-most wall, scenario like this: ⌉ or ⌋
    if x == state.width - 1 and ((up in obstacles) or (down in obstacles)):
        return True
    #  if box is against top-most wall, scenario like this: ⌈ or ⌉
    if y == 0 and ((left in obstacles) or (right in obstacles)):
        return True
    #  if box is against bottom-most wall, scenario like this: ⌊ or ⌋
    if y == state.height - 1 and ((left in obstacles) or (right in obstacles)):
        return True

    # Situation (2)
    # if box is against two original obstacles, scenario like this: ⌈ or ⌊
    if up in state.obstacles and ((left in state.obstacles) or (right in state.obstacles)):
        return True
    # if box is against two original obstacles, scenario like this: ⌉ or ⌋
    if down in state.obstacles and ((left in state.obstacles) or (right in state.obstacles)):
        return True
    return False


def edge_without_storage(box, state):
    # If the box is along the wall and there is no storage along that wall, this is a dead end
    (x, y) = box

    possible_storage_pos = get_possible_storage(box, state)

    (x_list, y_list) = ([], [])
    for coord in possible_storage_pos:
        x_list.append(coord[0])
        y_list.append(coord[1])
    # if the box is along left-most wall
    if x == 0 and (0 not in x_list):
        return True
    # if the box is along right-most wall
    elif x == (state.width - 1) and ((state.width - 1) not in x_list):
        return True
    # if the box is along top-most wall
    elif y == 0 and (0 not in y_list):
        return True
    # if the box is along bottom-most wall
    elif y == (state.height - 1) and ((state.width - 1) not in y_list):
        return True
    else:
        return False


# TODO
def num_obstacles(origin, destination, state):
    # return numbers of obstacles from origin to destination
    # robots on the way also considered as obstacles
    total = 0
    cast_rob = frozenset(state.robots)
    all_obs = state.obstacles | cast_rob
    for obstacle in all_obs:
        if max(destination[0], origin[0]) > obstacle[0] > min(origin[0], destination[0]):
            if max(destination[1], origin[1]) > obstacle[1] > min(origin[1], destination[1]):
                total += 1
    return total


# TODO
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


# TODO
def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    end_time = os.times()[0] + timebound
    time_remaining = timebound

    engine = SearchEngine('custom', 'full')
    engine.init_search(initial_state, sokoban_goal_state, heur_fn, (lambda sN: fval_function(sN, weight)))

    result = False

    # # first search
    # best_cost = float("inf")
    # result = engine.search(time_remaining, costbound=(float("inf"), float("inf"), best_cost))
    # time_remaining = end_time - os.times()[0]

    # if not result:  # no solution found
    #     return False
    # else:
    #     best_cost = result.gval + heur_fn(result)

    best_cost = float("inf")
    # while still time and frontier is not empty
    while time_remaining > 0:
        result = engine.search(time_remaining - 0.1, (float("inf"), float("inf"), best_cost))
        if result:  # better result found
            best_cost = result.gval + heur_fn(result)
            time_remaining = end_time - os.times()[0]
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
    time_remaining = timebound

    result = False

    cost_bound = (float("inf"), float("inf"), float("inf"))
    time = 0

    while time_remaining > 0:
        # print(time_remaining)
        # print(os.times()[0])
        final_state = search_engine.search(time_remaining - 0.1, cost_bound)

        if final_state:
            result = final_state
            # subtract one so search compares >= for costbound, not >
            # send in infinity for hval since solution.hval is always zero
            cost_bound = (result.gval - 1, float('inf'), float('inf'))
        else:
            break
        time_remaining = end_time - os.times()[0]
        # print(time_remaining)
        # time += 1
    # print("Searched {} times".format(time))
    return result
