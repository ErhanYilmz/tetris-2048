import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random  # used for randomly assigning 2 or 4 to each tile

# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = 'Arial', 16

   # Color map: each power of 2 gets its own background color (as in 2048)
   BACKGROUND_COLORS = {
      2:    Color(151, 178, 199),
      4:    Color(119, 158, 187),
      8:    Color(242, 177, 121),
      16:   Color(245, 149, 99),
      32:   Color(246, 124, 95),
      64:   Color(246, 94,  59),
      128:  Color(237, 207, 114),
      256:  Color(237, 204, 97),
      512:  Color(237, 200, 80),
      1024: Color(237, 197, 63),
      2048: Color(237, 194, 46),
   }

   # Foreground (text) color changes based on tile value
   FOREGROUND_COLORS = {
      2:    Color(0, 100, 200),
      4:    Color(0, 100, 200),
      8:    Color(255, 255, 255),
      16:   Color(255, 255, 255),
      32:   Color(255, 255, 255),
      64:   Color(255, 255, 255),
      128:  Color(255, 255, 255),
      256:  Color(255, 255, 255),
      512:  Color(255, 255, 255),
      1024: Color(255, 255, 255),
      2048: Color(255, 255, 255),
   }

   # A constructor that creates a tile with a randomly assigned number (2 or 4)
   def __init__(self, number=None):
      # if no number is given, randomly assign 2 or 4 as in 2048
      if number is None:
         self.number = random.choice([2, 4])
      else:
         self.number = number
      # set the colors based on the tile number (use self.number, not the parameter)
      self.background_color = self.get_background_color(self.number)
      self.foreground_color = self.get_foreground_color(self.number)
      self.box_color = Color(0, 100, 200)  # box (boundary) color stays the same

   # Returns the background color for a given number
   def get_background_color(self, number):
      # if the number is in the color map, return the corresponding color
      if number in self.BACKGROUND_COLORS:
         return self.BACKGROUND_COLORS[number]
      # for very large numbers (beyond 2048), use a default dark color
      return Color(60, 58, 50)

   # Returns the foreground color for a given number
   def get_foreground_color(self, number):
      if number in self.FOREGROUND_COLORS:
         return self.FOREGROUND_COLORS[number]
      return Color(255, 255, 255)  # white text for large numbers

   # Updates the tile's number and refreshes its colors accordingly
   def set_number(self, number):
      self.number = number
      self.background_color = self.get_background_color(number)
      self.foreground_color = self.get_foreground_color(number)

   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(position.x, position.y, str(self.number))