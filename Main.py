import pyglet
import random

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 50
SIDEBAR_WIDTH = 200
FPS = 1  # Initial FPS
MIN_FPS = 1
MAX_FPS = 60

# Create a simple rectangle class for panel sections
class Panel:
    def __init__(self, x, y, width, height, title=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        
    def draw(self):
        # Draw panel background
        pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, 
                              color=(40, 40, 40)).draw()
        # Draw panel border
        pyglet.shapes.BorderedRectangle(self.x, self.y, self.width, self.height,
                                      border=2, color=(40, 40, 40), 
                                      border_color=(100, 100, 100)).draw()
        # Draw title if exists
        if self.title:
            pyglet.text.Label(self.title,
                            font_name='Arial',
                            font_size=12,
                            bold=True,
                            x=self.x + 10,
                            y=self.y + self.height - 20,
                            anchor_x='left',
                            anchor_y='center').draw()

# Create a simple slider class
class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.dragging = False
        
        # Calculate initial handle position
        self.handle_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
        self.handle_radius = 8
        
    def draw(self):
        # Draw slider track
        pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, 
                              color=(100, 100, 100)).draw()
        # Draw handle
        pyglet.shapes.Circle(self.handle_x, self.y + self.height/2, 
                           self.handle_radius, color=(200, 200, 200)).draw()
        
    def hit_test(self, x, y):
        return (self.x <= x <= self.x + self.width and 
                self.y - self.handle_radius <= y <= self.y + self.height + self.handle_radius)
    
    def update_value(self, x):
        self.handle_x = min(max(x, self.x), self.x + self.width)
        normalized_value = (self.handle_x - self.x) / self.width
        self.value = round(self.min_value + normalized_value * (self.max_value - self.min_value))
        return self.value

# Create the window
window = pyglet.window.Window(WIDTH, HEIGHT, "Creature Simulation")

# Create panels
control_panel = Panel(WIDTH - SIDEBAR_WIDTH, HEIGHT - 120, SIDEBAR_WIDTH, 120, "Controls")
stats_panel = Panel(WIDTH - SIDEBAR_WIDTH, HEIGHT - 320, SIDEBAR_WIDTH, 190, "Statistics")

# Create the label to display creature stats with better formatting
stats_label = pyglet.text.Label('', 
                               font_name='Arial',
                               font_size=12,
                               x=WIDTH - SIDEBAR_WIDTH + 10,
                               y=HEIGHT - 170,  # Adjusted position
                               width=SIDEBAR_WIDTH - 20,
                               multiline=True,
                               anchor_x='left',
                               anchor_y='top')

# Create FPS slider and label
fps_label = pyglet.text.Label('Simulation Speed (FPS):',
                             font_name='Arial',
                             font_size=12,
                             x=WIDTH - SIDEBAR_WIDTH + 10,
                             y=HEIGHT - 60,
                             anchor_x='left',
                             anchor_y='top')

fps_slider = Slider(WIDTH - SIDEBAR_WIDTH + 10, HEIGHT - 90,
                   SIDEBAR_WIDTH - 20, MIN_FPS, MAX_FPS, FPS)

# Variable to track if FPS input is active
fps_input_active = False

