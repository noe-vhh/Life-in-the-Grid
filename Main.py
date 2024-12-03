import pyglet
import random

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 50
SIDEBAR_WIDTH = 200
FPS = 1  # Frames per second for simulation speed control

# Create the window (subtract sidebar width)
window = pyglet.window.Window(WIDTH, HEIGHT, "Creature Simulation")

# Create the label to display creature stats
stats_label = pyglet.text.Label('', font_name='Arial', font_size=12, x=WIDTH - SIDEBAR_WIDTH + 10, y=HEIGHT - 20,
                                width=SIDEBAR_WIDTH - 20, multiline=True, anchor_x='left', anchor_y='top')

class Creature:
    def __init__(self, x, y, health=100, energy=100):
        self.x = x  # x position on the grid
        self.y = y  # y position on the grid
        self.health = health
        self.energy = energy
        self.hunger = 100  # Hunger is 100 when the creature starts (full stomach)
        self.selected = False  # Whether this creature is selected
        self.color = (0, 255, 0)  # Default color (green)
        self.happiness = self.calculate_happiness()
        self.egg_timer = 0  # Timer for the egg to hatch
        self.egg = None  # No egg initially
        self.has_laid_egg = False  # Flag to check if the creature has laid an egg

    def calculate_happiness(self):
        """Calculate the happiness based on health and hunger."""
        return (self.health + self.hunger) / 2  # Happiness is the average of health and hunger

    def move(self, max_x, max_y):
        """Move the creature randomly within the bounds of the grid."""
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and self.y < max_y - 1:
            self.y += 1
        elif direction == 'down' and self.y > 0:
            self.y -= 1
        elif direction == 'left' and self.x > 0:
            self.x -= 1
        elif direction == 'right' and self.x < max_x - 1:
            self.x += 1

    def update(self):
        """Reduce health, energy, and hunger over time."""
        self.hunger -= 1
        self.energy -= 1
        if self.hunger <= 0:
            self.health -= 1
        if self.health <= 0:
            self.die()

        self.happiness = self.calculate_happiness()

        # Only try to lay an egg if we don't already have one
        if not self.egg and not self.has_laid_egg:
            if self.happiness >= 75 and self.energy >= 50:
                self.lay_egg()

        # Handle egg incubation
        if self.egg:
            self.egg_timer += 1
            if self.egg_timer >= 100:  # Time it takes to hatch the egg
                print(f"Egg hatching at ({self.x}, {self.y})")
                self.egg = False
                self.has_laid_egg = False
                self.egg_timer = 0

    def lay_egg(self):
        """Lays an egg and reduces energy."""
        if self.energy >= 50 and not self.egg and not self.has_laid_egg:
            print(f"Laying egg at ({self.x}, {self.y})")
            self.energy -= 50
            self.egg_timer = 0
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
        # Create only one creature in the environment
        self.width = width
        self.height = height
        self.creatures = [Creature(random.randint(0, width-1), random.randint(0, height-1))]  # Only one creature
        self.eggs = []  # List to track eggs

    def update(self, dt):
        """Update the environment, including moving creatures and handling interactions."""
        new_creatures = []
        for creature in self.creatures:
            if creature.health > 0:
                creature.move(self.width, self.height)
                creature.update()

                # Create new creature when egg hatches
                if creature.egg_timer >= 100 and creature.egg:
                    new_creatures.append(Creature(creature.x, creature.y, health=100, energy=50))
                    
                # Only add egg to the list when it's first laid
                if creature.egg and creature.egg_timer == 0:
                    self.eggs.append(Egg(creature.x, creature.y))

        # Add new creatures that hatched from eggs
        self.creatures.extend(new_creatures)

        # Update and remove hatched eggs
        self.eggs = [egg for egg in self.eggs if egg.timer < 100]
        for egg in self.eggs:
            egg.update()

    def draw(self, screen):
        """Draw all creatures on the screen."""
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
        self.x = x  # x position on the grid
        self.y = y  # y position on the grid
        self.timer = 0  # Timer for egg incubation
        self.selected = False  # Whether the egg is selected

    def update(self):
        """Increment the egg's timer."""
        self.timer += 1

    def __str__(self):
        return f"Egg Timer: {self.timer}"

# Handle mouse clicks
selected_creature = None  # No creature is selected initially
selected_egg = None  # No egg is selected initially

@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected_creature, selected_egg
    if x < WIDTH - SIDEBAR_WIDTH:  # Check if the click is within the grid area (subtract sidebar width)
        grid_x = x // GRID_SIZE
        grid_y = y // GRID_SIZE
        creature_found = False
        egg_found = False

        # Handle creature selection
        for creature in env.creatures:
            if creature.x == grid_x and creature.y == grid_y:
                # Deselect the previous selected egg (if any)
                if selected_egg:
                    selected_egg.selected = False
                
                # Deselect the previous selected creature (if any)
                if selected_creature:
                    selected_creature.selected = False
                
                # Select the new creature
                selected_creature = creature
                selected_creature.selected = True
                creature_found = True
                break

        # Handle egg selection
        if not creature_found:
            for egg in env.eggs:
                if egg.x == grid_x and egg.y == grid_y:
                    # Deselect the previous selected creature (if any)
                    if selected_creature:
                        selected_creature.selected = False
                    
                    # Deselect the previous selected egg (if any)
                    if selected_egg:
                        selected_egg.selected = False
                    
                    # Select the new egg
                    selected_egg = egg
                    selected_egg.selected = True
                    egg_found = True
                    break

        # Deselect everything if no creature or egg is clicked
        if not creature_found and not egg_found:
            if selected_creature:
                selected_creature.selected = False
            if selected_egg:
                selected_egg.selected = False

            selected_creature = None
            selected_egg = None

        update_stats()

    else:
        # Deselect if clicked on the sidebar
        if selected_creature:
            selected_creature.selected = False
        selected_creature = None
        selected_egg = None
        update_stats()

# Update the stats label when a creature or egg is selected
def update_stats():
    if selected_creature:
        stats_label.text = f"Selected Creature:\n{selected_creature}\n(x: {selected_creature.x}, y: {selected_creature.y})"
    elif selected_egg:
        stats_label.text = f"Selected Egg:\n{selected_egg}\n(x: {selected_egg.x}, y: {selected_egg.y})"
    else:
        stats_label.text = "No creature or egg selected"

# Create the environment with only one creature
env = Environment(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

# The game loop
@window.event
def on_draw():
    window.clear()
    env.draw(window)
    stats_label.draw()

# Update method (called on every frame)
def update(dt):
    env.update(dt)  # Update creatures and eggs
    update_stats()  # Update the stats each frame

# Schedule the update method to run at the specified FPS
pyglet.clock.schedule_interval(update, 1.0 / FPS)

# Run the pyglet application
pyglet.app.run()
