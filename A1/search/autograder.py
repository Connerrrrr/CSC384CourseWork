if __name__ == "__main__":
  import multiprocessing

  # import student's functions
  from solution import *
  from sokoban import sokoban_goal_state

  # Select what to test

  test_time_astar = True
  test_time_gbfs = True
  test_manhattan = True
  test_fval_function = True
  test_anytime_gbfs = True
  test_alternate = True
  test_anytime_weighted_astar = True

  # test_time_astar = False
  # test_time_gbfs = False
  # test_manhattan = False
  # test_fval_function = False
  # test_anytime_gbfs = False
  # test_alternate = False
  # test_anytime_weighted_astar = False

  if test_time_astar:

    time_bound = 3
    p = multiprocessing.Process(target=anytime_weighted_astar, name="Anytime A star",
                                args=(PROBLEMS[19], heur_alternate, 10, time_bound))
    p.start()
    p.join(3.1)
    if p.is_alive():

      print('Process killed. anytime_weighted_astar() not keeping track of time properly\n')
      p.terminate()
      p.join()
    else:
      print('anytime_weighted_astar did not exceed timebound\n')

  if test_time_gbfs:

    time_bound = 3
    p = multiprocessing.Process(target=anytime_gbfs, name="Anytime GBFS", args=(PROBLEMS[19], heur_alternate, time_bound))
    p.start()
    p.join(3.1)
    if p.is_alive():

      print('Process killed. anytime_gbfs() not keeping track of time properly\n')
      p.terminate()
      p.join()
    else:
      print('anytime_gbfs did not exceed timebound\n')

  if test_manhattan:
    ##############################################################
    # TEST MANHATTAN DISTANCE
    print('Testing Manhattan Distance')

    # Correct Manhattan distances for the initial states of the provided problem set
    correct_man_dist = [8, 2, 8, 3, 3, 11, 7, 11, 10,
                        12, 12, 13, 10, 13, 10, 35, 28,
                        41, 43, 36]

    solved = 0;
    unsolved = [];

    for i in range(0, 20):
      # print("PROBLEM {}".format(i))

      s0 = PROBLEMS[i]

      man_dist = heur_manhattan_distance(s0)
      print('calculated man_dist:', str(man_dist))
      # To see state
      # print(s0.state_string())

      if man_dist == correct_man_dist[i]:
        solved += 1
      else:
        unsolved.append(i)

    print("*************************************")
    print("In the problem set provided, you calculated the correct Manhattan distance for {} states out of 20.".format(
      solved))
    print("States that were incorrect: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

  if test_alternate:

    ##############################################################
    # TEST ALTERNATE HEURISTIC
    print('Testing alternate heuristic with best_first search')

    solved = 0;
    unsolved = [];
    benchmark = 12;
    timebound = 8  # time limit
    output = [20, 5, 29, 12, 13, -99, 18, 41, 16, -99, 42, 38, -99, 43, 37, -99, -99, -99, -99, -99]
    for i in range(0, len(PROBLEMS)):

      print("*************************************")
      print("PROBLEM {}".format(i))

      s0 = PROBLEMS[i]  # Problems get harder as i gets bigger

      # s0.print_path()

      se = SearchEngine('best_first', 'full')
      se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_alternate)
      final = se.search(timebound)

      if final:
        print(final.gval, output[i])
      else:
        print(final, output[i])

      if final:
        # final.print_path()
        solved += 1
      else:
        unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("The benchmark implementation solved {} out of {} practice problems given {} seconds.".format(benchmark,
                                                                                                        len(PROBLEMS),
                                                                                                        timebound))
    print("*************************************\n")
    ##############################################################

  if test_fval_function:

    test_state = SokobanState("START", 6, None, None, None, None, None, None, None)

    correct_fvals = [6, 11, 16]

    ##############################################################
    # TEST fval_function
    print("*************************************")
    print('Testing fval_function')

    solved = 0
    weights = [0., .5, 1.]
    for i in range(len(weights)):

      test_node = sNode(test_state, hval=10, fval_function=fval_function)

      fval = fval_function(test_node, weights[i])
      print('Test', str(i), 'calculated fval:', str(fval), 'correct:', str(correct_fvals[i]))

      if fval == correct_fvals[i]:
        solved += 1

    print("\n*************************************")
    print("Your fval_function calculated the correct fval for {} out of {} tests.".format(solved, len(correct_fvals)))
    print("*************************************\n")
    ##############################################################

  if test_anytime_gbfs:

    len_benchmark = [18, 4, 21, 12, 9, -99, 18, 41, 14, -99, 39, 38, -99, 34, 29, -99, -99, -99, -99, -99]

    ##############################################################
    # TEST ANYTIME GBFS
    print('Testing Anytime GBFS')

    solved = 0;
    unsolved = [];
    benchmark = 0;
    timebound = 8  # 8 second time limit
    for i in range(0, len(PROBLEMS)):
      print("*************************************")
      print("PROBLEM {}".format(i))

      s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
      weight = 10
      final = anytime_gbfs(s0, heur_fn=heur_alternate, timebound=timebound)

      if final:
        print(final.gval, len_benchmark[i])
      else:
        print(final, len_benchmark[i])

      if final:
        # output.append(final.gval)
        if i < len(len_benchmark):
          index = i
        else:
          index = 0
        # final.print_path()

        if final.gval <= len_benchmark[index] or len_benchmark[index] == -99:
          benchmark += 1
        solved += 1
      else:
        unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved,
                                                                                                              benchmark))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("The benchmark implementation solved 12 out of the 20 practice problems given 8 seconds.")
    print("*************************************\n")

  if test_anytime_weighted_astar:

    len_benchmark = [18, 4, 21, 10, 8, -99, 16, 41, 16, -99, 39, 38, -99, 35, 29, -99, -99, -99, -99, -99]

    output = []

    ##############################################################
    # TEST ANYTIME WEIGHTED A STAR
    print('Testing Anytime Weighted A Star')

    solved = 0;
    unsolved = [];
    benchmark = 0;
    timebound = 8  # 8 second time limit
    for i in range(0, len(PROBLEMS)):
      print("*************************************")
      print("PROBLEM {}".format(i))

      s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
      weight = 10
      final = anytime_weighted_astar(s0, heur_fn=heur_alternate, weight=weight, timebound=timebound)

      if final:
        print(final.gval, len_benchmark[i])
      else:
        print(final, len_benchmark[i])

      if final:
        if i < len(len_benchmark):
          index = i
        else:
          index = 0
          # final.print_path()
        if final.gval <= len_benchmark[index] or len_benchmark[index] == -99:
          benchmark += 1
        solved += 1
      else:
        unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved,
                                                                                                              benchmark))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("The benchmark implementation solved 12 out of the 20 practice problems given 8 seconds.")
    print("*************************************\n")
    ##############################################################