class Creature:
    def __init__(self, x, y, health=100, energy=100):
        self.x = x  # x position on the grid
        self.y = y  # y position on the grid
        self.health = health
        self.energy = energy
        self.hunger = 100  # Hunger is 100 when the creature starts (full stomach)
        self.selected = False  # Whether this creature is selected
        self.sleeping = False  # Add new sleeping state
        self.color = (0, 255, 0)  # Default color (green)
        self.happiness = self.calculate_happiness()
        self.egg_timer = 0  # Timer for the egg to hatch
        self.egg = None  # No egg initially
        self.has_laid_egg = False  # Flag to check if the creature has laid an egg

    def calculate_happiness(self):
        """Calculate the happiness based on health and hunger."""
        return (self.health + self.hunger) / 2  # Happiness is the average of health and hunger

    def move(self, max_x, max_y):
        """Move the creature randomly within the bounds of the grid, excluding the sidebar."""
        if not self.sleeping:  # Only move if not sleeping
            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and self.y < max_y - 1:
                self.y += 1
            elif direction == 'down' and self.y > 0:
                self.y -= 1
            elif direction == 'left' and self.x > 0:
                self.x -= 1
            elif direction == 'right' and self.x < (max_x - SIDEBAR_WIDTH // GRID_SIZE) - 1:
                self.x += 1

    def update(self):
        """Reduce health, energy, and hunger over time."""
        # Check if creature needs to sleep
        if self.energy <= 20 and not self.sleeping:
            self.sleeping = True
            self.color = (100, 100, 255)  # Blue color when sleeping
        elif self.sleeping and self.energy >= 90:
            self.sleeping = False
            self.color = (0, 255, 0)  # Back to green when awake

        # Only reduce energy and move if not sleeping
        if not self.sleeping:
            self.hunger = max(0, self.hunger - 1)
            self.energy = max(0, self.energy - 1)
        else:
            self.energy = min(100, self.energy + 2)  # Recover energy while sleeping
        
        if self.hunger <= 0:
            self.health -= 1
        if self.health <= 0:
            self.die()

        self.happiness = self.calculate_happiness()

        # Only try to lay an egg if conditions are met
        if not self.egg and not self.has_laid_egg:
            if self.happiness >= 75 and self.energy >= 50:
                self.lay_egg()

    def lay_egg(self):
        """Prepare to lay an egg."""
        if self.energy >= 50 and not self.egg and not self.has_laid_egg:
            self.energy -= 50
            self.egg = True
            self.has_laid_egg = True

    def die(self):
        """Remove the creature from the simulation."""
        self.x = self.y = -1  # Mark as dead

    def __str__(self):
        return f"Health: {self.health}, Energy: {self.energy}, Hunger: {self.hunger}, Happiness: {self.happiness}, Laid Egg: {self.has_laid_egg}"

# The environment where creatures live
class Environment:
    def __init__(self, width, height):
        # Adjust width to account for sidebar
        self.width = width - (SIDEBAR_WIDTH // GRID_SIZE)
        self.height = height
        # Ensure creature spawns within the valid grid area
        self.creatures = [Creature(random.randint(0, self.width-1), 
                                 random.randint(0, self.height-1))]
        self.eggs = []  # List to track eggs
        self.grid = {}  # Add a grid to track occupied positions
        # Add initial creature to the grid
        for creature in self.creatures:
            self.grid[(creature.x, creature.y)] = creature

    def is_position_occupied(self, x, y):
        """Check if a position is occupied by any entity"""
        return (x, y) in self.grid

    def get_adjacent_positions(self, x, y):
        """Get all valid adjacent positions."""
        positions = [
            (x, y+1),    # up
            (x, y-1),    # down
            (x-1, y),    # left
            (x+1, y),    # right
        ]
        # Filter out positions that are out of bounds or in the sidebar
        return [(x, y) for x, y in positions if 
                0 <= x < self.width and 
                0 <= y < self.height]

    def find_open_adjacent_spot(self, x, y):
        """Find an unoccupied adjacent position."""
        adjacent_positions = self.get_adjacent_positions(x, y)
        for pos_x, pos_y in adjacent_positions:
            if not self.is_position_occupied(pos_x, pos_y):
                return pos_x, pos_y
        return None

    def update(self, dt):
        """Update the environment, including moving creatures and handling interactions."""
        new_creatures = []
        eggs_to_remove = []
        
        # Update grid positions for creatures and eggs
        self.grid.clear()
        for creature in self.creatures:
            if creature.health > 0:
                self.grid[(creature.x, creature.y)] = creature
        for egg in self.eggs:
            self.grid[(egg.x, egg.y)] = egg

        # First, check for any eggs that are ready to hatch
        for egg in self.eggs:
            egg.update()
            if egg.ready_to_hatch:
                eggs_to_remove.append(egg)
                # Remove egg from grid before adding new creature
                self.grid.pop((egg.x, egg.y), None)
                new_creatures.append(Creature(egg.x, egg.y, health=100, energy=50))
        
        # Remove hatched eggs and add new creatures
        self.eggs = [egg for egg in self.eggs if egg not in eggs_to_remove]
        self.creatures.extend(new_creatures)
        
        # Then update creatures and handle new egg laying
        for creature in self.creatures:
            if creature.health > 0:
                old_x, old_y = creature.x, creature.y
                creature.move(self.width, self.height)
                
                # Check if new position is occupied
                if self.is_position_occupied(creature.x, creature.y) and (creature.x, creature.y) != (old_x, old_y):
                    # If occupied, revert to old position
                    creature.x, creature.y = old_x, old_y
                else:
                    # Update grid with new position
                    self.grid.pop((old_x, old_y), None)
                    self.grid[(creature.x, creature.y)] = creature

                creature.update()

                # Check for new eggs
                if creature.egg:
                    egg_pos = self.find_open_adjacent_spot(creature.x, creature.y)
                    if egg_pos:
                        new_egg = Egg(egg_pos[0], egg_pos[1])
                        self.eggs.append(new_egg)
                        self.grid[egg_pos] = new_egg
                        creature.egg = False
                    else:
                        # If no open spots, cancel egg laying but keep has_laid_egg true
                        creature.egg = False

    def draw(self, screen):
        """Draw all creatures and eggs on the screen."""
        for creature in self.creatures:
            if creature.health > 0:
                # Only draw the white border if the creature is selected
                if creature.selected:
                    pyglet.shapes.Circle(creature.x * GRID_SIZE + GRID_SIZE // 2, creature.y * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE // 2 + 2, color=(255, 255, 255), batch=None).draw()

                # Draw the creature itself (green circle)
                pyglet.shapes.Circle(creature.x * GRID_SIZE + GRID_SIZE // 2, creature.y * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE // 2, color=creature.color, batch=None).draw()

        # Draw the eggs (as small yellow circles)
        for egg in self.eggs:
            # Only draw the white border if the egg is selected
            if egg.selected:
                pyglet.shapes.Circle(egg.x * GRID_SIZE + GRID_SIZE // 2, egg.y * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE // 4 + 2, color=(255, 255, 255), batch=None).draw()

            pyglet.shapes.Circle(egg.x * GRID_SIZE + GRID_SIZE // 2, egg.y * GRID_SIZE + GRID_SIZE // 2, GRID_SIZE // 4, color=(255, 255, 0), batch=None).draw()

# The egg class to handle egg incubation
class Egg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.selected = False
        self.ready_to_hatch = False  # New flag to indicate hatching

    def update(self):
        """Increment the egg's timer and check if ready to hatch."""
        if self.timer < 100:
            self.timer += 1
        if self.timer >= 100:
            self.ready_to_hatch = True

    def __str__(self):
        return f"Egg Timer: {min(self.timer, 100)}"

# Handle mouse clicks
selected_creature = None  # No creature is selected initially
selected_egg = None  # No egg is selected initially

@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected_creature, selected_egg
    if x < WIDTH - SIDEBAR_WIDTH:  # Check if the click is within the grid area
        grid_x = x // GRID_SIZE
        grid_y = y // GRID_SIZE
        creature_found = False
        egg_found = False

        # First check if we clicked on a creature
        for creature in env.creatures:
            if creature.x == grid_x and creature.y == grid_y:
                creature_found = True
                # Only select if it's not already selected
                if selected_creature != creature:
                    # Deselect previous selections
                    if selected_creature:
                        selected_creature.selected = False
                    if selected_egg:
                        selected_egg.selected = False
                        selected_egg = None
                    # Select new creature
                    selected_creature = creature
                    selected_creature.selected = True
                break

        # Then check if we clicked on an egg
        if not creature_found:  # Only check eggs if we didn't click a creature
            for egg in env.eggs:
                if egg.x == grid_x and egg.y == grid_y:
                    egg_found = True
                    # Only select if it's not already selected
                    if selected_egg != egg:
                        # Deselect previous selections
                        if selected_creature:
                            selected_creature.selected = False
                            selected_creature = None
                        if selected_egg:
                            selected_egg.selected = False
                        # Select new egg
                        selected_egg = egg
                        selected_egg.selected = True
                    break

        # Deselect everything if clicking empty space
        if not creature_found and not egg_found:
            if selected_creature:
                selected_creature.selected = False
                selected_creature = None
            if selected_egg:
                selected_egg.selected = False
                selected_egg = None

        update_stats()

    else:
        # Check if clicking on slider
        if fps_slider.hit_test(x, y):
            fps_slider.dragging = True
            new_fps = fps_slider.update_value(x)
            update_fps(new_fps)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if fps_slider.dragging:
        new_fps = fps_slider.update_value(x)
        update_fps(new_fps)

@window.event
def on_mouse_release(x, y, button, modifiers):
    fps_slider.dragging = False

def update_fps(new_fps):
    """Update the FPS and reschedule the update function"""
    global FPS
    FPS = new_fps
    fps_label.text = f'FPS: {FPS}'
    pyglet.clock.unschedule(update)
    pyglet.clock.schedule_interval(update, 1.0 / FPS)

def format_stats(creature):
    """Format creature stats in a more readable way"""
    if not creature:
        return "No creature selected"
    
    return f"""Health: {creature.health}%
Energy: {creature.energy}%
Hunger: {creature.hunger}%
Happiness: {round(creature.happiness)}%
Position: ({creature.x}, {creature.y})
Has Egg: {'Yes' if creature.egg else 'No'}"""

def update_stats():
    """Update the stats with formatted text"""
    if selected_creature:
        stats_label.text = format_stats(selected_creature)
    elif selected_egg:
        stats_label.text = f"Selected Egg:\nIncubation: {selected_egg.timer}%\nPosition: ({selected_egg.x}, {selected_egg.y})"
    else:
        stats_label.text = "No creature or egg selected"

# Create the environment with only one creature
env = Environment(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

# The game loop
@window.event
def on_draw():
    window.clear()
    
    # Draw sidebar background
    pyglet.shapes.Rectangle(WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT,
                          color=(30, 30, 30)).draw()
    
    # Draw panels
    control_panel.draw()
    stats_panel.draw()
    
    # Draw content
    env.draw(window)
    stats_label.draw()
    fps_label.draw()
    fps_slider.draw()

# Update method (called on every frame)
def update(dt):
    env.update(dt)  # Update creatures and eggs
    update_stats()  # Update the stats each frame

# Run the pyglet application
pyglet.app.run()
