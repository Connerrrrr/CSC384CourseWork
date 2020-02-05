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


def storage_finder(box, state):
    # find all the available storage spot for the box provided
    storages = []
    # Create a deep copy of storage in current state
    # in order to not mess up with the state status
    for place in state.storage:
        storages.append(place)
    # if the box is in the storage point already
    # just return the current box's position for indication of stored status
    if box in storages:
        return [box]
    # otherwise, find all the available storages for the box provided
    for other_boxes in state.boxes:
        if box != other_boxes and other_boxes in storages:
            storages.remove(other_boxes)
    return storages


def get_num_of_obstacles(origin, destination, state):
    # Find the number of obstacles including robots to get from the origin to destination
    result = 0
    obstacles = state.obstacles.union(frozenset(state.robots))
    for obstacle in obstacles:
        (leftbound, rightbound) = (min(origin[0], destination[0]), max(origin[0], destination[0]))
        (upperbound, lowerbound) = (min(origin[1], destination[1]), max(origin[1], destination[1]))
        if leftbound < obstacle[0] < rightbound and upperbound < obstacle[0] < lowerbound:
            result += 1
    return result


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

    possible_storage_pos = storage_finder(box, state)

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


def in_dead_state(state):
    # Check if the state is in dead end, which contains following scenarios
    # (1) one or more boxes are again the corner of the map
    # (2) one or more boxes are against the corner of the wall and obstacles or the corner of the two original obstacles
    # (3) one or more boxes are along the side of the map and there are no storages along that sides
    for box in state.boxes:
        possible_storage_positions = storage_finder(box, state)
        if box not in possible_storage_positions:
            if box_against_corner(box, state) or box_against_corner_of_obs_or_consec_boxes(box, state)\
                    or edge_without_storage(box, state):
                return True
    return False


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    # The improvement is made by the following:
    # (1) check if current state is a dead end already for following situations:
    #     (1) one or more boxes are again the corner of the map
    #     (2) one or more boxes are against the corner of the wall and obstacles
    #         or the corner of the two original obstacles
    #     (3) one or more boxes are along the side of the map and there are no storages along that sides
    # (2) it's hard to dynamically keep track of the optimal position for both boxes and robots, divide and conquer
    #     is going to be used:
    #     (1) overall distance from robots to boxes
    #     (2) overall distance from boxes to storages
    heur_alt = 0
    if in_dead_state(state):
        return float("inf")

    # When dealing with potential obstacles in the way, we assign the distance with doubled distance
    # for taking a detour, imagine the following:
    #   if one object wants to move up for two units and there is another object just above it,
    #   it needs to
    #       (1) turn right or left (1 unit)
    #       (2) go up for two units (2 units)
    #       (3) turn left or right (1 unit)
    #   As shown above, in general the detour has doubled the distance

    # Robot to box
    # Assign the closest box to each of the robotdef in_dead_state(state):
    #     # Check if the state is in dead end, which contains following scenarios
    #     # (1) one or more boxes are again the corner of the map
    #     # (2) one or more boxes are against the corner of the wall and obstacles or the corner of the two original obstacles
    #     # (3) one or more boxes are along the side of the map and there are no storages along that sides
    #     for box in state.boxes:
    #         possible_storage_positions = storage_finder(box, state)
    #         if box not in possible_storage_positions:
    #             if box_against_corner(box, state) or box_against_corner_of_obs_or_consec_boxes(box, state)\
    #                     or edge_without_storage(box, state):
    #                 return True
    #     return False
    for robot in state.robots:
        closest_distance = float("inf")
        for box in state.boxes:
            closest_distance = min(manhattan_distance(robot, box) + get_num_of_obstacles(robot, box, state) * 2,
                                   closest_distance)
        heur_alt += closest_distance

    # Box to storage
    # Assign the closest storage to each of the box
    for box in state.boxes:
        storages = storage_finder(box, state)
        min_cost = float("inf")
        for storage in storages:
            min_cost = min(manhattan_distance(storage, box) + get_num_of_obstacles(box, storage, state) * 2, min_cost)
        heur_alt += min_cost
    return heur_alt


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
    # Set up the time bound
    end_time = os.times()[0] + timebound
    time_remaining = timebound

    multiplier = 0.6

    # initialize the search engine
    engine = SearchEngine('custom', 'full')
    engine.init_search(initial_state, sokoban_goal_state, heur_fn, (lambda sN: fval_function(sN, weight)))

    # initialize the result and the upper bound of f
    result = False
    best_cost = float("inf")

    # Update the time bound
    time_remaining = end_time - os.times()[0]

    while time_remaining > 0:
        # search begin, leave 0.1 sec for later processing
        final_state = engine.search(time_remaining - 0.1, (float("inf"), float("inf"), best_cost))
        # decrease the weight within each iteration
        weight = weight * multiplier
        # Update the time bound
        time_remaining = end_time - os.times()[0]
        # if more optimal solution found, update the result and the cost bound
        if final_state:
            result = final_state
            best_cost = result.gval + heur_fn(result) - 1
        else:
            break
    return result


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    # Set up the time bound
    end_time = os.times()[0] + timebound
    time_remaining = timebound

    # initialize the search engine
    search_engine = SearchEngine(strategy="best_first", cc_level="full")
    search_engine.init_search(initial_state, sokoban_goal_state, heur_fn)

    #  Set default value for result and cost bound
    result = False
    cost_bound = (float("inf"), float("inf"), float("inf"))

    # Update the time bound
    time_remaining = end_time - os.times()[0]
    while time_remaining > 0:
        # search begin, leave 0.1 sec for later processing
        final_state = search_engine.search(time_remaining - 0.1, cost_bound)
        # Update the time bound
        time_remaining = end_time - os.times()[0]
        # if more optimal solution found, update the result and the cost bound
        if final_state:
            result = final_state
            cost_bound = (result.gval - 1, float('inf'), float('inf'))
        else:
            break
    return result
