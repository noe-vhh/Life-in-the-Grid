import pyglet
import random
import math

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 50
SIDEBAR_WIDTH = 200
FPS = 1  # Initial FPS
MIN_FPS = 1
MAX_FPS = 60
NEST_CENTER_X = WIDTH // 4  # Center of the nest area
NEST_CENTER_Y = HEIGHT // 2
FOOD_STORAGE_RADIUS = 5 * GRID_SIZE
NURSERY_RADIUS = 3 * GRID_SIZE
SLEEPING_RADIUS = 4 * GRID_SIZE

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
    def __init__(self, x, y, environment, health=100, energy=100):
        # Initialize all attributes first
        self.egg_laying_cooldown = 0
        self.egg_laying_cooldown_max = 100
        self.rest_threshold = 30
        self.wake_threshold = 80
        self.max_age = random.randint(300, 500)
        self.selected = False
        
        # Then set the basic attributes
        self.x = x
        self.y = y
        self.env = environment
        self.health = health
        self.energy = energy
        self.hunger = 100
        self.age = 0
        self.mature = False
        self.dead = False
        self.sleeping = False
        self.eating = False
        self.color = (0, 255, 0)
        self.happiness = 100
        self.food_value = 100
        self.age_related_health_loss = False
        self.carrying_food = False
        self.target = None
        self.egg = False
        self.has_laid_egg = False

    def calculate_happiness(self):
        """Calculate creature happiness based on various factors"""
        happiness = 100
        
        if self.hunger < 50:
            happiness -= (50 - self.hunger)
        if self.energy < 50:
            happiness -= (50 - self.energy)
        if self.health < 50:
            happiness -= (50 - self.health)
        
        return max(0, min(100, happiness))

    def move(self, max_x, max_y):
        if self.dead:
            return

        target_x, target_y = self.x, self.y
        
        # Determine target position based on state
        if self.target == "sleeping":
            # Get sleep area center
            center = self.env.get_area_center("sleeping")
            target_x = int(center[0] / GRID_SIZE)
            target_y = int(center[1] / GRID_SIZE)
            # Move directly towards sleep area
            self.env.try_move_towards(self, target_x, target_y)
            return
        elif self.target == "food":
            center = self.env.get_area_center("food")
            target_x = int(center[0] / GRID_SIZE)
            target_y = int(center[1] / GRID_SIZE)
        elif isinstance(self.target, (Creature, Egg)):
            target_x, target_y = self.target.x, self.target.y
        else:
            # Random movement with bias towards current direction
            if random.random() < 0.8:
                target_x = self.x + random.randint(-1, 1)
                target_y = self.y + random.randint(-1, 1)
            else:
                angle = random.uniform(0, 2 * 3.14159)
                target_x = self.x + round(math.cos(angle))
                target_y = self.y + round(math.sin(angle))
        
        # Ensure target is within bounds
        target_x = max(0, min(target_x, max_x - 1))
        target_y = max(0, min(target_y, max_y - 1))
        
        # Try to move towards target
        self.env.try_move_towards(self, target_x, target_y)

    def update(self):
        """Update creature state"""
        if not self.dead:
            self.age += 1
            if self.age >= 20:
                self.mature = True
            
            # Age effects and death
            if self.age > self.max_age * 0.7:
                if random.random() < 0.1:
                    self.health = max(0, self.health - 1)
                    self.age_related_health_loss = True
            
            if self.age >= self.max_age:
                self.die()
                return

            # Check for sleep need
            if self.energy <= self.rest_threshold and not self.sleeping:
                self.sleeping = True
                self.color = (100, 100, 255)  # Blue while sleeping
                self.target = "sleeping"
                return

            # Sleep behavior
            if self.sleeping:
                if not self.env.is_in_area(self.x, self.y, "sleeping"):
                    self.move(self.env.width, self.env.height)
                else:
                    # Stay still while sleeping in the correct area
                    recovery_rate = 3 if self.hunger > 50 else 1
                    self.energy = min(100, self.energy + recovery_rate)
                    if random.random() < 0.1:
                        self.hunger = max(0, self.hunger - 1)
                
                # Check if we should wake up
                if self.energy >= self.wake_threshold:
                    self.sleeping = False
                    self.color = (0, 255, 0)
                    self.target = None
                return

            # Awake behavior
            if not self.sleeping:
                self.move(self.env.width, self.env.height)
                
                # Reset states
                self.eating = False
                if not self.carrying_food:
                    self.color = (0, 255, 0)

                # Priority 1: Eating when hungry
                if self.hunger < 70:
                    nearby_entities = self.env.get_nearby_entities(self.x, self.y)
                    found_food = False
                    
                    for entity in nearby_entities:
                        if isinstance(entity, Creature) and entity.dead and entity.food_value > 0:
                            dx = abs(self.x - entity.x)
                            dy = abs(self.y - entity.y)
                            if dx + dy == 1:  # Adjacent but not diagonal
                                if self.eat(entity):
                                    self.color = (255, 200, 0)  # Yellow while eating
                                    found_food = True
                                    if entity.food_value <= 0:
                                        self.env.remove_dead_creature(entity)
                                    break
                    
                    if not found_food:
                        # Move towards nearest food
                        for entity in nearby_entities:
                            if isinstance(entity, Creature) and entity.dead and entity.food_value > 0:
                                self.target = entity
                                break

                # Priority 2: Body transport when well-fed
                elif not self.carrying_food and self.hunger >= 70:
                    nearby_entities = self.env.get_nearby_entities(self.x, self.y)
                    for entity in nearby_entities:
                        if (isinstance(entity, Creature) and entity.dead and 
                            not self.env.is_in_area(entity.x, entity.y, "food")):
                            dx = abs(self.x - entity.x)
                            dy = abs(self.y - entity.y)
                            if dx + dy == 1:  # Adjacent but not diagonal
                                self.target = entity
                                self.carrying_food = True
                                self.color = (200, 150, 50)  # Brown while carrying
                                break
                            elif dx + dy <= 3:  # If nearby but not adjacent
                                self.target = entity
                                break

                # Handle carrying and dropping food
                if self.carrying_food and isinstance(self.target, Creature):
                    if self.env.is_in_area(self.x, self.y, "food"):
                        # Try to drop in food storage area
                        adjacent_spots = [
                            (self.x + dx, self.y + dy)
                            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                            if (self.env.is_in_area(self.x + dx, self.y + dy, "food") and 
                                not self.env.is_position_occupied(self.x + dx, self.y + dy))
                        ]
                        
                        if adjacent_spots:
                            drop_x, drop_y = random.choice(adjacent_spots)
                            if self.env.move_entity(self.target, drop_x, drop_y):
                                self.carrying_food = False
                                self.target = None
                                self.color = (0, 255, 0)
                    else:
                        # Move the dead creature along with us
                        dead_creature = self.target
                        # Try to move dead creature to an adjacent spot
                        adjacent_spots = [
                            (self.x + dx, self.y + dy)
                            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                            if not self.env.is_position_occupied(self.x + dx, self.y + dy)
                        ]
                        
                        if adjacent_spots:
                            new_x, new_y = random.choice(adjacent_spots)
                            self.env.move_entity(dead_creature, new_x, new_y)
                        
                        # Keep moving towards food storage
                        self.target = "food"

                # Energy and hunger updates
                if random.random() < 0.5:
                    self.hunger = max(0, self.hunger - 1)
                energy_cost = 2 if self.eating else 1
                self.energy = max(0, self.energy - energy_cost)

            # Health reduction from hunger
            if self.hunger <= 0:
                self.health -= 1
            if self.health <= 0:
                self.die()

            self.happiness = self.calculate_happiness()

            # Egg laying logic - reduced thresholds and better conditions
            if (not self.sleeping and not self.eating and 
                not self.egg and self.mature and not self.has_laid_egg and
                self.happiness >= 70 and  # Reduced from 90
                self.energy >= 60 and     # Reduced from 90
                self.hunger >= 60):       # Reduced from 90
                
                if self.env.is_in_area(self.x, self.y, "nursery"):
                    # Try to lay egg in adjacent spot
                    adjacent_spots = [
                        (self.x + dx, self.y + dy)
                        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                        if (self.env.is_valid_position(self.x + dx, self.y + dy) and
                            not self.env.is_position_occupied(self.x + dx, self.y + dy) and
                            self.env.is_in_area(self.x + dx, self.y + dy, "nursery"))
                    ]
                    
                    if adjacent_spots:
                        egg_x, egg_y = random.choice(adjacent_spots)
                        self.energy -= 50  # Reduced energy cost from 90
                        new_egg = Egg(egg_x, egg_y)
                        self.env.eggs.append(new_egg)
                        self.env.grid[(egg_x, egg_y)] = new_egg
                        self.has_laid_egg = True
                        self.target = None
                else:
                    # Move towards nursery if ready to lay egg
                    self.target = "nursery"
                    self.color = (255, 200, 200)  # Pink while ready to lay egg

    def lay_egg(self):
        """Lay an egg in the current position if in nursery"""
        if self.energy >= 90 and not self.egg:
            # Try to lay egg in current position
            if not self.env.is_position_occupied(self.x, self.y + 1):
                self.energy -= 90
                new_egg = Egg(self.x, self.y + 1)
                self.env.eggs.append(new_egg)
                self.env.grid[(self.x, self.y + 1)] = new_egg
                self.has_laid_egg = True
            elif not self.env.is_position_occupied(self.x + 1, self.y):
                self.energy -= 90
                new_egg = Egg(self.x + 1, self.y)
                self.env.eggs.append(new_egg)
                self.env.grid[(self.x + 1, self.y)] = new_egg
                self.has_laid_egg = True

    def die(self):
        """Mark the creature as dead instead of removing it."""
        self.dead = True
        self.color = (255, 0, 0)  # Red color for dead creatures
        self.health = 0
        self.food_value = 300  # Doubled from 100 to 200 - dead creatures provide more food
        
        # Determine cause of death
        if self.age >= self.max_age:
            self.death_cause = "Old Age"
        elif self.hunger <= 0:
            self.death_cause = "Starvation"
        else:
            self.death_cause = "Unknown"

    def __str__(self):
        if self.dead:
            return f"""DEAD CREATURE
Cause: {self.death_cause}
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
            if self.age > self.max_age * 0.7:
                status.append("(!) Elderly")  # Changed from emoji to standard characters
            
            age_percent = (self.age / self.max_age) * 100
            
            return f"""Health: {self.health}%
