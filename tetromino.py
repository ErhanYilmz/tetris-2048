from tile import Tile  # used for modeling each tile on the tetrominoes
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # the random module is used for generating random values
import numpy as np  # the fundamental Python module for scientific computing

# A class for modeling tetrominoes (all 7 types: I, O, Z, S, T, J, L)
class Tetromino:
   # a constant to store the shape (as non-empty cells) for each tetromino type
   # (see the documentation given with this code)
   SHAPES = {
      # (column_index, row_index) for each non-empty cell (tile)
      'I': [(1,0), (1,1), (1,2), (1,3)],
      'O': [(0,0), (0,1), (1,0), (1,1)],
      'Z': [(0,1), (1,1), (1,2), (2,2)],
      # --- added shapes ---
      'S': [(1,1), (2,1), (0,2), (1,2)],
      'T': [(0,1), (1,1), (2,1), (1,2)],
      'J': [(0,1), (0,2), (1,1), (2,1)],
      'L': [(0,1), (1,1), (2,1), (2,2)]
   }

   # the dimensions of the game grid (defined as class variables)
   grid_height, grid_width = None, None

   # A constructor that creates a tetromino with a given type (shape)
   def __init__(self, type):
      self.type = type  # set the type of this tetromino
      # determine the size of the tile matrix based on the type of this tetromino
      if self.type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
      elif self.type == 'O':
         n = 2
      else:
         n = 3  # J, L, S, T, Z all fit in a 3x3 matrix
      # create a matrix of numbered tiles based on the shape of this tetromino
      # (this matrix stores Tile objects and None is stored for each empty cell)
      self.tile_matrix = np.full((n, n), None)
      # each tetromino has four tiles (minos)
      for i in range(4):
         col_index, row_index = self.SHAPES[type][i][0], self.SHAPES[type][i][1]
         self.tile_matrix[row_index][col_index] = Tile()
      # initialize the position of this tetromino (as the bottom left cell in
      # the tile matrix) with a random horizontal position above the game grid
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = Tetromino.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)

   # A method that computes and returns the position of the cell in the tile
   # matrix specified by the given row and column indexes
   def get_cell_position(self, row, col):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      position = Point()
      # horizontal position of the cell
      position.x = self.bottom_left_cell.x + col
      # vertical position of the cell
      position.y = self.bottom_left_cell.y + (n - 1) - row
      return position

   # A method to return a copy of the tile matrix without any empty row/column,
   # and the position of the bottom left cell when return_position is set
   def get_min_bounded_tile_matrix(self, return_position=False):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # determine rows and columns to copy (omit empty rows and columns)
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      # copy the tiles from the tile matrix of this tetromino
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
      # return just the matrix copy when return_position is not set (as True)
      # the parameter return_position defaults to False when a value is not given
      if not return_position:
         return copy
      # otherwise return the position of the bottom left cell in copy as well
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position

   # A method for drawing the tetromino on the game grid
   def draw(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each tile of the tetromino on the game grid
            if self.tile_matrix[row][col] is not None:
               # get the position of the tile
               position = self.get_cell_position(row, col)
               # draw only the tiles that are inside the game grid
               if position.y < Tetromino.grid_height:
                  self.tile_matrix[row][col].draw(position)

   # A method for moving this tetromino in a given direction by 1 on the grid
   def move(self, direction, game_grid):
      # check if this tetromino can be moved in the given direction by using
      # the can_be_moved method defined below
      if not (self.can_be_moved(direction, game_grid)):
         return False  # the tetromino cannot be moved in the given direction
      # move this tetromino by updating the position of its bottom left cell
      if direction == 'left':
         self.bottom_left_cell.x -= 1
      elif direction == 'right':
         self.bottom_left_cell.x += 1
      else:  # direction == 'down'
         self.bottom_left_cell.y -= 1
      return True  # a successful move in the given direction

   # A method for rotating this tetromino 90 degrees clockwise
   def rotate(self, game_grid):
      n = len(self.tile_matrix)
      # create a new n x n matrix to store the rotated tiles
      rotated = np.full((n, n), None)
      # rotate 90 degrees clockwise: new[col][n-1-row] = old[row][col]
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               rotated[col][n - 1 - row] = self.tile_matrix[row][col]
      # save the old tile matrix in case rotation is not valid
      old_matrix = self.tile_matrix
      self.tile_matrix = rotated
      # check if the rotated position is valid (inside grid and no collision)
      if not self.is_valid_position(game_grid):
         # if not valid, revert back to the original matrix
         self.tile_matrix = old_matrix

   # A method to check if the current position of the tetromino is valid
   # (all tiles must be inside the grid and not collide with locked tiles)
   def is_valid_position(self, game_grid):
      n = len(self.tile_matrix)
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               pos = self.get_cell_position(row, col)
               # check if the tile is outside the grid boundaries
               if pos.x < 0 or pos.x >= Tetromino.grid_width:
                  return False
               if pos.y < 0:
                  return False
               # check if the tile collides with a locked tile on the grid
               if game_grid.is_occupied(pos.y, pos.x):
                  return False
      return True

   # A method for hard dropping the tetromino (instantly drop to the bottom)
   def hard_drop(self, game_grid):
      # keep moving down until the tetromino cannot move anymore
      while self.can_be_moved('down', game_grid):
         self.bottom_left_cell.y -= 1

   # A method for checking if this tetromino can be moved in a given direction
   def can_be_moved(self, direction, game_grid):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # check for moving left or right
      if direction == 'left' or direction == 'right':
         for row_index in range(n):
            for col_index in range(n):
               # direction = left --> check the leftmost tile of each row
               row, col = row_index, col_index
               if direction == 'left' and self.tile_matrix[row][col] is not None:
                  # the position of the leftmost tile of the current row
                  leftmost = self.get_cell_position(row, col)
                  # if any leftmost tile is at x = 0
                  if leftmost.x == 0:
                     return False  # this tetromino cannot be moved left
                  # if the grid cell on the left of a leftmost tile is occupied
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False  # this tetromino cannot be moved left
                  # as the leftmost tile of the current row is checked
                  break  # end the inner for loop
               # direction = right --> check the rightmost tile of each row
               row, col = row_index, n - 1 - col_index
               if direction == 'right' and self.tile_matrix[row][col] is not None:
                  # the position of the rightmost tile of the current row
                  rightmost = self.get_cell_position(row, col)
                  # if any rightmost tile is at x = grid_width - 1
                  if rightmost.x == Tetromino.grid_width - 1:
                     return False  # this tetromino cannot be moved right
                  # if the grid cell on the right of a rightmost tile is occupied
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False  # this tetromino cannot be moved right
                  # as the rightmost tile of the current row is checked
                  break  # end the inner for loop
      # direction = down --> check the bottommost tile of each column
      else:
         for col in range(n):
            for row in range(n - 1, -1, -1):
               # if the current cell of the tetromino is occupied by a tile
               if self.tile_matrix[row][col] is not None:
                  # the position of the bottommost tile of the current col
                  bottommost = self.get_cell_position(row, col)
                  # if any bottommost tile is at y = 0
                  if bottommost.y == 0:
                     return False  # this tetromino cannot be moved down
                  # if the grid cell below any bottommost tile is occupied
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False  # this tetromino cannot be moved down
                  # as the bottommost tile of the current row is checked
                  break  # end the inner for loop
      # if this method does not end by returning False before this line
      return True  # this tetromino can be moved in the given direction