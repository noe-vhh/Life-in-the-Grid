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
    __slots__ = ('x', 'y', 'health', 'energy', 'hunger', 'selected', 
                 'sleeping', 'color', 'happiness', 'egg_timer', 'egg',
                 'has_laid_egg', 'dead', 'eating', 'food_value',
                 'rest_threshold', 'wake_threshold', 'age', 'mature',
                 'env', 'max_age')
    
    def __init__(self, x, y, environment, health=100, energy=100):
        self.x = x
        self.y = y
        self.env = environment
        self.health = health
        self.energy = energy
        self.hunger = 100
        self.selected = False
        self.sleeping = False
        self.color = (0, 255, 0)
        self.happiness = self.calculate_happiness()
        self.egg_timer = 0
        self.egg = None
        self.has_laid_egg = False
        self.dead = False
        self.eating = False
        self.food_value = 100
        self.rest_threshold = random.randint(15, 25)
        self.wake_threshold = random.randint(85, 95)
        self.age = 0
        self.max_age = random.randint(300, 500)  # Creatures live between 300-500 ticks
        self.mature = False

    def calculate_happiness(self):
        """Calculate the happiness based on health and hunger."""
        return (self.health + self.hunger) / 2  # Happiness is the average of health and hunger

    def move(self, max_x, max_y):
        if self.sleeping or self.dead:
            return

        # Cache nearby entities using spatial partitioning
        nearby_entities = self.env.get_nearby_entities(self.x, self.y)
        
        # Movement vector based on various factors
        move_vector = [0, 0]
        
        # Avoid crowding
        for entity in nearby_entities:
            if isinstance(entity, Creature) and not entity.dead:
                dx = self.x - entity.x
                dy = self.y - entity.y
                dist = max(1, abs(dx) + abs(dy))
                move_vector[0] += dx / (dist * dist)
                move_vector[1] += dy / (dist * dist)
        
        # Add food seeking behavior if hungry
        if self.hunger < 50:
            food_pos = self.env.find_nearest_food(self.x, self.y)
            if food_pos:
                dx = food_pos[0] - self.x
                dy = food_pos[1] - self.y
                dist = max(1, abs(dx) + abs(dy))
                move_vector[0] += dx * 2 / dist  # Stronger attraction to food
                move_vector[1] += dy * 2 / dist

        # Add random movement if no other factors
        if move_vector[0] == 0 and move_vector[1] == 0:
            move_vector = [random.uniform(-1, 1), random.uniform(-1, 1)]

        # In Creature class, update the move method - modify the food stockpile behavior
        # Replace the previous well-fed behavior with this:
        if self.hunger >= 90 and nearby_entities:  # If well fed, help organize food storage
            dead_creatures = [e for e in nearby_entities 
                             if isinstance(e, Creature) and e.dead and e.food_value > 0]
            if dead_creatures:
                # Find the center of the largest nearby food cluster
                cluster_x = sum(d.x for d in dead_creatures) / len(dead_creatures)
                cluster_y = sum(d.y for d in dead_creatures) / len(dead_creatures)
                
                # If we're next to a dead creature, try to move it towards the cluster
                for dead in dead_creatures:
                    if abs(dead.x - self.x) <= 1 and abs(dead.y - self.y) <= 1:
                        dx = cluster_x - dead.x
                        dy = cluster_y - dead.y
                        dist = max(1, (dx*dx + dy*dy)**0.5)
                        move_vector[0] += dx / dist * 3  # Strong attraction to cluster
                        move_vector[1] += dy / dist * 3
                        break  # Only try to move one body at a time

        # Normalize and apply movement
        magnitude = max(1, (move_vector[0]**2 + move_vector[1]**2)**0.5)
        new_x = self.x + round(move_vector[0] / magnitude)
        new_y = self.y + round(move_vector[1] / magnitude)
        
        # Boundary checking
        new_x = max(0, min(new_x, max_x - 1))
        new_y = max(0, min(new_y, max_y - 1))
        
        if not self.env.is_position_blocked(new_x, new_y):
            self.x, self.y = new_x, new_y

    def update(self):
        """Update creature state"""
        if not self.dead:
            self.age += 1
            if self.age >= 20:  # Maturity age stays at 20
                self.mature = True
            
            # Age effects
            if self.age > self.max_age * 0.7:  # After 70% of lifespan
                # Gradual health decline
                if random.random() < 0.1:  # 10% chance each tick
                    self.health = max(0, self.health - 1)
                
            if self.age >= self.max_age:
                self.die()

        # Reset eating state and color at start of update
        self.eating = False
        if not self.sleeping and not self.dead:  # Reset color only if not sleeping or dead
            self.color = (0, 255, 0)  # Reset to normal green

        # Health regeneration when well-fed
        if self.hunger >= 75 and self.health < 100 and not self.dead:
            health_regen = 2  # Regenerate 2 health per tick when well-fed
            self.health = min(100, self.health + health_regen)
            self.color = (100, 255, 100)  # Light green when healing

        # Check for nearby food with improved detection
        if self.hunger < 70 and not self.dead:  # Food seeking behavior
            # Check all adjacent positions including diagonals
            adjacent_positions = [
                (self.x + dx, self.y + dy) 
                for dx in [-1, 0, 1] 
                for dy in [-1, 0, 1] 
                if not (dx == 0 and dy == 0)
            ]
            
            for pos_x, pos_y in adjacent_positions:
                if (pos_x, pos_y) in self.env.grid:
                    other = self.env.grid[(pos_x, pos_y)]
                    if isinstance(other, Creature) and other.dead and other.food_value > 0:
                        # Wake up if sleeping to eat when very hungry
                        if self.sleeping and self.hunger < 30:
                            self.sleeping = False
                            self.color = (0, 255, 0)
                        if not self.sleeping:  # Only eat if awake
                            if self.eat(other):
                                self.env.remove_dead_creature(other)
                                return  # Skip rest of update if eating

        if not self.dead:  # Rest behavior
            # Rest if energy is very low
            if self.energy <= self.rest_threshold and not self.sleeping:
                self.sleeping = True
                self.color = (100, 100, 255)  # Blue color when sleeping
            # Rest if well-fed and energy isn't full (to prepare for egg laying)
            elif self.hunger > 80 and self.energy < 90 and not self.sleeping:
                self.sleeping = True
                self.color = (100, 100, 255)
            # Wake up if energy is high enough
            elif self.sleeping and self.energy >= self.wake_threshold:
                self.sleeping = False
                self.color = (0, 255, 0)

        # Energy and hunger updates
        if not self.sleeping:
            if random.random() < 0.5:  # 50% chance to lose hunger each tick
                self.hunger = max(0, self.hunger - 1)  # Normal hunger drain
            energy_cost = 2 if self.eating else 1  # Eating costs more energy
            self.energy = max(0, self.energy - energy_cost)
        else:
            # Reduced hunger drain while sleeping
            if random.random() < 0.1:  # Only drain hunger 10% of the time while sleeping (reduced from 25%)
                self.hunger = max(0, self.hunger - 1)
            recovery_rate = 3 if self.hunger > 50 else 1
            self.energy = min(100, self.energy + recovery_rate)
        
        # Health reduction from hunger
        if self.hunger <= 0:
            self.health -= 1
        if self.health <= 0:
            self.die()

        self.happiness = self.calculate_happiness()

        # Egg laying logic - made much more restrictive
        if not self.egg and self.mature and not self.has_laid_egg:
            if (self.happiness >= 90 and    # Increased from 85
                self.energy >= 90 and       # Increased from 75
                self.hunger >= 90 and       # Increased from 80
                random.random() < 0.05):    # Reduced from 0.1 (5% chance instead of 10%)
                self.lay_egg()

    def lay_egg(self):
        """Prepare to lay an egg."""
        if self.energy >= 90 and not self.egg:  # Increased energy requirement
            self.energy -= 90  # Increased energy cost
            self.egg = True

    def die(self):
        """Mark the creature as dead instead of removing it."""
        self.dead = True
        self.color = (255, 0, 0)  # Red color for dead creatures
        self.health = 0
        self.food_value = 300  # Doubled from 100 to 200 - dead creatures provide more food

    def __str__(self):
        if self.dead:
            return f"""DEAD CREATURE
Remaining Food: {self.food_value}%
Position: ({self.x}, {self.y})"""
        else:
            status = []
            if self.sleeping:
                status.append("Sleeping")
            if self.eating:
                status.append("Eating")
            if self.has_laid_egg:
                status.append("Has unhatched egg")
            
            age_percent = (self.age / self.max_age) * 100
            
            return f"""Health: {self.health}%
Energy: {self.energy}%
Hunger: {self.hunger}%
Happiness: {round(self.happiness)}%
Age: {self.age} ({round(age_percent, 1)}% of lifespan)
Max Age: {self.max_age}
Mature: {'Yes' if self.mature else 'No'}
Status: {', '.join(status) if status else 'Active'}
Position: ({self.x}, {self.y})
Has Egg: {'Yes' if self.egg else 'No'}"""

    def eat(self, food_source):
        """Consume some food from a dead creature"""
        if not self.dead and food_source.dead and food_source.food_value > 0:
            self.eating = True
            food_amount = min(40, food_source.food_value)  # Increased from 20 to 40
            food_source.food_value -= food_amount
            self.hunger = min(100, self.hunger + food_amount * 1.5)  # Increased food efficiency
            return True
        return False

