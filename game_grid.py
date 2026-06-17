import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing

# A class for modeling the game grid
class GameGrid:
   # A constructor that creates the game grid using the given dimensions
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid to the given values
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles locked on the game grid
      # (this matrix stores Tile objects and None is stored for each empty cell)
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(42, 69, 99)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(0, 100, 200)
      self.boundary_color = Color(0, 100, 200)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.002
      self.box_thickness = 5 * self.line_thickness
      # score starts at 0
      self.score = 0

   # A method for displaying the game grid
   # also draws the side panel to ensure everything is drawn before stddraw.show()
   def display(self, score=0, next_tetromino=None, panel_width=6):
      # clear the entire canvas first (this clears both grid and panel areas)
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None
      # (the case when the game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid
      self.draw_boundaries()
      # draw the side panel in the same frame before stddraw.show() is called
      if next_tetromino is not None:
         self.draw_side_panel(score, next_tetromino, panel_width)
      # show everything at once — grid + panel — no flickering
      stddraw.show(200)

   # A method for drawing the right side panel (score + next piece + controls)
   def draw_side_panel(self, score, next_tetromino, panel_width):
      from point import Point
      panel_color = Color(30, 50, 75)
      text_color = Color(25, 255, 228)
      panel_start_x = self.grid_width - 0.5
      panel_end_x = self.grid_width + panel_width - 0.5
      panel_center_x = (panel_start_x + panel_end_x) / 2
      # draw the panel background
      stddraw.setPenColor(panel_color)
      stddraw.filledRectangle(panel_start_x, -0.5, panel_width, self.grid_height)
      # draw the score label and value
      stddraw.setFontFamily('Arial')
      stddraw.setFontSize(18)
      stddraw.setPenColor(text_color)
      stddraw.boldText(panel_center_x, self.grid_height - 2, 'SCORE')
      stddraw.setFontSize(22)
      stddraw.boldText(panel_center_x, self.grid_height - 3.5, str(score))
      # draw a divider line
      stddraw.setPenColor(text_color)
      stddraw.setPenRadius(0.003)
      stddraw.line(panel_start_x + 0.5, self.grid_height - 5,
                   panel_end_x - 0.5, self.grid_height - 5)
      stddraw.setPenRadius()
      # draw the next piece label
      stddraw.setFontSize(18)
      stddraw.boldText(panel_center_x, self.grid_height - 6, 'NEXT')
      # draw the next tetromino preview tile by tile
      n = len(next_tetromino.tile_matrix)
      preview_start_x = self.grid_width + (panel_width - n) // 2
      preview_start_y = self.grid_height - 7
      for row in range(n):
         for col in range(n):
            if next_tetromino.tile_matrix[row][col] is not None:
               tile_pos = Point()
               tile_pos.x = preview_start_x + col
               tile_pos.y = preview_start_y - row
               next_tetromino.tile_matrix[row][col].draw(tile_pos)
      # draw controls hint at the bottom of the panel
      stddraw.setFontSize(11)
      stddraw.setPenColor(text_color)
      stddraw.text(panel_center_x, 6, '← → Move')
      stddraw.text(panel_center_x, 5, '↓ Soft Drop')
      stddraw.text(panel_center_x, 4, '↑ Rotate')
      stddraw.text(panel_center_x, 3, 'Space: Drop')
      stddraw.text(panel_center_x, 2, 'P: Pause')

   # A method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # if the current grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               # draw this tile
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the game grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius to box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # A method that locks the tiles of a landed tetromino on the grid checking
   # if the game is over due to having any tile above the topmost grid row.
   # (This method returns True when the game is over and False otherwise.)
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the grid
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # after locking, perform merge and then clear full lines
      self.merge_tiles()
      self.clear_full_lines()
      # handle tiles that are not connected to the bottom after merging
      self.handle_free_tiles()
      # return the value of the game_over flag
      return self.game_over

   # A method for merging column-wise touching tiles with the same number.
   # Merging is done from bottom to top (chain merging).
   def merge_tiles(self):
      # keep merging until no more merges are possible (for chain merging)
      merged = True
      while merged:
         merged = False
         # check each column from bottom to top
         for col in range(self.grid_width):
            for row in range(self.grid_height - 1):
               # check if two vertically adjacent tiles have the same number
               bottom = self.tile_matrix[row][col]
               top = self.tile_matrix[row + 1][col]
               if bottom is not None and top is not None:
                  if bottom.number == top.number:
                     # merge: double the bottom tile's number
                     new_number = bottom.number * 2
                     bottom.set_number(new_number)
                     # add the merged value to the score
                     self.score += new_number
                     # shift all tiles above the merged tile down by one
                     # so no gaps are left in the column (required for chain merging)
                     for r in range(row + 1, self.grid_height - 1):
                        self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
                     # clear the topmost cell of this column after shifting
                     self.tile_matrix[self.grid_height - 1][col] = None
                     # a merge happened, so we need another pass
                     merged = True

   # A method for clearing full horizontal lines and updating the score.
   def clear_full_lines(self):
      row = 0
      while row < self.grid_height:
         # check if the current row is completely full
         if all(self.tile_matrix[row][col] is not None for col in range(self.grid_width)):
            # add the sum of all numbers in this row to the score
            for col in range(self.grid_width):
               self.score += self.tile_matrix[row][col].number
            # remove this row by shifting all rows above it down by one
            for r in range(row, self.grid_height - 1):
               for col in range(self.grid_width):
                  self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
            # clear the topmost row after shifting
            for col in range(self.grid_width):
               self.tile_matrix[self.grid_height - 1][col] = None
            # do not increment row since the same index now has a new row
         else:
            row += 1

   # A method for handling free (unconnected) tiles after merging.
   # A tile is free if it is not 4-connected to the bottom of the grid.
   # Free tiles are deleted and their numbers are added to the score.
   def handle_free_tiles(self):
      # find all tiles that are connected to the bottom using flood fill
      connected = np.full((self.grid_height, self.grid_width), False)
      # start from each tile in the bottom row
      for col in range(self.grid_width):
         if self.tile_matrix[0][col] is not None:
            self.flood_fill(0, col, connected)
      # delete any tile that is not connected to the bottom
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None and not connected[row][col]:
               # add the free tile's number to the score before deleting
               self.score += self.tile_matrix[row][col].number
               self.tile_matrix[row][col] = None

   # A helper method for flood fill (used in handle_free_tiles).
   # Marks all tiles that are 4-connected to the given cell as connected.
   def flood_fill(self, row, col, connected):
      # stop if out of bounds, already visited, or cell is empty
      if not self.is_inside(row, col):
         return
      if connected[row][col]:
         return
      if self.tile_matrix[row][col] is None:
         return
      # mark this cell as connected
      connected[row][col] = True
      # visit all 4 neighbors (up, down, left, right)
      self.flood_fill(row + 1, col, connected)
      self.flood_fill(row - 1, col, connected)
      self.flood_fill(row, col + 1, connected)
      self.flood_fill(row, col - 1, connected)

   # A method to check if any tile on the grid has reached 2048 (win condition)
   def has_won(self):
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               if self.tile_matrix[row][col].number >= 2048:
                  return True
      return False