Energy: {self.energy}%
Hunger: {self.hunger}%
Happiness: {round(self.happiness)}%
Age: {self.age} ({round(age_percent, 1)}% of lifespan)
Max Age: {self.max_age}
Mature: {'Yes' if self.mature else 'No'}
Status: {', '.join(status) if status else 'Active'}
Position: ({self.x}, {self.y})"""

    def eat(self, food_source):
        """Consume some food from a dead creature when adjacent to it"""
        if (not self.dead and food_source.dead and food_source.food_value > 0 and
            not self.sleeping and self.hunger < 100):
            # Check if we're adjacent to the food source
            dx = abs(self.x - food_source.x)
            dy = abs(self.y - food_source.y)
            if dx + dy == 1:  # Must be exactly one space away (no diagonals)
                self.eating = True
                food_amount = min(40, food_source.food_value)
                food_source.food_value -= food_amount
                self.hunger = min(100, self.hunger + food_amount * 1.5)
                self.color = (255, 200, 0)  # Yellow while eating
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
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True  # Consider out-of-bounds as occupied
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
        # Clear and rebuild grid at the start of update
        self.grid.clear()
        for creature in self.creatures:
            self.grid[(creature.x, creature.y)] = creature
        for egg in self.eggs:
            self.grid[(egg.x, egg.y)] = egg
        
        # Update creatures
        for creature in self.creatures:
            if not creature.dead:
                old_x, old_y = creature.x, creature.y
                creature.update()  # This will now call move()
                
                # Update grid if position changed
                if (creature.x, creature.y) != (old_x, old_y):
                    self.grid.pop((old_x, old_y), None)
                    self.grid[(creature.x, creature.y)] = creature
        
        # Handle colony organization
        for creature in self.creatures:
            if creature.dead and not self.is_in_area(creature.x, creature.y, "food"):
                # Find nearby creature to move the dead one
                for other in self.creatures:
                    if (not other.dead and not other.carrying_food and 
                        not other.target and
                        abs(other.x - creature.x) + abs(other.y - creature.y) <= 2):
                        other.target = creature
                        other.carrying_food = True
                        break
                    
        # Update eggs
        eggs_to_remove = []
        for egg in self.eggs:
            egg.update()
            if egg.ready_to_hatch:
                eggs_to_remove.append(egg)
                if (egg.x, egg.y) in self.grid:
                    self.grid.pop((egg.x, egg.y))
                new_creature = Creature(egg.x, egg.y, self)
                self.creatures.append(new_creature)
                self.grid[(egg.x, egg.y)] = new_creature
                
        # Remove hatched eggs
        self.eggs = [egg for egg in self.eggs if egg not in eggs_to_remove]

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
        
        # Draw colony areas
        areas = [
            ("food", FOOD_STORAGE_RADIUS, (100, 50, 50)),
            ("nursery", NURSERY_RADIUS, (50, 100, 50)),
            ("sleeping", SLEEPING_RADIUS, (50, 50, 100))
        ]

        for area_type, radius, color in areas:
            center = self.get_area_center(area_type)
            shapes.append(pyglet.shapes.Circle(
                center[0], center[1], radius,
                color=(*color, 50),  # Semi-transparent
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

    def get_nearby_entities(self, x, y, radius=3):
        """Get entities in nearby cells"""
        nearby = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                check_x = x + dx
                check_y = y + dy
                if (check_x, check_y) in self.grid:
                    nearby.append(self.grid[(check_x, check_y)])
        return nearby

    def update_spatial_grid(self):
        """Update spatial partitioning grid"""
        self.spatial_grid.clear()
        for creature in self.creatures:
            cell = (creature.x // self.cell_size, creature.y // self.cell_size)
            if cell not in self.spatial_grid:
                self.spatial_grid[cell] = []
            self.spatial_grid[cell].append(creature)

    def get_area_center(self, area_type):
        """Get the center coordinates for different colony areas"""
        if area_type == "food":
            return (NEST_CENTER_X - FOOD_STORAGE_RADIUS, NEST_CENTER_Y)
        elif area_type == "nursery":
            return (NEST_CENTER_X + NURSERY_RADIUS, NEST_CENTER_Y + NURSERY_RADIUS)
        elif area_type == "sleeping":
            return (NEST_CENTER_X, NEST_CENTER_Y - SLEEPING_RADIUS)
        return (NEST_CENTER_X, NEST_CENTER_Y)

    def is_in_area(self, x, y, area_type):
        """Check if position is within a specific colony area"""
        # Convert grid coordinates to pixel coordinates for center calculation
        px = x * GRID_SIZE + GRID_SIZE // 2
        py = y * GRID_SIZE + GRID_SIZE // 2
        
        center = self.get_area_center(area_type)
        distance = ((px - center[0])**2 + (py - center[1])**2)**0.5
        
        if area_type == "food":
            return distance <= FOOD_STORAGE_RADIUS
        elif area_type == "nursery":
            return distance <= NURSERY_RADIUS
        elif area_type == "sleeping":
            return distance <= SLEEPING_RADIUS
        return False

    def find_nursery_spot(self):
        """Find an open spot in the nursery area"""
        center = self.get_area_center("nursery")
        center_x = int(center[0] / GRID_SIZE)
        center_y = int(center[1] / GRID_SIZE)
        
        for radius in range(1, int(NURSERY_RADIUS / GRID_SIZE)):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    x = center_x + dx
                    y = center_y + dy
                    if (self.is_in_area(x, y, "nursery") and 
                        not self.is_position_occupied(x, y)):
                        return x, y
        return None

    def move_entity(self, entity, new_x, new_y):
        """Safely move an entity to a new position"""
        if not self.is_valid_position(new_x, new_y):
            return False
        
        if (new_x, new_y) in self.grid:
            return False
        
        # Remove from old position
        self.grid.pop((entity.x, entity.y), None)
        
        # Update position
        entity.x = new_x
        entity.y = new_y
        
        # Add to new position
        self.grid[(new_x, new_y)] = entity
        return True

    def try_move_towards(self, entity, target_x, target_y):
        """Try to move entity towards target, handling collisions"""
        if entity.dead:
            return False
        
        dx = target_x - entity.x
        dy = target_y - entity.y
        
        # If already at target, no need to move
        if dx == 0 and dy == 0:
            return True
        
        # Calculate movement direction
        move_x = 0 if dx == 0 else dx // abs(dx)
        move_y = 0 if dy == 0 else dy // abs(dy)
        
        # Try primary movement direction first
        if abs(dx) > abs(dy):
            # Try horizontal movement first
            if not self.is_position_occupied(entity.x + move_x, entity.y):
                return self.move_entity(entity, entity.x + move_x, entity.y)
            # Then try vertical
            elif not self.is_position_occupied(entity.x, entity.y + move_y):
                return self.move_entity(entity, entity.x, entity.y + move_y)
        else:
            # Try vertical movement first
            if not self.is_position_occupied(entity.x, entity.y + move_y):
                return self.move_entity(entity, entity.x, entity.y + move_y)
            # Then try horizontal
            elif not self.is_position_occupied(entity.x + move_x, entity.y):
                return self.move_entity(entity, entity.x + move_x, entity.y)
        
        # If primary movements failed, try diagonal
        if not self.is_position_occupied(entity.x + move_x, entity.y + move_y):
            return self.move_entity(entity, entity.x + move_x, entity.y + move_y)
        
        return False

    def try_move_dead_creature(self, carrier, dead_creature):
        """Try to move a dead creature towards food storage"""
        if not isinstance(dead_creature, Creature) or not dead_creature.dead:
            return False

        # Get food storage center
        center = self.get_area_center("food")
        target_x = int(center[0] / GRID_SIZE)
        target_y = int(center[1] / GRID_SIZE)

        # Calculate movement direction
        dx = target_x - dead_creature.x
        dy = target_y - dead_creature.y
        
        # Normalize direction
        dist = max(1, (dx*dx + dy*dy)**0.5)
        move_x = round(dx / dist)
        move_y = round(dy / dist)

        # Try to move the dead creature
        new_x = dead_creature.x + move_x
        new_y = dead_creature.y + move_y

        return self.move_entity(dead_creature, new_x, new_y)

    def is_valid_position(self, x, y):
        """Check if a position is within bounds"""
        return 0 <= x < self.width and 0 <= y < self.height

    def find_valid_egg_spot(self, x, y):
        """Find a valid spot for an egg near the given position"""
        # Check immediate adjacent spots first
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = x + dx
            new_y = y + dy
            if (self.is_valid_position(new_x, new_y) and
                not self.is_position_occupied(new_x, new_y) and
                self.is_in_area(new_x, new_y, "nursery")):
                return new_x, new_y
            
        # If no immediate spots, check slightly further
        for d in range(2, 4):
            for dx in range(-d, d+1):
                for dy in range(-d, d+1):
                    if dx == 0 and dy == 0:
                        continue
                    new_x = x + dx
                    new_y = y + dy
                    if (self.is_valid_position(new_x, new_y) and
                        not self.is_position_occupied(new_x, new_y) and
                        self.is_in_area(new_x, new_y, "nursery")):
                        return new_x, new_y
        return None

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
