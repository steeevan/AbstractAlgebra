import turtle
import math
# Initialize the screen
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Hexagonal Tessellation")
screen.setup(width=800, height=800)

# Create the turtle
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Function to draw a hexagon
def draw_hexagon(x, y, size, color):
    """Draw a single hexagon centered at (x, y)."""
    pen.penup()
    pen.goto(x, y)
    pen.setheading(30)  # Align the hexagon properly
    pen.color(color)
    pen.pendown()
    pen.begin_fill()
    for _ in range(6):
        pen.forward(size)
        pen.left(60)
    pen.end_fill()

# Create a hexagonal tiling
def hexagonal_tiling(rows, cols, size):
    """Create a hexagonal tiling pattern."""
    colors = ["blue", "green", "red", "purple", "orange", "yellow"]
    h = size * math.sqrt(3)  # Height of a single hexagon
    for row in range(rows):
        for col in range(cols):
            # Calculate x and y offsets
            x_offset = col * 1.5 * size
            y_offset = row * h
            if col % 2 == 1:
                y_offset += h / 2  # Offset every other column
            
            # Choose a color for variety
            color = colors[(row + col) % len(colors)]
            
            # Draw the hexagon
            draw_hexagon(x_offset - cols * size / 2, y_offset - rows * h / 2, size, color)

# Parameters
rows = 10  # Number of rows of hexagons
cols = 10  # Number of columns of hexagons
hex_size = 30  # Size of each hexagon

# Draw the hexagonal tiling
hexagonal_tiling(rows, cols, hex_size)

# Finish
screen.mainloop()
