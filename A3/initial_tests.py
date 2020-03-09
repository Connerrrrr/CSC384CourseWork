#!/usr/bin/env python
import os  # for time functions

# import student's functions
from agent import *

smallboards = [((0, 0, 0, 0), (0, 2, 1, 0), (0, 1, 1, 1), (0, 0, 0, 0)),
((0, 1, 0, 0), (0, 1, 1, 0), (0, 1, 2, 1), (0, 0, 0, 2)),
((0, 0, 0, 0), (0, 2, 1, 0), (0, 1, 1, 1), (0, 1, 1, 0)),
((0, 1, 0, 0), (0, 2, 2, 0), (0, 1, 2, 1), (0, 0, 2, 2)),
((1, 0, 0, 2), (1, 1, 2, 0), (1, 1, 1, 1), (1, 2, 2, 2)),
((0, 1, 0, 0), (0, 1, 1, 0), (2, 2, 2, 1), (0, 0, 0, 2))]

bigboards = [((0, 0, 0, 0, 0, 0), (0, 0, 2, 2, 0, 0), (0, 1, 1, 2, 2, 0), (2, 2, 1, 2, 0, 0), (0, 1, 0, 1, 2, 0), (0, 0, 0, 0, 0, 0)),
((0, 0, 0, 0, 0, 0), (0, 0, 1, 2, 0, 0), (0, 1, 1, 1, 1, 0), (2, 2, 1, 2, 0, 0), (0, 1, 0, 1, 2, 0), (0, 0, 0, 0, 0, 0)),
((0, 0, 0, 0, 1, 0), (0, 0, 1, 1, 0, 0), (0, 1, 1, 1, 1, 0), (2, 2, 1, 2, 0, 0), (0, 2, 0, 1, 2, 0), (0, 0, 2, 2, 1, 0)),
((0, 0, 0, 0, 0, 0), (0, 0, 0, 2, 0, 0), (0, 1, 2, 2, 2, 0), (0, 2, 2, 2, 0, 0), (0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0)),
((0, 0, 0, 0, 0, 0), (0, 0, 0, 2, 0, 0), (0, 1, 2, 1, 1, 0), (0, 2, 2, 2, 0, 0), (0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0))]

#Select what to test
test_compute_utility = True
test_alphabeta_min_node_1 = True
test_alphabeta_max_node_1 = True
test_minimax_min_node_1 = True
test_minimax_max_node_1 = True
test_alphabeta_min_node_2 = True
test_alphabeta_max_node_2 = True
test_minimax_min_node_2 = True
test_minimax_max_node_2 = True
test_caching_big = True
test_ordering = True
test_select_move_minimax = True
test_select_move_alphabeta = True
test_select_move_equal = True

if test_compute_utility:

    ##############################################################
    print('Testing Utility')
    correctvalues = [3, 3, 5, -2, 3, 0]
    correct = 0
    for i in range(0,len(smallboards)):
      board = smallboards[i]
      value1 = compute_utility(board, 1)
      value2 = compute_utility(board, 2)
      if (value1 == correctvalues[i] and value2 == correctvalues[i]*-1):
        correct+=1  

    print("You computed correct utilities for {} of {} small boards".format(correct, len(correctvalues)))

if test_select_move_minimax:
    correctmoves_1 = [(0,0),(2,3),(0,0),(3,0),(3,1), (0,3)]
    correctmoves_2 = [(3,3),(0,0),(3,3),(0,2),(3,1),(0,0)]
    correct = 0
    for i in range(0,len(smallboards)):
      board = smallboards[i]
      value1 = select_move_minimax(board, 1, 6)
      value2 = select_move_minimax(board, 2, 6)
      if (value1 == correctmoves_1[i] and value2 == correctmoves_2[i]):
        correct+=1  
    print('Testing Minimax (no Depth Limit)')
    print("You computed correct minimax moves for {} of {} small boards".format(correct, len(correctmoves_1)))

