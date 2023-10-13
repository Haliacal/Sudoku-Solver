import numpy as np
from string import whitespace as WHITESPACE

board = [
  [1,7,4,3,8,2,9,5,6],
  [2,9,5,4,6,7,1,3,8],
  [3,8,6,9,5,1,4,0,0],
  [4,6,1,5,2,3,8,0,7],
  [7,3,8,1,0,9,6,0,0],
  [9,5,2,8,7,6,3,1,0],
  [5,2,9,6,3,4,7,8,1],
  [6,1,7,2,9,8,5,4,3],
  [8,4,3,7,1,5,2,6,0]
]

board = np.array(board)

def nineNumCheck(Board_array, allow_zeroes=False):
  check = True
  for i in Board_array:
    # i is each line in the array

    # Allow zeroes for ingame and endgame results
    if(not allow_zeroes): DIGITS  = [1,2,3,4,5,6,7,8,9]
    else: DIGITS  = [1,2,3,4,5,6,7,8,9,0]
    for j in i:
      # removes the corresponding number if in digits
      # if it isn't there then there are two numbers in the same line
      if(j not in DIGITS):
        check = False
        break
      else: 
        if(allow_zeroes and j == 0): continue
        else: DIGITS.remove(j)
  return check

def squaresCheck(Board_array, allow_zeroes=False):
  squares = []
  start_col = 0 # 'start' col
  end_col = 3 # 'end' row
  for _ in range(3):
    start_row = 0 # 'start' row
    end_row = 3 # 'end' row

    # iterates accross the board checking for the squares from top to bottom
    # e.g In order of checking Boxes: top left , middle left, bottom left , top middle .
    for _ in range(3):
      # Reshapes all boxes into lines
      squares.append(Board_array[start_row:end_row, start_col:end_col].reshape(-1))
      start_row += 3
      end_row += 3
    
    start_col += 3 
    end_col += 3
  
  # Check for reiterations of elements in those lines
  return nineNumCheck(squares,allow_zeroes)

def goalState(board, check=True):
  # Copies the board as to not change the original board
  grid = np.copy(board)

  # Check horizontal lines
  check = nineNumCheck(grid)

  # Check vertical lines
  # Transpose swaps columns and rows
  if(check): check = nineNumCheck(grid.transpose())
    
  # Check the Squares
  if(check): check = squaresCheck(grid)  
  return check

def posMoves(board):

  grid = np.copy(board)
  trans_grid = grid.transpose()
  pos_moves = []
  valid_pos_moves = []

  # Runs through each row 
  for row,i in enumerate(grid):
    DIGITS = [1,2,3,4,5,6,7,8,9]

    # Removes all numbers that are already in the row
    for j in i:
      if(j in DIGITS):
        DIGITS.remove(j)
    
    # Runs through each element in the row 
    for column,k in enumerate(i):
      temp_grid = np.copy(grid)
      temp_DIGITS = np.copy(DIGITS)

      # If 0 then it can have poss. moves
      if(k == 0):
        # Remove all elements in that elements column 
        for l in trans_grid[column]:
          if(l in temp_DIGITS):
            temp_DIGITS = np.delete(temp_DIGITS, np.argwhere(temp_DIGITS == l))
      
        # Append all poss. actions
        for m in temp_DIGITS:
          if(str(m) not in WHITESPACE):
            temp_grid[row][column] = m
            pos_moves.append(temp_grid)

  # Checks squares and removes if invalid
  for i in pos_moves:
    if(squaresCheck(i,True)): 
      valid_pos_moves.append(i)

  return valid_pos_moves

# Checks if the 'element' is in the list
# This must be done because its numpy array -_-
def isIn(list,element,check=False):
  for i in list:
    comparing = (i == element)
    # Checks if every single element is the same 
    if(comparing.all()):
          check = True
          break

  return check

def sudoku_solver(board):
  state = np.array(np.copy(board))
  stack = [state]
  explored = []
  generated = 0

  # Initialises the false board
  rows = 9
  columns = 9
  false_board = [[-1] * rows for i in range(columns)]

  current_state = stack.pop()
  while(not goalState(current_state)):

    explored.append(current_state) # Appends all current state
    pos_moves = posMoves(current_state) # Calculates all poss. moves
    
    for new_state in pos_moves:
      generated += 1

      # For all poss. moves check if they are
      # already in the stack or explored
      in_explored = isIn(explored,new_state)
      in_stack = isIn(stack,new_state)
      
      # If its not in either append to the stack
      if((not in_explored) and (not in_stack)): stack.append(new_state)

    if(len(stack) == 0):
      # If the stack is empty then that means there is no solution
      # Because everything has already been explored
      print("No solution found.")
      return false_board
    
    current_state = stack.pop()
    
  
  print("Solution found.")
  return current_state

print(sudoku_solver(board))