# The environment where creatures live
class Environment:
    def __init__(self, width, height):
        # Adjust width to account for sidebar
        self.width = width - (SIDEBAR_WIDTH // GRID_SIZE)
        self.height = height
        # Pass self (environment) to creature constructor
        self.creatures = [
            Creature(random.randint(0, self.width-1), 
                    random.randint(0, self.height-1),
                    self)  # Pass self here
        ]
        
        # Add a dead creature at startup
        dead_creature = Creature(random.randint(0, self.width-1),
                               random.randint(0, self.height-1),
                               self)
        dead_creature.die()  # This sets dead=True and food_value=300
        self.creatures.append(dead_creature)
        
        self.eggs = []  # List to track eggs
        self.grid = {}  # Add a grid to track occupied positions
        # Add initial creatures to the grid
        for creature in self.creatures:
            self.grid[(creature.x, creature.y)] = creature
            
        self.creatures_to_remove = []  # Track creatures to remove after being eaten
        self.cell_size = GRID_SIZE * 2  # Size of each partition cell
        self.spatial_grid = {}  # Spatial partitioning grid
        
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
            # Include dead creatures in the grid
            self.grid[(creature.x, creature.y)] = creature
        for egg in self.eggs:
            self.grid[(egg.x, egg.y)] = egg

        # First, check for any eggs that are ready to hatch
        for egg in self.eggs:
            egg.update()
            if egg.ready_to_hatch:
                # Find the parent creature and allow it to lay new eggs
                for creature in self.creatures:
                    if creature.has_laid_egg:
                        creature.has_laid_egg = False
                eggs_to_remove.append(egg)
                self.grid.pop((egg.x, egg.y), None)
                new_creatures.append(Creature(egg.x, egg.y, self, health=100, energy=50))
        
        # Remove hatched eggs and add new creatures
        self.eggs = [egg for egg in self.eggs if egg not in eggs_to_remove]
        self.creatures.extend(new_creatures)
        
        # Remove eaten creatures
        if self.creatures_to_remove:
            self.creatures = [c for c in self.creatures if c not in self.creatures_to_remove]
            self.creatures_to_remove.clear()

        # Then update creatures and handle new egg laying
        for creature in self.creatures:
            if creature.health > 0:
                old_x, old_y = creature.x, creature.y
                
                # Only move if not eating
                if not creature.eating:
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
                        creature.has_laid_egg = True  # Mark that this creature has an unhatched egg
                    else:
                        # If no open spots, cancel egg laying
                        creature.egg = False

    def draw(self, screen):
        # Create batch for efficient rendering
        batch = pyglet.graphics.Batch()
        
        # Create all shapes in the batch
        shapes = []
        
        # Draw eggs first (so they appear under creatures)
        for egg in self.eggs:
            if egg.selected:
                shapes.append(pyglet.shapes.Circle(
                    egg.x * GRID_SIZE + GRID_SIZE // 2,
                    egg.y * GRID_SIZE + GRID_SIZE // 2,
                    (GRID_SIZE // 3) + 2,  # Just slightly larger than egg size
                    color=(255, 255, 255),  # White selection circle
                    batch=batch
                ))
            
            shapes.append(pyglet.shapes.Circle(
                egg.x * GRID_SIZE + GRID_SIZE // 2,
                egg.y * GRID_SIZE + GRID_SIZE // 2,
                GRID_SIZE // 3,  # Egg size stays the same
                color=(255, 200, 0),  # Golden/yellow color for eggs
                batch=batch
            ))
        
        # Draw creatures (existing code)
        for creature in self.creatures:
            if creature.eating:
                shapes.append(pyglet.shapes.Circle(
                    creature.x * GRID_SIZE + GRID_SIZE // 2,
                    creature.y * GRID_SIZE + GRID_SIZE // 2,
                    GRID_SIZE // 2 + 4,
                    color=(255, 255, 0),
                    batch=batch
                ))
            
            if creature.selected:
                shapes.append(pyglet.shapes.Circle(
                    creature.x * GRID_SIZE + GRID_SIZE // 2,
                    creature.y * GRID_SIZE + GRID_SIZE // 2,
                    GRID_SIZE // 2 + 2,
                    color=(255, 255, 255),
                    batch=batch
                ))
            
            shapes.append(pyglet.shapes.Circle(
                creature.x * GRID_SIZE + GRID_SIZE // 2,
                creature.y * GRID_SIZE + GRID_SIZE // 2,
                GRID_SIZE // 2,
                color=creature.color,
                batch=batch
            ))
        
        # Draw everything in one call
        batch.draw()

    def is_position_blocked(self, x, y):
        """Check if a position is blocked by a living creature"""
        if (x, y) in self.grid:
            entity = self.grid[(x, y)]
            # Allow movement through dead creatures (to prevent gridlock)
            if isinstance(entity, Creature) and not entity.dead:
                return True
        return False

    def find_nearest_food(self, x, y):
        """Find the nearest dead creature with improved accessibility check"""
        food_sources = []
        
        for creature in self.creatures:
            if creature.dead and creature.food_value > 0:
                # Calculate base distance
                distance = abs(x - creature.x) + abs(y - creature.y)
                
                # Check if there's too many creatures already targeting this food
                nearby_creatures = sum(1 for c in self.creatures 
                                     if not c.dead and 
                                     abs(c.x - creature.x) + abs(c.y - creature.y) <= 1)
                
                # Add penalty to distance based on nearby creatures
                distance += nearby_creatures * 2
                
                food_sources.append((creature.x, creature.y, distance))
        
        if food_sources:
            # Sort by adjusted distance and add small random factor to prevent perfect alignment
            food_sources.sort(key=lambda x: x[2] + random.uniform(0, 0.5))
            return (food_sources[0][0], food_sources[0][1])
            
        return None

    def remove_dead_creature(self, creature):
        """Mark a dead creature for removal after being fully consumed"""
        if creature.food_value <= 0:
            self.creatures_to_remove.append(creature)

    def count_nearby_creatures(self, x, y):
        """Count number of creatures in adjacent cells"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = x + dx
                check_y = y + dy
                if (check_x, check_y) in self.grid:
                    entity = self.grid[(check_x, check_y)]
                    if isinstance(entity, Creature) and not entity.dead:
                        count += 1
        return count

    def get_nearby_entities(self, x, y, radius=2):
        """Get entities in nearby cells using spatial partitioning"""
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        nearby = []
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.spatial_grid:
                    nearby.extend(self.spatial_grid[cell])
        
        return nearby

    def update_spatial_grid(self):
        """Update spatial partitioning grid"""
        self.spatial_grid.clear()
        for creature in self.creatures:
            cell = (creature.x // self.cell_size, creature.y // self.cell_size)
            if cell not in self.spatial_grid:
                self.spatial_grid[cell] = []
            self.spatial_grid[cell].append(creature)

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
    
    return str(creature)  # Use the creature's string representation

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
