################################################################################
#                                                                              #
# The main program of Tetris 2048                                              #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)

# The main function of this program
def main():
   # set the dimensions of the game grid
   grid_height, grid_width = 20, 12
   # set the size of the drawing canvas (the displayed window)
   cell_size = 40
   # the right panel is 6 cells wide (used for score and next piece display)
   panel_width = 6
   canvas_height = cell_size * grid_height
   canvas_width = cell_size * (grid_width + panel_width)
   stddraw.setCanvasSize(canvas_width, canvas_height)
   # set the x-scale and the y-scale of the drawing canvas
   # the grid goes from -0.5 to grid_width - 0.5
   # the panel goes from grid_width - 0.5 to grid_width + panel_width - 0.5
   stddraw.setXscale(-0.5, grid_width + panel_width - 0.5)
   stddraw.setYscale(-0.5, grid_height - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_height
   Tetromino.grid_width = grid_width
   # create the game grid
   grid = GameGrid(grid_height, grid_width)
   # create the first tetromino to enter the game grid
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino
   # create the next tetromino (shown in the panel)
   next_tetromino = create_tetromino()

   # display the game menu before starting
   display_game_menu(grid_height, grid_width, panel_width)

   # clear the canvas once before the game loop starts
   # this sets a clean black background for the entire canvas
   stddraw.clear(Color(0, 0, 0))

   # paused flag to track whether the game is paused
   paused = False

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped()
         # left arrow key: move tetromino left
         if key_typed == 'left':
            current_tetromino.move(key_typed, grid)
         # right arrow key: move tetromino right
         elif key_typed == 'right':
            current_tetromino.move(key_typed, grid)
         # down arrow key: soft drop (move down faster)
         elif key_typed == 'down':
            current_tetromino.move(key_typed, grid)
         # up arrow key: rotate the tetromino clockwise
         elif key_typed == 'up':
            current_tetromino.rotate(grid)
         # space key: hard drop (instantly drop to the bottom)
         elif key_typed == 'space':
            current_tetromino.hard_drop(grid)
         # p key: pause or resume the game
         elif key_typed == 'p':
            paused = not paused
         stddraw.clearKeysTyped()

      # if the game is paused, skip the update and just show the pause screen
      if paused:
         display_pause_screen(grid_height, grid_width, panel_width)
         stddraw.show(100)
         continue

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move('down', grid)
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            break
         # check if the player has won (a tile reached 2048)
         if grid.has_won():
            display_win_screen(grid_height, grid_width, panel_width, grid.score)
            return  # exit the main function (ends the program)
         # the next tetromino becomes the current one
         current_tetromino = next_tetromino
         grid.current_tetromino = current_tetromino
         # create a new next tetromino
         next_tetromino = create_tetromino()

      # display the game grid, side panel and show everything in one call
      grid.display(grid.score, next_tetromino, panel_width)

   # show the game over screen when the loop ends
   display_game_over_screen(grid_height, grid_width, panel_width, grid.score)

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # all 7 tetromino types are now included
   tetromino_types = ['I', 'O', 'Z', 'S', 'T', 'J', 'L']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying the right side panel (score + next piece)
def display_side_panel(grid_height, grid_width, panel_width, score, next_tetromino):
   # colors used in the panel
   panel_color = Color(30, 50, 75)
   text_color = Color(25, 255, 228)
   # the panel starts right after the game grid
   panel_start_x = grid_width - 0.5
   panel_end_x = grid_width + panel_width - 0.5
   panel_center_x = (panel_start_x + panel_end_x) / 2

   # draw the panel background
   stddraw.setPenColor(panel_color)
   stddraw.filledRectangle(panel_start_x, -0.5, panel_width, grid_height)

   # draw the score section
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(18)
   stddraw.setPenColor(text_color)
   stddraw.boldText(panel_center_x, grid_height - 2, 'SCORE')
   stddraw.setFontSize(22)
   stddraw.boldText(panel_center_x, grid_height - 3.5, str(score))

   # draw a divider line between score and next piece sections
   stddraw.setPenColor(text_color)
   stddraw.setPenRadius(0.003)
   stddraw.line(panel_start_x + 0.5, grid_height - 5, panel_end_x - 0.5, grid_height - 5)
   stddraw.setPenRadius()

   # draw the next piece label
   stddraw.setFontSize(18)
   stddraw.boldText(panel_center_x, grid_height - 6, 'NEXT')

   # draw the next tetromino preview centered in the panel
   # draw each tile manually instead of using tetromino.draw()
   # because tetromino.draw() clips tiles outside the grid height
   n = len(next_tetromino.tile_matrix)
   # calculate the top-left starting position for the preview
   preview_start_x = grid_width + (panel_width - n) // 2
   preview_start_y = grid_height - 7  # vertical position in the panel
   from point import Point
   for row in range(n):
      for col in range(n):
         if next_tetromino.tile_matrix[row][col] is not None:
            # compute the screen position of this tile in the panel
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

# A function for displaying the pause screen overlay
def display_pause_screen(grid_height, grid_width, panel_width):
   overlay_color = Color(20, 20, 20)
   text_color = Color(25, 255, 228)
   center_x = (grid_width - 1) / 2
   center_y = grid_height / 2
   # draw a semi-transparent dark rectangle over the grid
   stddraw.setPenColor(overlay_color)
   stddraw.filledRectangle(-0.5, center_y - 2, grid_width, 4)
   # draw the pause text
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(30)
   stddraw.setPenColor(text_color)
   stddraw.boldText(center_x, center_y + 0.5, 'PAUSED')
   stddraw.setFontSize(16)
   stddraw.text(center_x, center_y - 0.8, 'Press P to Resume')

# A function for displaying the game over screen
def display_game_over_screen(grid_height, grid_width, panel_width, score):
   background_color = Color(42, 69, 99)
   text_color = Color(25, 255, 228)
   button_color = Color(25, 255, 228)
   button_text_color = Color(42, 69, 99)
   center_x = (grid_width - 1) / 2
   stddraw.clear(background_color)
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(40)
   stddraw.setPenColor(text_color)
   stddraw.boldText(center_x, grid_height - 5, 'GAME OVER')
   stddraw.setFontSize(22)
   stddraw.text(center_x, grid_height - 8, 'Your Score:')
   stddraw.setFontSize(30)
   stddraw.boldText(center_x, grid_height - 10, str(score))
   # draw a restart button
   button_w, button_h = grid_width - 2, 2
   button_x = center_x - button_w / 2
   button_y = grid_height - 15
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_x, button_y, button_w, button_h)
   stddraw.setFontSize(20)
   stddraw.setPenColor(button_text_color)
   stddraw.boldText(center_x, button_y + 1, 'Play Again')
   stddraw.show(100)
   # wait for the player to click the play again button
   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mx, my = stddraw.mouseX(), stddraw.mouseY()
         if button_x <= mx <= button_x + button_w:
            if button_y <= my <= button_y + button_h:
               main()  # restart the game
               return

