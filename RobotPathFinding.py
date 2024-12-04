import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 700, 600
grid_size = 20
sidebar_width = 300
window = pygame.display.set_mode((width + sidebar_width, height))
pygame.display.set_caption('Robot Simulation')

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

class Robot:
    def __init__(self, x=0, y=0, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.path = []
        self.detected_fires = []  # List to log detected fire coordinates
        self.direction = 1  # 1 for down, -1 for up

    def move_to_next_cell(self):
        if self.path:
            next_point = self.path[0]
            dx, dy = next_point[0] - self.x, next_point[1] - self.y
            distance = math.hypot(dx, dy)

            if distance < self.speed:
                # Snap to the target if close
                self.x, self.y = next_point
                self.path.pop(0)  # Remove the reached point
            else:
                # Move toward the next point
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)

    def create_zigzag_path(self):
        """Create a path that covers the entire map in a zigzag pattern."""
        self.path = []
        for col in range(0, width + grid_size, grid_size):
            if self.direction == 1:  # Moving down
                for row in range(0, height + grid_size, grid_size):
                    self.path.append((col, row))
            else:  # Moving up
                for row in range(height, -grid_size, -grid_size):
                    self.path.append((col, row))
            self.direction *= -1  # Change direction at each column

    def log_fire(self, fire):
        if fire not in self.detected_fires:
            self.detected_fires.append(fire)
            print(f"Detected fire at: {fire}")

    def get_position(self):
        return (self.x, self.y)

def draw_grid(surface, grid_size):
    """Draw a grid on the screen."""
    for x in range(0, width, grid_size):
        pygame.draw.line(surface, GRAY, (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(surface, GRAY, (0, y), (width, y))

def draw_path(surface, path):
    """Draw the calculated zigzag path."""
    if len(path) > 1:
        pygame.draw.lines(surface, YELLOW, False, path, 2)

def draw_table(surface, fires, position, font_size=20):
    """Draw the table of logged fire coordinates."""
    font = pygame.font.Font(None, font_size)
    header_text = font.render("Logged Fires:", True, BLACK)
    surface.blit(header_text, position)
    for i, fire in enumerate(fires):
        fire_text = font.render(f"{i + 1}: {fire}", True, BLACK)
        surface.blit(fire_text, (position[0], position[1] + (i + 1) * font_size))

def draw_slider(surface, slider_rect, speed, max_speed):
    """Draw the speed control slider."""
    pygame.draw.rect(surface, GRAY, slider_rect)
    pygame.draw.rect(
        surface, BLUE,
        (slider_rect[0], slider_rect[1], int(slider_rect[2] * (speed / max_speed)), slider_rect[3])
    )
    font = pygame.font.Font(None, 30)
    speed_text = font.render(f"Speed: {speed:.1f}", True, BLACK)
    surface.blit(speed_text, (slider_rect[0], slider_rect[1] - 30))

# Simulation parameters
robot = Robot(x=0, y=0, speed=2)
robot.create_zigzag_path()
fires = [(100,50),(200, 200), (400, 300), (600, 450)]
running = True
clock = pygame.time.Clock()

# Slider parameters
slider_rect = pygame.Rect(width + 20, 100, 200, 20)
max_speed = 10
min_speed = 1

# Simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if slider_rect.collidepoint(event.pos):
                mouse_x = event.pos[0]
                slider_value = (mouse_x - slider_rect.x) / slider_rect.width
                robot.speed = max(min_speed, min(max_speed, slider_value * max_speed))

    # Move the robot along the zigzag path
    robot.move_to_next_cell()

    # Check if robot is close to a fire and log it
    for fire in fires:
        if math.hypot(fire[0] - robot.x, fire[1] - robot.y) < grid_size / 2:
            robot.log_fire(fire)

    # Stop when the path is complete
    if not robot.path:
        print("Finished scanning the map.")
        running = False

    # Clear the screen
    window.fill(WHITE)

    # Draw the grid
    draw_grid(window, grid_size)

    # Draw the fires
    for fire in fires:
        pygame.draw.circle(window, RED, fire, 10)

    # Draw the robot
    pygame.draw.circle(window, BLUE, (int(robot.x), int(robot.y)), 10)

    # Draw the robot's path
    draw_path(window, robot.path)

    # Draw the speed slider
    draw_slider(window, slider_rect, robot.speed, max_speed)

    # Draw the table of logged fires
    draw_table(window, robot.detected_fires, (width + 20, 200))

    # Display the robot's coordinates
    coords = robot.get_position()
    draw_text = lambda text, pos: window.blit(pygame.font.Font(None, 30).render(text, True, BLACK), pos)
    draw_text(f'Coordinates: ({coords[0]:.2f}, {coords[1]:.2f})', (width + 20, 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