if test_select_move_alphabeta:
    correctmoves_1 = [(0,0),(2,3),(0,0),(3,0),(3,1), (0,3)]
    correctmoves_2 = [(3,3),(0,0),(3,3),(0,2),(3,1),(0,0)]
    correct = 0
    for i in range(0,len(smallboards)):
      board = smallboards[i]
      value1 = select_move_alphabeta(board, 1, 6)
      value2 = select_move_alphabeta(board, 2, 6)
      if (value1 == correctmoves_1[i] and value2 == correctmoves_2[i]):
        correct+=1  
    print('Testing Alphabeta (no Depth Limit)')
    print("You computed correct alphabeta moves for {} of {} small boards".format(correct, len(correctmoves_1)))
  
if test_select_move_equal:
    correctmoves_1 = [(0,0),(2,3),(0,0),(3,0),(3,1)]
    correctmoves_2 = [(3,3),(0,0),(3,3),(0,2),(3,1)]
    correct = 0
    for i in range(0,len(correctmoves_1)):
      board = smallboards[i]
      value1_minimax = select_move_minimax(board, 1, 6)
      value2_minimax = select_move_minimax(board, 2, 6)
      value1_ab = select_move_alphabeta(board, 1, 6)
      value2_ab = select_move_alphabeta(board, 2, 6)
      if (value1_minimax == value1_ab == correctmoves_1[i] and value2_minimax == value2_ab == correctmoves_2[i]):
        correct+=1  

    print('Testing Minimax and Alphabeta Moves Equality (no Depth Limit)')
    print("You computed correct moves for {} of {} tests".format(correct, len(correctmoves_1)))

if test_caching_big:

    print('Testing Caching Big')
    check_1 = 0
    check_2 = 0  
    for i in range(0,len(bigboards)):

      start_time_1 = os.times()[0]
      no_cache = select_move_alphabeta(bigboards[i], 1, 6)
      end_time_1 = os.times()[0]

      start_time_2 = os.times()[0]
      with_cache = select_move_alphabeta(bigboards[i], 1, 6, 1)
      end_time_2 = os.times()[0]

      if (end_time_1 - start_time_1) >= (end_time_2 - start_time_2):
        check_1 += 1

      if (with_cache == no_cache):
         check_2 += 1       

    print("State caching improved the time of your alpha-beta for {} of {} boards".format(check_1, len(bigboards))) 
    print("Move choice with and without caching is the same for {} of {} boards".format(check_2, len(bigboards)))
    
if test_ordering:

    print('Testing Ordering')
    check_1 = 0
    check_2 = 0  
    for i in range(0,len(bigboards)):

      start_time_1 = os.times()[0]
      no_order = select_move_alphabeta(bigboards[i], 1, 6, 0, 0)
      end_time_1 = os.times()[0]

      start_time_2 = os.times()[0]
      with_order = select_move_alphabeta(bigboards[i], 1, 6, 0, 1)
      end_time_2 = os.times()[0]

      if (end_time_1 - start_time_1) >= (end_time_2 - start_time_2):
        check_1 += 1

      if (with_order == no_order):
         print(with_order)
         print(no_order)
         check_2 += 1       

    print("Node ordering improved the time of your alpha-beta for {} of {} boards".format(check_1, len(bigboards))) 
    