# A function for displaying the win screen
def display_win_screen(grid_height, grid_width, panel_width, score):
   background_color = Color(42, 69, 99)
   text_color = Color(237, 194, 46)
   button_color = Color(237, 194, 46)
   button_text_color = Color(42, 69, 99)
   center_x = (grid_width - 1) / 2
   stddraw.clear(background_color)
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(40)
   stddraw.setPenColor(text_color)
   stddraw.boldText(center_x, grid_height - 5, 'YOU WIN!')
   stddraw.setFontSize(20)
   stddraw.setPenColor(Color(25, 255, 228))
   stddraw.text(center_x, grid_height - 7.5, 'You reached 2048!')
   stddraw.setFontSize(22)
   stddraw.text(center_x, grid_height - 9.5, 'Your Score:')
   stddraw.setFontSize(30)
   stddraw.setPenColor(text_color)
   stddraw.boldText(center_x, grid_height - 11.5, str(score))
   # draw a play again button
   button_w, button_h = grid_width - 2, 2
   button_x = center_x - button_w / 2
   button_y = grid_height - 16
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_x, button_y, button_w, button_h)
   stddraw.setFontSize(20)
   stddraw.setPenColor(button_text_color)
   stddraw.boldText(center_x, button_y + 1, 'Play Again')
   stddraw.show(100)
   # wait for the player to click the play again button
   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mx, my = stddraw.mouseX(), stddraw.mouseY()
         if button_x <= mx <= button_x + button_w:
            if button_y <= my <= button_y + button_h:
               main()  # restart the game
               return

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width, panel_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is located
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # build the path of the image file
   img_file = os.path.join(current_dir, 'images/menu_image.png')
   # the coordinates to display the image centered horizontally
   # use the total canvas width (grid + panel) to find the true center
   img_center_x, img_center_y = (grid_width + panel_width - 1) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = 'Click Here to Start the Game'
   stddraw.text(img_center_x, 5, text_to_display)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game

# Call the main() function to start the program.
main()