if test_alphabeta_min_node_1:

    print('Testing Alpha Beta Min Node - Player 1')
    answers = [((2,4),-10),((1,1),-4),((3,0),-6),((0,1),-8),((5,2),-6)]
    correct = 0
    correctval = 0
    for i in range(0,len(bigboards)):
      board = bigboards[i]

      color = 1
      (move, value) = alphabeta_min_node(board, color, float("-Inf"), float("Inf"), 1, 0, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct alpha-beta min moves for {} of {} boards".format(correct, len(bigboards))) 
    print("You computed correct alpha-beta min values for {} of {} boards".format(correctval, len(bigboards))) 


if test_alphabeta_max_node_1:

    print('Testing Alpha Beta Max Node - Player 1')
    answers = [(),((5,5),8),((1,5),12),(),((3,4),4)]
    correct = 0
    correctval = 0
    selected = [1,2,4] #some boards have moves that are tied in value
    for i in selected:
      board = bigboards[i]

      color = 1
      (move, value) = alphabeta_max_node(board, color, float("-Inf"), float("Inf"), 1, 0, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct alpha-beta max moves for {} of {} boards".format(correct, len(selected))) 
    print("You computed correct alpha-beta max values for {} of {} boards".format(correctval, len(selected))) 


if test_minimax_min_node_1:
    ##############################################################
    # Must program some trees where we know cut set
    ##############################################################

    print('Testing Minimax Min Node - Player 1')
    answers = [((2,4),-10),((1,1),-4),((3,0),-6),((0,1),-8),((5,2),-6)]
    correct = 0
    correctval = 0
    for i in range(0,len(bigboards)):
      board = bigboards[i]

      color = 1
      (move, value) = minimax_min_node(board, color, 1, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct minimax min moves for {} of {} boards".format(correct, len(bigboards))) 
    print("You computed correct minimax min values for {} of {} boards".format(correctval, len(bigboards))) 

if test_minimax_max_node_1:

    print('Testing Minimax Max Node - Player 1')  
    answers = [(),((5,5),8),((1,5),12),(),((3,4),4)]
    correct = 0
    correctval = 0
    selected = [1,2,4] #some boards have moves that are tied in value
    for i in selected:
      board = bigboards[i]

      color = 1
      (move, value) = minimax_max_node(board, color, 1, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct minimax max moves for {} of {} boards".format(correct, len(selected))) 
    print("You computed correct minimax max values for {} of {} boards".format(correctval, len(selected))) 

if test_alphabeta_min_node_2:

    print('Testing Alpha Beta Min Node - Player 2')
    answers = [((3,0),-6),((5,5),-8),((1,5),-12),((5,2),-2),((3,4),-4)]
    correct = 0
    correctval = 0
    for i in range(0,len(bigboards)):
      board = bigboards[i]

      color = 2
      (move, value) = alphabeta_min_node(board, color, float("-Inf"), float("Inf"), 1, 0, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct alpha-beta min moves for {} of {} boards".format(correct, len(bigboards))) 
    print("You computed correct alpha-beta min values for {} of {} boards".format(correctval, len(bigboards))) 


if test_alphabeta_max_node_2:

    print('Testing Alpha Beta Max Node - Player 2')
    answers = [((0,0),0),((1,1),4),((3,0),6),((0,0),0),((5,2), 6),((0,0), 0)]
    correct = 0
    correctval = 0
    selected = [1,2,4] #some boards have moves that are tied in value
    for i in selected:
      board = bigboards[i]

      color = 2
      (move, value) = alphabeta_max_node(board, color, float("-Inf"), float("Inf"), 1, 0, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct alpha-beta max moves for {} of {} boards".format(correct, len(selected))) 
    print("You computed correct alpha-beta max values for {} of {} boards".format(correctval, len(selected))) 


if test_minimax_min_node_2:
    ##############################################################
    # Must program some trees where we know cut set
    ##############################################################

    print('Testing Minimax Min Node - Player 2')
    answers = [((3,0),-6),((5,5),-8),((1,5),-12),((5,2),-2),((3,4),-4)]
    correct = 0
    correctval = 0
    for i in range(0,len(bigboards)):
      board = bigboards[i]

      color = 2
      (move, value) = minimax_min_node(board, color, 1, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct minimax min moves for {} of {} boards".format(correct, len(bigboards))) 
    print("You computed correct minimax min values for {} of {} boards".format(correctval, len(bigboards))) 

if test_minimax_max_node_2:

    print('Testing Minimax Max Node - Player 2')  
    answers = [((0,0),0),((1,1),4),((3,0),6),((0,0),0),((5,2), 6),((0,0), 0)]
    correct = 0
    correctval = 0
    selected = [1,2,4] #some boards have moves that are tied in value
    for i in selected:
      board = bigboards[i]

      color = 2
      (move, value) = minimax_max_node(board, color, 1, 0)
      answer = answers[i][0]
      answer_value = answers[i][1]

      if (answer[0] == move[0] and answer[1] == move[1]):
        correct+=1
      if (answer_value == value):
        correctval+=1      

    print("You computed correct minimax max moves for {} of {} boards".format(correct, len(selected))) 
    print("You computed correct minimax max values for {} of {} boards".format(correctval, len(selected))) 
