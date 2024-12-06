import pyglet
import random
import math

# Constants
WIDTH = 1200
HEIGHT = 900
GRID_SIZE = 50
SIDEBAR_WIDTH = 200        # Make sure sidebar is wide enough
FPS = 0  # Initial FPS (paused)
MIN_FPS = 1
MAX_FPS = 60
NEST_CENTER_X = WIDTH // 4  # Center of the nest area
NEST_CENTER_Y = HEIGHT // 2
FOOD_STORAGE_RADIUS = 5 * GRID_SIZE
NURSERY_RADIUS = 3 * GRID_SIZE
SLEEPING_RADIUS = 4 * GRID_SIZE
CONTROL_PANEL_HEIGHT = 60  # Just enough for buttons
STATS_PANEL_HEIGHT = 160   # Reduced height since we removed labels
LEGEND_PANEL_HEIGHT = 380  # Tall enough for all legend items
TOP_MARGIN = 5           # Small top margin
PANEL_SPACING = 8         # Increased spacing to prevent overlap
SIDE_MARGIN = 10        # Content margin from panel edge

# Update Constants with refined sizes and spacing
SIDEBAR_WIDTH = 280        # Slightly wider for better text display
TOP_MARGIN = 15           # Slightly larger margin
PANEL_SPACING = 15        # Increased spacing between panels

# Panel heights
CONTROL_PANEL_HEIGHT = 90  # Reduced as it only contains FPS control
STATS_PANEL_HEIGHT = 220  # Increased for stats content
LEGEND_PANEL_HEIGHT = 520  # Increased for legend content

# Legend specific constants
LEGEND_ITEM_SPACING = 24   # Space between legend items
LEGEND_HEADER_SPACING = 30 # Space after headers
LEGEND_GROUP_SPACING = 15  # Additional space between groups
LEGEND_TEXT_SIZE = 10      # Text size
LEGEND_HEADER_SIZE = 12    # Header text size
LEGEND_ICON_SIZE = 16      # Icon size
LEGEND_TOP_PADDING = 50    # Space from top of panel to first item

# Constants for area positioning (add these near other constants)
QUADRANT_OFFSET = 300  # Increased distance between centers to prevent overlap

# Add these constants near the top with other constants
ICON_ANIMATION_SPEED = 0.05  # Reduced from 0.5 to 0.2 (slower animation)
ICON_OFFSET_Y = GRID_SIZE // 2  # Changed from GRID_SIZE to GRID_SIZE // 2
ICON_SIZE = GRID_SIZE // 2  # Size of the icons

# Add these constants near other egg-related constants
EGG_PULSE_SPEED = 2.0  # Speed of the pulsing animation
EGG_INNER_RATIO = 0.7  # Size of the inner egg shape
EGG_SHINE_OFFSET = 0.3  # Offset for the shine effect

# Add these constants near other animation constants
BLINK_INTERVAL = 5  # Every ~5 frames at normal speed
BLINK_DURATION = 1  # Blink for 1 frame
EYE_SIZE = 3  # Size of the eyes
EYE_SPACING = 6  # Distance between eyes
EYE_OFFSET_Y = 2  # Vertical offset from center

# Add these constants near other eye-related constants
PUPIL_SIZE = 2  # Size of the pupil (smaller than eye)
PUPIL_RANGE = 2  # How far the pupil can move from center

# Add these constants near other creature appearance constants
ANTENNA_LENGTH = 8  # Length of each antenna
ANTENNA_WIDTH = 2   # Width/thickness of antennae
ANTENNA_SPACING = 6  # Space between antenna bases
ANTENNA_WAVE_SPEED = 0.25  # Speed of antenna movement
ANTENNA_WAVE_AMOUNT = 0.5  # How much the antennae wave (in radians)

# Add these constants near other animation constants
BREATH_SPEED = 0.1  # Even slower breathing animation
BREATH_AMOUNT = 0.05  # Increased from 0.08 to 0.15 (15% of size)
DEAD_BREATH_AMOUNT = 0.08  # Increased from 0.04 to 0.08 (8% of size)

# Near the top with other constants
HEART_ANIMATION_SPEED = 2.0  # Adjust this value to control animation speed

# Add these constants near other appearance-related constants
MOUTH_WIDTH = 8  # Width of the mouth
MOUTH_HEIGHT = 4  # Height of the mouth when open
MOUTH_Y_OFFSET = -8  # Lowered vertical position relative to center
MOUTH_OPEN_SPEED = 0.1  # Speed of mouth opening/closing animation
MAX_MOUTH_OPEN = 6  # Maximum height when eating
SMILE_CURVE = 3  # Amount of curve for smiles/frowns

<<<<<<< HEAD
<<<<<<< HEAD
# Add these constants near other appearance-related constants
TEXTURE_PATTERNS = {
    "dots": {"chance": 0.25, "density": 8},
    "stripes": {"chance": 0.25, "density": 4},
    "spots": {"chance": 0.25, "density": 5},
    "plain": {"chance": 0.25}  # Default pattern
}

PATTERN_COLORS = [
    (255, 255, 255),  # White
    (50, 50, 50),     # Dark Gray
    (200, 200, 200),  # Light Gray
    (255, 223, 186),  # Peach
    (255, 218, 233),  # Pink
    (230, 230, 255)   # Light Blue
]

# Add near other UI constants
LOADING_BAR_WIDTH = 120
LOADING_BAR_HEIGHT = 15
LOADING_BAR_PADDING = 5
LOADING_BAR_COLORS = {
    'health': (255, 50, 50),    # Red
    'energy': (50, 150, 255),   # Blue
    'hunger': (255, 200, 50),   # Yellow
    'happiness': (255, 100, 255) # Pink
}

class LoadingBar:
    def __init__(self, x, y, width, height, label, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.value = 0
        self.color = color
        self.extra_text = ""  # Add this field

    def update_value(self, value, extra_text=""):
        self.value = min(100, max(0, value))  # Clamp between 0 and 100
        self.extra_text = extra_text  # Store extra text

    def draw(self):
        # Draw label
        pyglet.text.Label(
            f"{self.label}: {int(self.value)}%{self.extra_text}",  # Add extra text here
            x=self.x,
            y=self.y + self.height + 5,
            anchor_y='bottom',
            color=(255, 255, 255, 255)
        ).draw()

        # Draw background
        pyglet.shapes.Rectangle(
            self.x, self.y,
            self.width, self.height,
            color=(50, 50, 50)
        ).draw()

        # Draw filled portion
        if self.value > 0:
            fill_width = (self.value / 100) * self.width
            pyglet.shapes.Rectangle(
                self.x, self.y,
                fill_width, self.height,
                color=self.color
            ).draw()

=======
>>>>>>> parent of fd846d1 (Added creature textures and patterns. Updated Todo list.)
=======
>>>>>>> parent of fd846d1 (Added creature textures and patterns. Updated Todo list.)
# Create a simple rectangle class for panel sections
class Panel:
    def __init__(self, x, y, width, height, title=""):
        self.width = width
        self.height = height
        self.title = title
        self.update_position(x, y)  # Separate position update
        
    def update_position(self, x, y):
        """Update panel position"""
        self.x = x
        self.y = y
        
    def draw(self):
        # Draw panel background
        pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, 
                              color=(40, 40, 40)).draw()
        # Draw panel border
        pyglet.shapes.BorderedRectangle(self.x, self.y, self.width, self.height,
                                      border=2, color=(40, 40, 40), 
                                      border_color=(100, 100, 100)).draw()
        # Draw centered title if exists
        if self.title:
            pyglet.text.Label(self.title,
                            font_name='Arial',
                            font_size=12,
                            bold=True,
                            x=self.x + self.width//2,
                            y=self.y + self.height - 20,
                            anchor_x='center',  # Changed from 'left' to 'center'
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

# Create the window with resizable=False and fixed size
window = pyglet.window.Window(WIDTH, HEIGHT, "Creature Simulation", resizable=False)

# Load images for buttons
pause_unclicked_image = pyglet.resource.image('Assets/UI Icons/pause-play-unclick.png')
pause_clicked_image = pyglet.resource.image('Assets/UI Icons/pause-play-click.png')

play_unclicked_image = pyglet.resource.image('Assets/UI Icons/play-button-unclick.png')
play_clicked_image = pyglet.resource.image('Assets/UI Icons/play-button-click.png')

fast_forward_unclicked_image = pyglet.resource.image('Assets/UI Icons/fast-forward-button-unclick.png')
fast_forward_clicked_image = pyglet.resource.image('Assets/UI Icons/fast-forward-button-click.png')

# Create sprites for buttons with scaling
icon_scale = 0.075  # Adjusted scale factor

# Calculate the y position to be below the "Controls" label
buttons_y_position = HEIGHT - CONTROL_PANEL_HEIGHT + 20  # Reduced from 120 to 20 to move buttons higher

# Create panels before anything else
control_panel = Panel(
    WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
    HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT,
    SIDEBAR_WIDTH,
    CONTROL_PANEL_HEIGHT,
    "Controls"
)

stats_panel = Panel(
    WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
    HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT - PANEL_SPACING - STATS_PANEL_HEIGHT,
    SIDEBAR_WIDTH,
    STATS_PANEL_HEIGHT,
    "Stats"
)

legend_panel = Panel(
    WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
    HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT - PANEL_SPACING - 
    STATS_PANEL_HEIGHT - PANEL_SPACING - LEGEND_PANEL_HEIGHT,
    SIDEBAR_WIDTH,
    LEGEND_PANEL_HEIGHT,
    "Legend"
)

# THEN create the button sprites with pause initially clicked
pause_button = pyglet.sprite.Sprite(
    pause_clicked_image,  # Start with clicked image
    x=WIDTH - SIDEBAR_WIDTH + 15, 
    y=control_panel.y + control_panel.height - 75
)
pause_button.scale = icon_scale

play_button = pyglet.sprite.Sprite(
    play_unclicked_image, 
    x=WIDTH - SIDEBAR_WIDTH + 75, 
    y=control_panel.y + control_panel.height - 75
)
play_button.scale = icon_scale

fast_forward_button = pyglet.sprite.Sprite(
    fast_forward_unclicked_image, 
    x=WIDTH - SIDEBAR_WIDTH + 135, 
    y=control_panel.y + control_panel.height - 75
)
fast_forward_button.scale = icon_scale

# Variable to track if FPS input is active
fps_input_active = False

# Add this near the top with other global variables
current_speed_state = "pause"  # Start paused

# Update Constants section - add new indicator constants
INDICATOR_BORDER_WIDTH = 2
SELECTION_RING_SIZE = 4
STATUS_RING_SIZE = 2
INNER_CIRCLE_RATIO = 0.6  # Size of inner circle relative to main body

# Near the top of the file with other global variables
stats_bars = None  # Initialize as None

class Creature:
    def __init__(self, x, y, environment, health=100, energy=100):
        # Initialize all attributes first
        self.egg_laying_cooldown = 0
        self.egg_laying_cooldown_max = 300
        self.rest_threshold = 30
        self.wake_threshold = 80
        self.max_age = random.randint(500, 750)
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
        self.base_color = (0, 255, 0)  # Store base color for normal state
        self.color = self.base_color
        self.happiness = 100
        self.food_value = 100
        self.age_related_health_loss = False
        self.carrying_food = False
        self.target = None
        self.egg = False
        self.has_laid_egg = False
        self.dragging_target = None  # Add this new attribute
        
        # Add animation properties
        self.animation_timer = 0
        self.animation_frame = 0
        
        # Add eye animation properties
        self.blink_timer = random.uniform(0, BLINK_INTERVAL)
        self.is_blinking = False
        
        # Add breathing animation property
        self.breath_offset = random.uniform(0, 2 * math.pi)  # Random starting phase
        
        # Add heart animation property
        self.heart_animation_offset = random.uniform(0, 2 * math.pi)  # Add random starting phase
        
        # Add mouth animation properties
        self.mouth_open_amount = 0
        self.target_mouth_open = 0
        self.is_chewing = False
        self.chew_timer = 0
        
    def calculate_happiness(self):
        """Calculate creature happiness based on various factors with weighted importance"""
        base_happiness = 100
        
        # Health factor (30% weight)
        health_factor = self.health / 100
        health_impact = 30 * health_factor
        
        # Hunger factor (25% weight)
        # More nuanced hunger impact - starts affecting happiness earlier
        hunger_factor = self.hunger / 100
        hunger_impact = 25 * hunger_factor
        
        # Energy factor (20% weight)
        # More nuanced energy impact - gradual decrease
        energy_factor = self.energy / 100
        energy_impact = 20 * energy_factor
        
        # Age factor (10% weight)
        # Happiness slightly decreases with age, but not too dramatically
        age_factor = max(0, 1 - (self.age / self.max_age) * 0.5)  # Only 50% decrease at max age
        age_impact = 10 * age_factor
        
        # Social factor (15% weight)
        # Count nearby creatures for social happiness
        nearby_creatures = len([c for c in self.env.get_nearby_entities(self.x, self.y, 2)
                              if isinstance(c, Creature) and not c.dead])
        social_factor = min(1.0, nearby_creatures / 3)  # Max happiness with 3 nearby creatures
        social_impact = 15 * social_factor
        
        # Calculate total happiness
        happiness = (health_impact + hunger_impact + energy_impact + 
                    age_impact + social_impact)
        
        # Additional modifiers
        if self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping"):
            happiness += 10  # Bonus for sleeping in proper area
        if self.has_laid_egg:
            happiness += 15  # Bonus for recent reproduction
        if self.carrying_food:
            happiness -= 5   # Slight decrease while working
        if self.age_related_health_loss:
            happiness -= 10  # Penalty for age-related health issues
        
        # Ensure happiness stays within bounds
        return max(0, min(100, happiness))

    def move(self, max_x, max_y):
        if self.dead:
            return
        
        # If we have a target that's a creature or egg, get its position
        target_x, target_y = self.x, self.y
        
        if isinstance(self.target, Creature) and self.target.dead:
            if self.carrying_food:
                # If carrying food, move towards food storage area
                food_center = self.env.get_area_center("food")
                target_x = int(food_center[0] / GRID_SIZE)
                target_y = int(food_center[1] / GRID_SIZE)
            else:
                # If not carrying yet, move towards the dead creature
                target_x, target_y = self.target.x, self.target.y
        elif isinstance(self.target, (Creature, Egg)):
            target_x, target_y = self.target.x, self.target.y
        elif self.target == "sleeping":
            center = self.env.get_area_center("sleeping")
            target_x = int(center[0] / GRID_SIZE)
            target_y = int(center[1] / GRID_SIZE)
        elif self.target == "nursery":
            center = self.env.get_area_center("nursery")
            target_x = int(center[0] / GRID_SIZE)
            target_y = int(center[1] / GRID_SIZE)
            self.color = (255, 200, 0)  # Match egg color when moving to nursery
        elif self.target == "food":
            # First check if there's food adjacent to eat
            nearby_entities = self.env.get_nearby_entities(self.x, self.y)
            # Sort dead creatures by remaining food value (ascending)
            nearby_entities.sort(key=lambda e: e.food_value if isinstance(e, Creature) and e.dead else float('inf'))
            for entity in nearby_entities:
                if isinstance(entity, Creature) and entity.dead and entity.food_value > 0:
                    dx = abs(self.x - entity.x)
                    dy = abs(self.y - entity.y)
                    if dx + dy == 1:  # Adjacent but not diagonal
                        if self.eat(entity):
                            self.target = None
                            return
            
            # If no adjacent food, find nearest food source
            food_position = self.env.find_nearest_food(self.x, self.y)
            if food_position:
                target_x, target_y = food_position
            else:
                # If no food found, move randomly
                target_x = self.x + random.randint(-1, 1)
                target_y = self.y + random.randint(-1, 1)
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
        if self.env.try_move_towards(self, target_x, target_y):
            # If we successfully moved and we're carrying food to the food area
            if (self.carrying_food and 
                isinstance(self.target, Creature) and 
                self.target.dead and 
                self.env.is_in_area(self.target.x, self.target.y, "food")):
                # Release the food once it's in the storage area
                self.carrying_food = False
                self.target = None
                self.color = (0, 255, 0)  # Reset color

    def update(self):
        if self.dead:
            return

        # Add this near the start of update
        self.update_mouth()
        
        if FPS > 0:  # Only update animation if game is not paused
            self.animation_timer += 1/60  # Increment by a fixed time step

        self.update_eyes()  # Add this line near the start
        
        # Always update basic stats first
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

        # Always update hunger and energy
        if random.random() < 0.2:
            self.hunger = max(0, self.hunger - 1)
        energy_cost = 1 if self.eating or self.carrying_food else 0.5
        self.energy = max(0, self.energy - energy_cost)

        # Reset eating state at the start of each update
        if self.eating:
            self.eating = False
            self.color = (0, 255, 0)  # Reset color
            self.animation_timer = 0
            self.animation_frame = 0

        # Health reduction from hunger
        if self.hunger <= 0:
            self.health = max(0, self.health - 1)
            if self.health <= 0:
                self.die()
                return

        # Modified hunger behavior - look for food more proactively
        if self.hunger <= 30:  # Changed from 20 to 30
            self.sleeping = False
            self.target = "food"
            self.move(self.env.width, self.env.height)
            return

        # Sleep behavior
        if self.sleeping:
            if not self.env.is_in_area(self.x, self.y, "sleeping"):
                self.target = "sleeping"
                self.color = (0, 255, 0)
                self.move(self.env.width, self.env.height)
            else:
                recovery_rate = 3 if self.hunger > 50 else 1
                self.energy = min(100, self.energy + recovery_rate)
                self.color = (100, 100, 255)
                
                if (self.energy >= self.wake_threshold or
                    self.hunger <= 30 or
                    self.health < 50):
                    self.sleeping = False
                    self.color = (0, 255, 0)
                    self.target = None
        
        # Check for sleep need
        elif self.energy <= self.rest_threshold and self.hunger > 30:
            self.sleeping = True
            self.target = "sleeping"
            self.color = (0, 255, 0)
            self.move(self.env.width, self.env.height)
        
        # Normal behavior
        else:
            if not self.carrying_food:
                self.color = (0, 255, 0)
            
            # Always try to move unless specifically sleeping in sleep area
            if not (self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping")):
                self.move(self.env.width, self.env.height)

            # Update egg laying cooldown
            if self.egg_laying_cooldown > 0:
                self.egg_laying_cooldown -= 1

            # Check egg laying conditions first
            if (not self.sleeping and not self.eating and 
                not self.egg and self.mature and 
                self.egg_laying_cooldown == 0 and  # Only if cooldown is complete
                self.happiness >= 70 and 
                self.energy >= 60 and    
                self.hunger >= 60):  
                
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
                        self.energy -= 50
                        new_egg = Egg(egg_x, egg_y, self.env)
                        self.env.eggs.append(new_egg)
                        self.env.grid[(egg_x, egg_y)] = new_egg
                        self.has_laid_egg = True  # Track current egg
                        self.egg_laying_cooldown = self.egg_laying_cooldown_max  # Start cooldown
                        self.target = None
                else:
                    # Move towards nursery if ready to lay egg
                    self.target = "nursery"
                    self.color = (255, 200, 0)  # Match egg color
                    return  # Return here to prioritize egg laying

            # Prioritize eating over moving bodies
            if not self.sleeping and not self.eating:
                nearby_entities = self.env.get_nearby_entities(self.x, self.y)
                found_food = False
                
                # First check if we can eat something adjacent
                if self.hunger < 70:
                    for entity in nearby_entities:
                        if isinstance(entity, Creature) and entity.dead and entity.food_value > 0:
                            dx = abs(self.x - entity.x)
                            dy = abs(self.y - entity.y)
                            if dx + dy == 1:  # Adjacent but not diagonal
                                if self.eat(entity):
                                    self.color = (255, 200, 0)
                                    found_food = True
                                    self.target = None
                                    self.carrying_food = False
                                    break
                
            # If we didn't find adjacent food to eat, look for dead creatures to move
            if not found_food:
                found_dead_creature = False
                
                # First check if we're currently carrying a dead creature
                if self.carrying_food and isinstance(self.target, Creature):
                    # Check if we're still adjacent to our target
                    if abs(self.x - self.target.x) + abs(self.y - self.target.y) == 1:
                        found_dead_creature = True
                    else:
                        # Lost contact with the dead creature we were carrying
                        self.carrying_food = False
                        self.target = None
                        self.color = (0, 255, 0)  # Reset color
                
                # Only look for new dead creatures if we're not already carrying one
                if not self.carrying_food:
                    for entity in nearby_entities:
                        if (isinstance(entity, Creature) and 
                            entity.dead and 
                            entity.food_value > 0 and 
                            not self.env.is_in_area(entity.x, entity.y, "food") and
                            not any(c.target == entity for c in self.env.creatures if c != self and not c.dead)):
                            # Check if adjacent to the dead creature
                            if abs(self.x - entity.x) + abs(self.y - entity.y) == 1:
                                self.target = entity
                                self.carrying_food = True
                                self.color = (200, 150, 50)  # Brown while carrying
                                found_dead_creature = True
                                break
                
                # Reset carrying_food if no dead creature is found nearby
                if not found_dead_creature and self.carrying_food:
                    self.carrying_food = False
                    self.target = None
                    self.color = (0, 255, 0)  # Reset color

            # Update happiness and visual state at the end
            self.happiness = self.calculate_happiness()
            self.update_visual_state()

    def update_visual_state(self):
        """Update the creature's visual appearance based on its state"""
        if self.dead:
            self.color = (255, 0, 0)  # Red for dead
            return

        # Start with base color
        r, g, b = self.base_color

        # Health indicator - reduce green as health decreases
        health_factor = self.health / 100
        g = int(g * health_factor)

        # Energy indicator - add blue tint when tired
        if self.energy < self.rest_threshold + 20 and not self.sleeping:
            b = min(255, b + int((1 - self.energy / 100) * 255))

        # Hunger indicator - add red tint when hungry
        if self.hunger < 50:
            r = min(255, r + int((1 - self.hunger / 100) * 255))

        # Special states override the gradual changes
        if self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping"):
            self.color = (100, 100, 255)  # Blue only when sleeping in sleep area
        elif self.eating:
            self.color = (255, 200, 0)    # Yellow while eating
        elif self.carrying_food:
            self.color = (200, 150, 50)   # Brown while carrying
        elif self.target == "nursery":
            self.color = (255, 200, 0)    # Changed to match egg color (was pink)
        else:
            self.color = (r, g, b)

    def lay_egg(self):
        """Lay an egg in the current position if in nursery"""
        if self.energy >= 90 and not self.egg:
            # Try to lay egg in current position
            if not self.env.is_position_occupied(self.x, self.y + 1):
                self.energy -= 90
                new_egg = Egg(self.x, self.y + 1, self.env)
                self.env.eggs.append(new_egg)
                self.env.grid[(self.x, self.y + 1)] = new_egg
                self.has_laid_egg = True
            elif not self.env.is_position_occupied(self.x + 1, self.y):
                self.energy -= 90
                new_egg = Egg(self.x + 1, self.y, self.env)
                self.env.eggs.append(new_egg)
                self.env.grid[(self.x + 1, self.y)] = new_egg
                self.has_laid_egg = True

    def die(self):
        """Mark the creature as dead instead of removing it."""
        self.dead = True
        self.color = (255, 0, 0)  # Red color for dead creatures
        self.health = 0
        self.food_value = 200  # Doubled from 100 to 200 - dead creatures provide more food
        
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
Remaining Food: {self.food_value/2}%
Position: ({self.x}, {self.y})"""
<<<<<<< HEAD
=======
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
                # Set eating state
                self.eating = True
                self.target = None  # Clear any other targets
                
                # Process the eating action
                food_amount = min(40, food_source.food_value)
                food_source.food_value -= food_amount
                self.hunger = min(100, self.hunger + food_amount * 1.5)
                self.color = (255, 200, 0)  # Yellow while eating
                
                # Don't reset eating state here - let update() handle it
                return True
        return False

    def draw(self, batch):
        shapes = []
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        base_radius = GRID_SIZE // 2

        # Calculate breathing effect
        breath_amount = DEAD_BREATH_AMOUNT if self.dead else BREATH_AMOUNT
        # Use a smaller multiplier for the animation timer to slow down the breathing
        breath_scale = 1.0 + math.sin(self.animation_timer * BREATH_SPEED * math.pi + self.breath_offset) * breath_amount

        # Apply breathing to base_radius
        current_radius = base_radius * breath_scale

        # 1. Selection indicator (white ring, outermost)
        if self.selected:
            shapes.append(pyglet.shapes.Circle(
                center_x, center_y,
                current_radius + SELECTION_RING_SIZE,  # Apply breathing to selection ring
                color=(255, 255, 255, 180),
                batch=batch
            ))

        # 2. Critical status indicator (red ring)
        if not self.dead and (self.hunger < 30 or self.energy < 30 or self.health < 30):
            shapes.append(pyglet.shapes.Circle(
                center_x, center_y,
                current_radius + STATUS_RING_SIZE,  # Apply breathing to status ring
                color=(255, 0, 0, 200),
                batch=batch
            ))

        # 3. Main body
        if self.dead:
            # Base circle for dead creature
            shapes.append(pyglet.shapes.Circle(
                center_x, center_y,
                current_radius,  # Apply breathing
                color=(100, 0, 0),  # Dark red base
                batch=batch
            ))
            
            # Food value indicator (arc) with updated color scheme
            if self.food_value > 0:
                food_percentage = self.food_value / 200
                # Use a more muted green for the food indicator
                shapes.append(pyglet.shapes.Arc(
                    center_x, center_y,
                    current_radius * 0.8,  # Apply breathing to food indicator
                    color=(120, 150, 0),  # Muted green-brown color
                    batch=batch,
                    angle=food_percentage * 6.28319  # 2*pi for full circle
                ))
        else:
            # Living creature main body
            shapes.append(pyglet.shapes.Circle(
                center_x, center_y,
                current_radius,  # Apply breathing
                color=self.color,
                batch=batch
            ))

            # 4. Age indicator (inner circle)
            if self.mature:
                age_factor = self.age / self.max_age
                inner_radius = current_radius * INNER_CIRCLE_RATIO  # Apply breathing to inner circle
                
                # Color transitions from green to yellow to red with age
                if age_factor < 0.5:
                    # Young adult: green to yellow
                    green = 255
                    red = int(255 * (age_factor * 2))
                else:
                    # Elder: yellow to red
                    red = 255
                    green = int(255 * (2 - age_factor * 2))
                    
                shapes.append(pyglet.shapes.Circle(
                    center_x, center_y,
                    inner_radius,
                    color=(red, green, 0, 230),
                    batch=batch
                ))

        # Add status icons animation
        if not self.dead:
            # Only update animation if game is not paused (FPS > 0)
            if FPS > 0:  
                self.animation_timer += ICON_ANIMATION_SPEED
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.animation_frame = (self.animation_frame + 1) % 3

            icon_x = self.x * GRID_SIZE + GRID_SIZE // 2
            icon_y = self.y * GRID_SIZE + GRID_SIZE + ICON_OFFSET_Y

            # 1. Eating animation (highest priority - always show when eating)
            if self.eating:
                icon_color = (255, 200, 0, 255)
                if self.animation_frame == 0:
                    angle = 15
                elif self.animation_frame == 1:
                    angle = 0
                else:
                    angle = -15

                fork_height = ICON_SIZE
                fork_width = ICON_SIZE // 3
                
                cx = icon_x
                cy = icon_y
                
                rotated_rect = pyglet.shapes.Rectangle(
                    cx - fork_width//2,
                    cy - fork_height//2,
                    fork_width,
                    fork_height,
                    color=icon_color,
                    batch=batch
                )
                rotated_rect.rotation = angle
                shapes.append(rotated_rect)

            # 2. Hunger exclamation animation
            elif self.hunger < 30 and self.target == "food":
                y_offset = math.sin(self.animation_timer * 3) * 5  # Bobbing motion
                hungry_label = pyglet.text.Label(
                    "!",
                    font_name='Arial',
                    font_size=ICON_SIZE,
                    bold=True,
                    x=icon_x,
                    y=icon_y + y_offset,
                    anchor_x='center',
                    anchor_y='center',
                    color=(255, 100, 100, 255)
                )
                hungry_label.draw()

            # 3. Egg laying animation
            elif (not self.has_laid_egg and self.mature and 
                self.target == "nursery"):
                # Pulsing effect
                scale = 1 + math.sin(self.animation_timer * 3) * 0.2
                egg_size = ICON_SIZE // 2 * scale
                
                shapes.append(pyglet.shapes.Circle(
                    icon_x,
                    icon_y,
                    egg_size,
                    color=(255, 200, 0, 200),  # Match egg color
                    batch=batch
                ))

            # 4. Low energy animation
            elif self.energy < 30 and not self.eating and not (self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping")):
                # Flashing effect
                alpha = 255 if self.animation_frame < 2 else 180
                battery_width = ICON_SIZE
                battery_height = ICON_SIZE // 2
                
                # Battery outline
                shapes.append(pyglet.shapes.Rectangle(
                    icon_x - battery_width//2,
                    icon_y - battery_height//2,
                    battery_width,
                    battery_height,
                    color=(100, 100, 100, alpha),
                    batch=batch
                ))
                
                # Dynamic battery level
                battery_level = max(1, int((self.energy / 30) * (battery_width - 4)))
                shapes.append(pyglet.shapes.Rectangle(
                    icon_x - battery_width//2 + 2,
                    icon_y - battery_height//2 + 2,
                    battery_level,
                    battery_height - 4,
                    color=(255, 0, 0, alpha),
                    batch=batch
                ))

            # 5. Carrying food animation
            elif self.carrying_food:
                # Draw package icon
                package_size = ICON_SIZE // 2
                y_offset = math.sin(self.animation_timer * 3) * 3  # Slight bobbing

                # Package outline
                shapes.append(pyglet.shapes.Rectangle(
                    icon_x - package_size//2,
                    icon_y + y_offset - package_size//2,
                    package_size,
                    package_size,
                    color=(200, 150, 50),  # Brown color
                    batch=batch
                ))

                # Package cross lines
                shapes.append(pyglet.shapes.Line(
                    icon_x - package_size//2,
                    icon_y + y_offset,
                    icon_x + package_size//2,
                    icon_y + y_offset,
                    color=(150, 100, 0),
                    batch=batch
                ))
                shapes.append(pyglet.shapes.Line(
                    icon_x,
                    icon_y + y_offset - package_size//2,
                    icon_x,
                    icon_y + y_offset + package_size//2,
                    color=(150, 100, 0),
                    batch=batch
                ))

            # 6. Sleep animation
            elif self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping"):
                z_size = ICON_SIZE // 2
                for i in range(3):
                    if i <= self.animation_frame:
                        z_label = pyglet.text.Label(
                            "Z",
                            font_name='Arial',
                            font_size=z_size,
                            bold=True,
                            x=icon_x + (i * z_size//2),
                            y=icon_y + (i * z_size//2),
                            anchor_x='center',
                            anchor_y='center',
                            color=(200, 200, 255, 255)
                        )
                        z_label.draw()

            # 7. Happy animation (lowest priority)
            elif self.happiness > 80 and not self.sleeping:
                # Only update animation if game is not paused (FPS > 0)
                if FPS > 0:  
                    # Create a smooth circular motion
                    continuous_angle = (self.animation_timer * HEART_ANIMATION_SPEED + self.heart_animation_offset) % (2 * math.pi)
                    
                    # Create a smooth circular motion
                    x_offset = math.cos(continuous_angle) * 3
                    y_offset = math.sin(continuous_angle) * 3
                    
                    # Smooth opacity transition using the same angle
                    opacity = int(180 + 75 * math.sin(continuous_angle))
                    
                    heart_label = pyglet.text.Label(
                        "♥",
                        font_name='Arial',
                        font_size=ICON_SIZE // 2,
                        x=icon_x + x_offset,
                        y=icon_y + y_offset,
                        anchor_x='center',
                        anchor_y='center',
                        color=(255, 150, 150, opacity)
                    )
                    heart_label.draw()

        # Add eyes after the main creature body is drawn
        if not isinstance(self.color, str):  # Make sure we have a valid color
            center_x = self.x * GRID_SIZE + GRID_SIZE // 2
            center_y = self.y * GRID_SIZE + GRID_SIZE // 2
            base_radius = GRID_SIZE // 2
            
            # Calculate eye positions
            left_eye_x = center_x - EYE_SPACING
            right_eye_x = center_x + EYE_SPACING
            eye_y = center_y + EYE_OFFSET_Y
            
            if self.dead:
                # Draw X eyes for dead creatures
                for eye_x in [left_eye_x, right_eye_x]:
                    # Draw X lines
                    shapes.extend([
                        pyglet.shapes.Line(
                            eye_x - EYE_SIZE, eye_y + EYE_SIZE,
                            eye_x + EYE_SIZE, eye_y - EYE_SIZE,
                            color=(0, 0, 0),
                            batch=batch,
                            width=2
                        ),
                        pyglet.shapes.Line(
                            eye_x - EYE_SIZE, eye_y - EYE_SIZE,
                            eye_x + EYE_SIZE, eye_y + EYE_SIZE,
                            color=(0, 0, 0),
                            batch=batch,
                            width=2
                        )
                    ])
            else:
                # Draw normal eyes
                for eye_x in [left_eye_x, right_eye_x]:
                    if self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping"):
                        # Draw closed eyes (horizontal lines) only when actually sleeping in the sleeping area
                        shapes.append(
                            pyglet.shapes.Line(
                                eye_x - EYE_SIZE, eye_y,
                                eye_x + EYE_SIZE, eye_y,
                                color=(0, 0, 0),
                                batch=batch,
                                width=2
                            )
                        )
                    elif self.is_blinking:
                        # Draw blinking eyes (shorter horizontal lines, similar to sleeping)
                        shapes.append(
                            pyglet.shapes.Line(
                                eye_x - EYE_SIZE, eye_y,
                                eye_x + EYE_SIZE, eye_y,
                                color=(0, 0, 0),
                                batch=batch,
                                width=2
                            )
                        )
                    else:
                        # Draw open eyes (white background with black pupil)
                        shapes.append(
                            pyglet.shapes.Circle(
                                eye_x, eye_y,
                                EYE_SIZE + 2,  # Larger white area
                                color=(255, 255, 255),
                                batch=batch
                            )
                        )
                        
                        # Calculate pupil offset based on target or movement direction
                        pupil_offset_x = 0
                        pupil_offset_y = 0
                        
                        if self.target:
                            if isinstance(self.target, (Creature, Egg)):
                                # Look at target creature/egg
                                dx = self.target.x - self.x
                                dy = self.target.y - self.y
                            elif self.target in ["sleeping", "nursery", "food"]:
                                # Look towards area center
                                center = self.env.get_area_center(self.target)
                                dx = (center[0] / GRID_SIZE) - self.x
                                dy = (center[1] / GRID_SIZE) - self.y
                            else:
                                dx = dy = 0
                            
                            # Normalize direction to maximum pupil range
                            if dx != 0 or dy != 0:
                                magnitude = (dx * dx + dy * dy) ** 0.5
                                pupil_offset_x = (dx / magnitude) * PUPIL_RANGE
                                pupil_offset_y = (dy / magnitude) * PUPIL_RANGE
                        
                        # Draw pupil with offset
                        shapes.append(
                            pyglet.shapes.Circle(
                                eye_x + pupil_offset_x,
                                eye_y + pupil_offset_y,
                                PUPIL_SIZE,
                                color=(0, 0, 0),
                                batch=batch
                            )
                        )
    
        # Draw antennae
        # Only living creatures have antennae
        if not self.dead:
            # Calculate base positions for antennae
            antenna_base_y = center_y + base_radius - 2  # Slightly below top of head
            left_base_x = center_x - ANTENNA_SPACING // 2
            right_base_x = center_x + ANTENNA_SPACING // 2

            # Calculate wave effect
            wave = math.sin(self.animation_timer * ANTENNA_WAVE_SPEED) * ANTENNA_WAVE_AMOUNT
            # Add extra wave when moving or targeting
            if self.target or self.carrying_food:
                wave *= 1.5  # More movement when active

            # Draw left antenna
            left_tip_x = left_base_x - math.sin(wave) * ANTENNA_LENGTH
            left_tip_y = antenna_base_y + math.cos(wave) * ANTENNA_LENGTH
            shapes.append(pyglet.shapes.Line(
                left_base_x, antenna_base_y,
                left_tip_x, left_tip_y,
                width=ANTENNA_WIDTH,
                color=self.color if not isinstance(self.color, str) else (0, 255, 0),
                batch=batch
            ))

            # Draw right antenna
            right_tip_x = right_base_x + math.sin(wave) * ANTENNA_LENGTH
            right_tip_y = antenna_base_y + math.cos(wave) * ANTENNA_LENGTH
            shapes.append(pyglet.shapes.Line(
                right_base_x, antenna_base_y,
                right_tip_x, right_tip_y,
                width=ANTENNA_WIDTH,
                color=self.color if not isinstance(self.color, str) else (0, 255, 0),
                batch=batch
            ))

            # Draw small dots at antenna tips
            tip_size = ANTENNA_WIDTH // 2
            shapes.extend([
                pyglet.shapes.Circle(
                    left_tip_x, left_tip_y,
                    tip_size,
                    color=self.color if not isinstance(self.color, str) else (0, 255, 0),
                    batch=batch
                ),
                pyglet.shapes.Circle(
                    right_tip_x, right_tip_y,
                    tip_size,
                    color=self.color if not isinstance(self.color, str) else (0, 255, 0),
                    batch=batch
                )
            ])
        else:
            # Dead creature antennae (drooping and darker color)
            antenna_base_y = center_y + base_radius - 2
            left_base_x = center_x - ANTENNA_SPACING // 2
            right_base_x = center_x + ANTENNA_SPACING // 2

            # Calculate drooping effect for dead antennae
            droop_angle = -math.pi / 4  # 45 degrees downward

            # Draw left antenna (drooping)
            left_tip_x = left_base_x - math.cos(droop_angle) * ANTENNA_LENGTH
            left_tip_y = antenna_base_y - math.sin(droop_angle) * ANTENNA_LENGTH
            shapes.append(pyglet.shapes.Line(
                left_base_x, antenna_base_y,
                left_tip_x, left_tip_y,
                width=ANTENNA_WIDTH,
                color=(80, 0, 0),  # Darker red for dead creature
                batch=batch
            ))

            # Draw right antenna (drooping)
            right_tip_x = right_base_x + math.cos(droop_angle) * ANTENNA_LENGTH
            right_tip_y = antenna_base_y - math.sin(droop_angle) * ANTENNA_LENGTH
            shapes.append(pyglet.shapes.Line(
                right_base_x, antenna_base_y,
                right_tip_x, right_tip_y,
                width=ANTENNA_WIDTH,
                color=(80, 0, 0),  # Darker red for dead creature
                batch=batch
            ))

            # Draw small dots at antenna tips (darker for dead)
            tip_size = ANTENNA_WIDTH // 2
            shapes.extend([
                pyglet.shapes.Circle(
                    left_tip_x, left_tip_y,
                    tip_size,
                    color=(80, 0, 0),  # Darker red for dead creature
                    batch=batch
                ),
                pyglet.shapes.Circle(
                    right_tip_x, right_tip_y,
                    tip_size,
                    color=(80, 0, 0),  # Darker red for dead creature
                    batch=batch
                )
            ])

        # Add this after drawing the main body but before status icons
        if not self.dead:
            # Calculate mouth position
            mouth_x = center_x
            mouth_y = center_y + MOUTH_Y_OFFSET
            
            if self.eating:
                # Open mouth for eating
                shapes.append(pyglet.shapes.Rectangle(
                    mouth_x - MOUTH_WIDTH//2,
                    mouth_y - self.mouth_open_amount//2,
                    MOUTH_WIDTH,
                    self.mouth_open_amount,
                    color=(0, 0, 0),
                    batch=batch
                ))
                
                # Mouth outline
                shapes.append(pyglet.shapes.BorderedRectangle(
                    mouth_x - MOUTH_WIDTH//2,
                    mouth_y - self.mouth_open_amount//2,
                    MOUTH_WIDTH,
                    self.mouth_open_amount,
                    border=1,
                    color=(0, 0, 0),
                    border_color=(50, 50, 50),
                    batch=batch
                ))
            else:
                # Different mouth expressions based on state
                points = []
                
                if self.health < 30 or self.hunger < 30 or self.energy < 30:
                    # Worried/concerned expression (inverted curve)
                    points = [
                        (mouth_x - MOUTH_WIDTH//2, mouth_y),
                        (mouth_x, mouth_y + SMILE_CURVE),
                        (mouth_x + MOUTH_WIDTH//2, mouth_y)
                    ]
                elif self.happiness > 80:
                    # Happy smile (curved down)
                    points = [
                        (mouth_x - MOUTH_WIDTH//2, mouth_y),
                        (mouth_x, mouth_y - SMILE_CURVE),
                        (mouth_x + MOUTH_WIDTH//2, mouth_y)
                    ]
                else:
                    # Neutral expression (straight line)
                    points = [
                        (mouth_x - MOUTH_WIDTH//2, mouth_y),
                        (mouth_x, mouth_y),
                        (mouth_x + MOUTH_WIDTH//2, mouth_y)
                    ]
                
                # Draw the mouth curve
                shapes.append(pyglet.shapes.Line(
                    points[0][0], points[0][1],
                    points[1][0], points[1][1],
                    color=(0, 0, 0),
                    batch=batch,
                    width=2
                ))
                shapes.append(pyglet.shapes.Line(
                    points[1][0], points[1][1],
                    points[2][0], points[2][1],
                    color=(0, 0, 0),
                    batch=batch,
                    width=2
                ))
        else:
            # Straight line for dead creatures
            mouth_x = center_x
            mouth_y = center_y + MOUTH_Y_OFFSET
            
            shapes.append(pyglet.shapes.Line(
                mouth_x - MOUTH_WIDTH//2, mouth_y,
                mouth_x + MOUTH_WIDTH//2, mouth_y,
                color=(50, 0, 0),
                batch=batch,
                width=2
            ))

        return shapes

    def update_eyes(self):
        """Update eye animation state"""
        if not self.dead and not (self.sleeping and self.env.is_in_area(self.x, self.y, "sleeping")):
            self.blink_timer -= 1  # Decrement by 1 frame instead of 1/60
            if self.blink_timer <= 0:
                if not self.is_blinking:
                    self.is_blinking = True
                    self.blink_timer = BLINK_DURATION
                else:
                    self.is_blinking = False
                    self.blink_timer = BLINK_INTERVAL + random.randint(-2, 2)  # Add some randomness

    def update_mouth(self):
        """Update mouth animation state"""
        if self.dead:
            # Dead creatures have a static slightly open mouth
            self.mouth_open_amount = 2
            return
        
        if self.eating:
            # Chewing animation
            self.is_chewing = True
            self.chew_timer += MOUTH_OPEN_SPEED
            self.target_mouth_open = (math.sin(self.chew_timer * 4) * 0.5 + 0.5) * MAX_MOUTH_OPEN
        elif self.sleeping:
            # Slightly open mouth when sleeping (breathing)
            self.target_mouth_open = 2 + math.sin(self.animation_timer) * 1
        else:
            # Normal state - occasional mouth movements
            if random.random() < 0.01:  # Random chance to open/close mouth
                self.target_mouth_open = random.uniform(0, 3)
        
        # Smoothly animate towards target
        if self.mouth_open_amount < self.target_mouth_open:
            self.mouth_open_amount = min(self.mouth_open_amount + MOUTH_OPEN_SPEED, self.target_mouth_open)
        elif self.mouth_open_amount > self.target_mouth_open:
            self.mouth_open_amount = max(self.mouth_open_amount - MOUTH_OPEN_SPEED, self.target_mouth_open)
<<<<<<< HEAD
>>>>>>> parent of fd846d1 (Added creature textures and patterns. Updated Todo list.)
=======
>>>>>>> parent of fd846d1 (Added creature textures and patterns. Updated Todo list.)

# The environment where creatures live
class Environment:
    def __init__(self, width, height):
        # Adjust width to account for sidebar
        self.width = (WIDTH - SIDEBAR_WIDTH) // GRID_SIZE  # Use adjusted width
        self.height = height
        # Pass self (environment) to creature constructor
        self.creatures = [
            Creature(random.randint(0, self.width-1), 
                    random.randint(0, self.height-1),
                    self)  # Pass self here
        ]
        
        self.eggs = []  # List to track eggs
        self.grid = {}  # Add a grid to track occupied positions
        # Add initial creatures to the grid
        for creature in self.creatures:
            self.grid[(creature.x, creature.y)] = creature
            
        self.creatures_to_remove = []  # Track creatures to remove after being eaten
        self.cell_size = GRID_SIZE * 2  # Size of each partition cell
        self.spatial_grid = {}  # Spatial partitioning grid
        self.sleeping_area_scale = 1.0
        self.food_area_scale = 1.0
        self.nursery_area_scale = 1.0
        
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
        global selected_egg  # Add this line to modify the global variable

        self.update_area_scales()
        
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
            else:
                # Remove dead creatures with no food value
                if creature.food_value <= 0:
                    self.creatures_to_remove.append(creature)
        
        # Update eggs
        for egg in self.eggs[:]:  # Create a copy of the list to safely modify it
            egg.update()
            if egg.ready_to_hatch:
                # Unselect the egg if it is selected
                if selected_egg == egg:
                    selected_egg.selected = False
                    selected_egg = None

                # Create new creature at egg's position
                new_creature = Creature(egg.x, egg.y, self)
                self.creatures.append(new_creature)
                self.grid[(egg.x, egg.y)] = new_creature
                # Remove the hatched egg
                self.eggs.remove(egg)
                self.grid.pop((egg.x, egg.y), None)
        
        # Remove creatures marked for removal
        self.creatures = [c for c in self.creatures if c not in self.creatures_to_remove]
        self.creatures_to_remove.clear()

    def draw(self, screen):
        batch = pyglet.graphics.Batch()
        shapes = []
        
        # Draw colony areas first
        areas = [
            ("food", FOOD_STORAGE_RADIUS * self.food_area_scale, (100, 50, 50), "Food Zone"),
            ("nursery", NURSERY_RADIUS * self.nursery_area_scale, (50, 100, 50), "Nursery Zone"),
            ("sleeping", SLEEPING_RADIUS * self.sleeping_area_scale, (50, 50, 100), "Sleeping Zone")
        ]

        for area_type, radius, color, label in areas:
            center = self.get_area_center(area_type)
            
            # Explicitly unpack RGB values and set very low opacity
            r, g, b = color
            # Draw very transparent circle for the zone
            zone_circle = pyglet.shapes.Circle(
                center[0], center[1], radius,
                color=(r, g, b, 20),  # Even more transparent (alpha=20)
                batch=batch
            )
            shapes.append(zone_circle)
            
            # Draw subtle border for the zone
            border_circle = pyglet.shapes.Circle(
                center[0], center[1], radius + 2,
                color=(255, 255, 255, 30),
                batch=batch
            )
            shapes.append(border_circle)
            
            # Calculate label position, ensuring it stays within window bounds
            label_x = min(max(center[0], 100), WIDTH - SIDEBAR_WIDTH - 100)
            label_y = min(max(center[1] - radius - 25, 30), HEIGHT - 30)
            
            # Draw label with semi-transparent background
            label_width = len(label) * 8
            pyglet.shapes.Rectangle(
                label_x - label_width/2 - 5,
                label_y - 10,
                label_width + 10,
                20,
                color=(0, 0, 0, 100)
            ).draw()
            
            # Draw the text
            pyglet.text.Label(
                label,
                font_name='Arial',
                font_size=14,
                bold=True,
                x=label_x,
                y=label_y,
                anchor_x='center',
                anchor_y='center',
                color=(255, 255, 255, 200)
            ).draw()

        # Draw eggs
        for egg in self.eggs:
            shapes.extend(egg.draw(batch))  # Ensure this line is calling the draw method

        # Draw creatures using their new draw method
        for creature in self.creatures:
            shapes.extend(creature.draw(batch))

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
        """Get the center coordinates for different colony areas with fixed positions"""
        if area_type == "food":
            # Food storage in bottom-left quadrant
            return (NEST_CENTER_X - QUADRANT_OFFSET, NEST_CENTER_Y - QUADRANT_OFFSET)
        elif area_type == "nursery":
            # Nursery in top-right quadrant
            return (NEST_CENTER_X + QUADRANT_OFFSET, NEST_CENTER_Y + QUADRANT_OFFSET)
        elif area_type == "sleeping":
            # Sleeping area in bottom-right quadrant
            return (NEST_CENTER_X + QUADRANT_OFFSET, NEST_CENTER_Y - QUADRANT_OFFSET)
        return (NEST_CENTER_X, NEST_CENTER_Y)

    def is_in_area(self, x, y, area_type):
        """Check if position is within a specific colony area"""
        # Convert grid coordinates to pixel coordinates for center calculation
        px = x * GRID_SIZE + GRID_SIZE // 2
        py = y * GRID_SIZE + GRID_SIZE // 2
        
        center = self.get_area_center(area_type)
        distance = ((px - center[0])**2 + (py - center[1])**2)**0.5
        
        # Scale only affects the radius, not the center position
        if area_type == "food":
            return distance <= FOOD_STORAGE_RADIUS * self.food_area_scale
        elif area_type == "nursery":
            return distance <= NURSERY_RADIUS * self.nursery_area_scale
        elif area_type == "sleeping":
            return distance <= SLEEPING_RADIUS * self.sleeping_area_scale
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
        """Try to move entity towards target, handling collisions and obstacles"""
        if entity.dead:
            return False

        # Calculate movement towards target
        dx = target_x - entity.x
        dy = target_y - entity.y
        
        # If already at target, no need to move
        if dx == 0 and dy == 0:
            return True

        # Get all possible moves, ordered by priority
        possible_moves = []
        
        # Direct moves (primary direction)
        if abs(dx) > abs(dy):
            # Prioritize horizontal movement
            if dx != 0:
                possible_moves.append((dx // abs(dx), 0))  # Horizontal
                if dy != 0:
                    possible_moves.append((dx // abs(dx), dy // abs(dy)))  # Diagonal
                    possible_moves.append((0, dy // abs(dy)))  # Vertical
            else:
                possible_moves.append((0, dy // abs(dy)))  # Vertical
        else:
            # Prioritize vertical movement
            if dy != 0:
                possible_moves.append((0, dy // abs(dy)))  # Vertical
                if dx != 0:
                    possible_moves.append((dx // abs(dx), dy // abs(dy)))  # Diagonal
                    possible_moves.append((dx // abs(dx), 0))  # Horizontal
            else:
                possible_moves.append((dx // abs(dx), 0))  # Horizontal

        # Add alternative moves for obstacle avoidance
        if dx != 0:
            possible_moves.append((dx // abs(dx), 1))   # Side step up
            possible_moves.append((dx // abs(dx), -1))  # Side step down
        if dy != 0:
            possible_moves.append((1, dy // abs(dy)))   # Side step right
            possible_moves.append((-1, dy // abs(dy)))  # Side step left

        # Add perpendicular moves as last resort
        possible_moves.extend([
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Cardinal directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal directions
        ])

        # If carrying a dead creature, handle special movement
        if entity.carrying_food and isinstance(entity.target, Creature):
            dead_creature = entity.target
            
            # Check if we're adjacent to the dead creature
            if abs(entity.x - dead_creature.x) + abs(entity.y - dead_creature.y) > 1:
                # Lost contact with dead creature, drop it
                entity.carrying_food = False
                entity.target = None
                return False

            # Try each possible move
            for move_x, move_y in possible_moves:
                new_carrier_x = entity.x + move_x
                new_carrier_y = entity.y + move_y
                
                if not (self.is_valid_position(new_carrier_x, new_carrier_y) and
                       not self.is_position_occupied(new_carrier_x, new_carrier_y)):
                    continue
                
                # Find best position for dead creature
                best_dead_pos = None
                min_distance = float('inf')
                
                # Check all adjacent positions for the dead creature
                for dead_dx, dead_dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_dead_x = new_carrier_x + dead_dx
                    new_dead_y = new_carrier_y + dead_dy
                    
                    if (self.is_valid_position(new_dead_x, new_dead_y) and
                        not self.is_position_occupied(new_dead_x, new_dead_y)):
                        # Calculate distance to target considering both positions
                        dist = (abs(new_dead_x - target_x) + abs(new_dead_y - target_y) +
                               abs(new_carrier_x - target_x) + abs(new_carrier_y - target_y))
                        if dist < min_distance:
                            min_distance = dist
                            best_dead_pos = (new_dead_x, new_dead_y)
                
                # If we found valid positions for both, move them
                if best_dead_pos is not None:
                    # Remove both entities from their current positions
                    self.grid.pop((entity.x, entity.y), None)
                    self.grid.pop((dead_creature.x, dead_creature.y), None)
                    
                    # Update positions
                    entity.x = new_carrier_x
                    entity.y = new_carrier_y
                    dead_creature.x = best_dead_pos[0]
                    dead_creature.y = best_dead_pos[1]
                    
                    # Add both entities back to grid at their new positions
                    self.grid[(entity.x, entity.y)] = entity
                    self.grid[(dead_creature.x, dead_creature.y)] = dead_creature
                    
                    return True
            
            return False

        # Normal movement for non-carrying entities
        # Try each possible move in order of priority
        for move_x, move_y in possible_moves:
            new_x = entity.x + move_x
            new_y = entity.y + move_y
            
            if (self.is_valid_position(new_x, new_y) and
                not self.is_position_occupied(new_x, new_y)):
                return self.move_entity(entity, new_x, new_y)
        
        return False

    def try_move_dead_creature(self, dead_creature):
        """Remove this method or make it do nothing since dead creatures shouldn't move"""
        return False

    def is_valid_position(self, x, y):
        """Check if a position is within bounds and not behind the sidebar"""
        return 0 <= x < self.width - (SIDEBAR_WIDTH // GRID_SIZE) and 0 <= y < self.height

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

    def update_area_scales(self):
        """Update the scales of the areas based on specific needs"""
        num_creatures = len(self.creatures)
        num_dead = sum(1 for c in self.creatures if c.dead)
        num_eggs = len(self.eggs)
        
        # Calculate scales based on different needs
        sleeping_need = num_creatures
        food_need = num_dead
        nursery_need = num_eggs
        
        # Calculate base scales (more conservative maximum to prevent touching)
        max_scale = 1.5  # Ensure zones do not touch
        
        # Base scale is 1.0, maximum scale prevents touching
        self.sleeping_area_scale = min(max_scale, 1.0 + (sleeping_need / max(1, num_creatures)) * 0.3)
        self.food_area_scale = min(max_scale, 1.0 + (food_need / max(1, num_creatures)) * 0.3)
        self.nursery_area_scale = min(max_scale, 1.0 + (nursery_need / max(1, num_creatures)) * 0.3)

# The egg class to handle egg incubation
class Egg:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.env = environment
        self.timer = 0
        self.hatch_time = 300  # Increased from 100 to 300 for slower hatching
        self.selected = False
        self.ready_to_hatch = False

    def update(self):
        """Increment the egg's timer and check if ready to hatch."""
        if self.timer < self.hatch_time:
            self.timer += 1  # Increment by 1 per frame
        
        if self.timer >= self.hatch_time and not self.ready_to_hatch:
            # Reset egg laying status for all nearby creatures
            nearby_creatures = [
                creature for creature in self.env.creatures
                if abs(creature.x - self.x) + abs(creature.y - self.y) <= 3  # Within 3 tiles
                and creature.has_laid_egg
            ]
            for creature in nearby_creatures:
                creature.has_laid_egg = False  # Allow them to lay eggs again
            self.ready_to_hatch = True

    def __str__(self):
        """Return the egg's incubation progress as a percentage, capped at 100%"""
        progress = min(100, int((self.timer/300) * 100))
        return f"Egg Timer: {progress}%"

    def draw(self, batch):
        """Draw the egg with improved visuals and animations"""
        shapes = []
        
        # Calculate center position
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        base_radius = GRID_SIZE // 3
        
        # Calculate pulse effect
        pulse = math.sin(self.timer * EGG_PULSE_SPEED * math.pi / 300) * 0.1
        current_radius = base_radius * (1 + pulse)
        
        # Selection indicator (if selected)
        if self.selected:
            shapes.append(pyglet.shapes.Circle(
                center_x, center_y,
                current_radius + 4,
                color=(255, 255, 255, 128),
                batch=batch
            ))
        
        # Main egg shape (outer)
        shapes.append(pyglet.shapes.Circle(
            center_x, center_y,
            current_radius,
            color=(255, 200, 0),
            batch=batch
        ))
        
        # Inner egg shape (darker)
        shapes.append(pyglet.shapes.Circle(
            center_x, center_y,
            current_radius * EGG_INNER_RATIO,
            color=(230, 180, 0),
            batch=batch
        ))
        
        # Add shine effect (small white circle in upper-right)
        shine_x = center_x + current_radius * EGG_SHINE_OFFSET
        shine_y = center_y + current_radius * EGG_SHINE_OFFSET
        shapes.append(pyglet.shapes.Circle(
            shine_x, shine_y,
            current_radius * 0.2,
            color=(255, 255, 255, 180),
            batch=batch
        ))
        
        # Progress indicator (arc around the egg)
        if self.timer > 0:
            progress = min(self.timer / 300, 1.0)
            shapes.append(pyglet.shapes.Arc(
                center_x, center_y,
                current_radius + 2,
                color=(255, 255, 255, 150),
                batch=batch,
                angle=progress * math.pi * 2  # Full circle is 2π radians
            ))
        
        return shapes

# Handle mouse clicks
selected_creature = None  # No creature is selected initially
selected_egg = None  # No egg is selected initially

@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected_creature, selected_egg, current_speed_state
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
        # Calculate button dimensions (use original size * scale)
        button_width = 38  # Fixed width for hit detection
        button_height = 38  # Fixed height for hit detection
        
        # Pause button
        pause_area = {
            'x1': pause_button.x,
            'x2': pause_button.x + button_width,
            'y1': pause_button.y,
            'y2': pause_button.y + button_height
        }
        
        # Pause button
        if (pause_area['x1'] <= x <= pause_area['x2'] and 
            pause_area['y1'] <= y <= pause_area['y2']):
            if current_speed_state != "pause":
                current_speed_state = "pause"
                update_fps(0)  # Pause
                pause_button.image = pause_clicked_image
                play_button.image = play_unclicked_image
                fast_forward_button.image = fast_forward_unclicked_image
        
        # Play button
        elif (play_button.x <= x <= play_button.x + button_width and 
              play_button.y <= y <= play_button.y + button_height):
            if current_speed_state != "play":
                current_speed_state = "play"
                update_fps(1)  # Normal speed
                play_button.image = play_clicked_image
                pause_button.image = pause_unclicked_image
                fast_forward_button.image = fast_forward_unclicked_image
        
        # Fast forward button
        elif (fast_forward_button.x <= x <= fast_forward_button.x + button_width and 
              fast_forward_button.y <= y <= fast_forward_button.y + button_height):
            if current_speed_state != "fast":
                current_speed_state = "fast"
                update_fps(20)  # Fast speed
                fast_forward_button.image = fast_forward_clicked_image
                pause_button.image = pause_unclicked_image
                play_button.image = play_unclicked_image

def update_fps(new_fps):
    """Update the FPS and reschedule the update function"""
    global FPS
    FPS = new_fps
    pyglet.clock.unschedule(update)
    if FPS > 0:  # Only schedule if FPS is greater than 0
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
        stats_label.text = f"Selected Egg:\nIncubation: {int((selected_egg.timer/300) * 100)}%\nPosition: ({selected_egg.x}, {selected_egg.y})"
    else:
        stats_label.text = "No creature or egg selected"

# Create the environment with only one creature
env = Environment((WIDTH - SIDEBAR_WIDTH) // GRID_SIZE, HEIGHT // GRID_SIZE)

# Update the legend labels to include groups and headers
legend_labels = [
    # Group 1: Basic States
    ("Basic States", "header"),
    ("Normal Creature", (0, 255, 0)),
    ("Dead Creature (with food)", "dead_with_food"),
    ("Dead Creature (depleted)", (100, 0, 0)),
    ("Waiting for Egg to Hatch", (255, 200, 0)),
    
    # Group 2: Age Indicators
    ("Age Indicators", "header"),
    ("Young Adult (green core)", "young_adult"),
    ("Middle Age (yellow core)", "middle_age"),
    ("Elder (red core)", "elder"),
    
    # Group 3: Status Indicators
    ("Status Indicators", "header"),
    ("Selected (white ring)", "selected"),
    ("Critical Status (red ring)", "critical"),
    ("Sleeping", (100, 100, 255)),
    ("Carrying Food", (200, 150, 50)),
    ("Ready to Lay Egg", (255, 200, 0))  # Changed to match egg color
]

# Initialize the stats bars
stats_bars = {
    'age': LoadingBar(
        WIDTH - SIDEBAR_WIDTH + 15,
        stats_panel.y + stats_panel.height - 140,
        LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT,
        "Age", (255, 200, 50)  # Yellow color for age bar
    ),
    'health': LoadingBar(
        WIDTH - SIDEBAR_WIDTH + 15,
        stats_panel.y + stats_panel.height - 160,
        LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT,
        "Health", LOADING_BAR_COLORS['health']
    ),
    'energy': LoadingBar(
        WIDTH - SIDEBAR_WIDTH + 15,
        stats_panel.y + stats_panel.height - 180,
        LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT,
        "Energy", LOADING_BAR_COLORS['energy']
    ),
    'hunger': LoadingBar(
        WIDTH - SIDEBAR_WIDTH + 15,
        stats_panel.y + stats_panel.height - 200,
        LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT,
        "Hunger", LOADING_BAR_COLORS['hunger']
    ),
    'happiness': LoadingBar(
        WIDTH - SIDEBAR_WIDTH + 15,
        stats_panel.y + stats_panel.height - 220,
        LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT,
        "Happiness", LOADING_BAR_COLORS['happiness']
    )
}

def update_ui_positions():
    """Update all UI element positions with refined spacing"""
    # Calculate positions from top-right
    start_y = HEIGHT - TOP_MARGIN
    panel_x = WIDTH - SIDEBAR_WIDTH + 5
    panel_center_x = panel_x + (SIDEBAR_WIDTH // 2)  # Center point of panels
    
    # Control Panel (top)
    control_panel.update_position(panel_x, start_y - CONTROL_PANEL_HEIGHT)
    
    # Center buttons in control panel
    button_y = control_panel.y + 10
    total_buttons_width = (45 * 2) + 38  # 2 spaces between 3 buttons + button width
    first_button_x = panel_center_x - (total_buttons_width // 2)
    
    pause_button.x = first_button_x
    pause_button.y = button_y
    play_button.x = first_button_x + 45
    play_button.y = button_y
    fast_forward_button.x = first_button_x + 90
    fast_forward_button.y = button_y
    
    # Stats Panel (middle)
    stats_y = control_panel.y - PANEL_SPACING - STATS_PANEL_HEIGHT
    stats_panel.update_position(panel_x, stats_y)
    
    # Status section (icons) - moved higher in the panel
    status_y = stats_panel.y + STATS_PANEL_HEIGHT - 30
    
    # Center all bars with consistent spacing
    bar_spacing = 25  # Increased spacing between bars
    bar_start_y = status_y - 80  # Increased gap between icons and first bar
    bar_x = panel_center_x - (LOADING_BAR_WIDTH // 2)
    
    # Position all bars in sequence with consistent spacing
    age_percent = (selected_creature.age / selected_creature.max_age) * 100
    
    stats_bars['health'].update_position(bar_x, bar_start_y)
    stats_bars['energy'].update_position(bar_x, bar_start_y - bar_spacing)
    stats_bars['hunger'].update_position(bar_x, bar_start_y - (bar_spacing * 2))
    stats_bars['happiness'].update_position(bar_x, bar_start_y - (bar_spacing * 3))
    stats_bars['age'].update_value(age_percent, f"({selected_creature.age})")
    
    # Legend Panel (bottom) with more spacing
    legend_y = stats_y - (PANEL_SPACING * 2) - LEGEND_PANEL_HEIGHT
    legend_panel.update_position(panel_x, legend_y)

@window.event
def on_draw():
    window.clear()
    
    # Draw panels background area
    pyglet.shapes.Rectangle(
        WIDTH - SIDEBAR_WIDTH - TOP_MARGIN, 0, 
        SIDEBAR_WIDTH + TOP_MARGIN, HEIGHT,
        color=(30, 30, 30)
    ).draw()
    
    # Draw panels
    control_panel.draw()
    stats_panel.draw()
    legend_panel.draw()
    
    # Draw legend with adjusted starting position
    legend_start_y = legend_panel.y + legend_panel.height - LEGEND_TOP_PADDING
    y_offset = legend_start_y
    
    for label_text, color in legend_labels:
        if color == "header":
            # Add extra space before headers (except the first one)
            if y_offset < legend_start_y:
                y_offset -= LEGEND_GROUP_SPACING
            
            pyglet.text.Label(
                label_text,
                font_name='Arial',
                font_size=LEGEND_HEADER_SIZE,
                bold=True,
                x=WIDTH - SIDEBAR_WIDTH - TOP_MARGIN + 15,
                y=y_offset,
                anchor_x='left',
                anchor_y='center',
                color=(200, 200, 200, 255)
            ).draw()
            y_offset -= LEGEND_HEADER_SPACING
            continue
            
        # Draw indicators with refined positioning
        x_pos = WIDTH - SIDEBAR_WIDTH - TOP_MARGIN + 20 + LEGEND_ICON_SIZE//2
        if color == "dead_with_food":
            # Dead creature with food indicator
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=(100, 0, 0)).draw()
            # Draw green arc to show remaining food
            pyglet.shapes.Arc(x_pos, y_offset, 
                            LEGEND_ICON_SIZE//2 * 0.8,  # Slightly smaller radius
                            color=(120, 150, 0),  # Muted green-brown color
                            start_angle=0,  # Start from right
                            angle=4.71239,  # About 3/4 of a circle
                            batch=None).draw()
        elif color == "selected":
            # Selection indicator with creature inside
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 + 4, color=(255, 255, 255, 180)).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=(0, 255, 0)).draw()
            # Add inner circle to match actual creature appearance
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * INNER_CIRCLE_RATIO, 
                               color=(0, 255, 0, 230)).draw()
        elif color == "critical":
            # Critical status indicator with creature inside
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 + 2, color=(255, 0, 0, 200)).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=(0, 255, 0)).draw()
            # Add inner circle to match actual creature appearance
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * INNER_CIRCLE_RATIO, 
                               color=(0, 255, 0, 230)).draw()
        elif color in ["young_adult", "middle_age", "elder"]:
            # Age indicator examples with outer and inner circles
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=(0, 255, 0)).draw()
            # Different inner colors based on age
            if color == "young_adult":
                inner_color = (0, 255, 0)
            elif color == "middle_age":
                inner_color = (255, 255, 0)
            else:  # elder
                inner_color = (255, 0, 0)
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * INNER_CIRCLE_RATIO, 
                               color=inner_color + (230,)).draw()  # Add alpha channel
        elif isinstance(color, tuple):
            # Regular color indicators (sleeping, carrying food, etc.)
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=color).draw()
            # Add inner circle for consistency if it's a living creature color
            if color != (255, 200, 0):  # Not an egg
                pyglet.shapes.Circle(x_pos, y_offset, 
                                   LEGEND_ICON_SIZE//2 * INNER_CIRCLE_RATIO, 
                                   color=color + (230,)).draw()
        
        # Draw label with refined positioning
        label = pyglet.text.Label(
            label_text,
            font_name='Arial',
            font_size=LEGEND_TEXT_SIZE,
            x=WIDTH - SIDEBAR_WIDTH - TOP_MARGIN + 45,
            y=y_offset,
            width=SIDEBAR_WIDTH - 55,
            multiline=True,
            anchor_x='left',
            anchor_y='center'
        )
        label.draw()
        
        y_offset -= LEGEND_ITEM_SPACING
    
    env.draw(window)
    
    # Update and draw stats
    if selected_creature:
        if not selected_creature.dead:
            # Update loading bar values
            age_percent = (selected_creature.age / selected_creature.max_age) * 100
            stats_bars['age'].update_value(age_percent, f"({selected_creature.age})")  # Add age value
            stats_bars['health'].update_value(selected_creature.health)
            stats_bars['energy'].update_value(selected_creature.energy)
            stats_bars['hunger'].update_value(selected_creature.hunger)
            stats_bars['happiness'].update_value(selected_creature.happiness)
            
            # Draw loading bars
            for bar in stats_bars.values():
                bar.draw()
    
    pause_button.draw()
    play_button.draw()
    fast_forward_button.draw()
    
    # Draw status icons and bars for selected creature
    if selected_creature:
        if not selected_creature.dead:
            # Draw status icons at the top of stats panel
            icon_y = stats_panel.y + STATS_PANEL_HEIGHT - 60
            icon_spacing = 30
            icon_size = 16  # Standardized size for all icons
            
            # Calculate panel center x (same as in update_ui_positions)
            panel_x = WIDTH - SIDEBAR_WIDTH + 5
            panel_center_x = panel_x + (SIDEBAR_WIDTH // 2)
            
            # Calculate starting x position to center all icons
            num_possible_icons = 5  # Maximum number of icons that could appear
            total_width = (num_possible_icons - 1) * icon_spacing
            start_x = panel_center_x - (total_width // 2)

            # Draw status icons based on creature state
            if selected_creature.sleeping:
                # Draw Z's
                for i in range(3):
                    pyglet.text.Label(
                        "Z",
                        font_name='Arial',
                        font_size=icon_size,
                        bold=True,
                        x=start_x + (i * icon_size//2),
                        y=icon_y + (i * icon_size//2),
                        anchor_x='center',
                        anchor_y='center',
                        color=(200, 200, 255, 255)
                    ).draw()

            if selected_creature.eating:
                # Draw fork icon
                fork_height = icon_size
                fork_width = icon_size // 3
                
                rotated_rect = pyglet.shapes.Rectangle(
                    start_x + icon_spacing - fork_width//2,
                    icon_y - fork_height//2,
                    fork_width,
                    fork_height,
                    color=(255, 200, 0, 255)
                )
                rotated_rect.draw()

            if selected_creature.carrying_food:
                # Draw package icon
                package_size = icon_size
                
                # Package outline
                pyglet.shapes.Rectangle(
                    start_x + icon_spacing * 2 - package_size//2,
                    icon_y - package_size//2,
                    package_size,
                    package_size,
                    color=(200, 150, 50)
                ).draw()

                # Package cross lines
                pyglet.shapes.Line(
                    start_x + icon_spacing * 2 - package_size//2,
                    icon_y,
                    start_x + icon_spacing * 2 + package_size//2,
                    icon_y,
                    color=(150, 100, 0)
                ).draw()
                pyglet.shapes.Line(
                    start_x + icon_spacing * 2,
                    icon_y - package_size//2,
                    start_x + icon_spacing * 2,
                    icon_y + package_size//2,
                    color=(150, 100, 0)
                ).draw()

            if selected_creature.target == "nursery":
                # Draw egg icon
                egg_size = icon_size // 2
                pyglet.shapes.Circle(
                    start_x + icon_spacing * 3,
                    icon_y,
                    egg_size,
                    color=(255, 200, 0, 200)
                ).draw()

            if selected_creature.energy < 30:
                # Draw battery icon
                battery_width = icon_size
                battery_height = icon_size // 2
                
                # Battery outline
                pyglet.shapes.Rectangle(
                    start_x + icon_spacing * 4 - battery_width//2,
                    icon_y - battery_height//2,
                    battery_width,
                    battery_height,
                    color=(100, 100, 100, 255)
                ).draw()
                
                # Battery level
                battery_level = max(1, int((selected_creature.energy / 30) * (battery_width - 4)))
                pyglet.shapes.Rectangle(
                    start_x + icon_spacing * 4 - battery_width//2 + 2,
                    icon_y - battery_height//2 + 2,
                    battery_level,
                    battery_height - 4,
                    color=(255, 0, 0, 255)
                ).draw()

            # Update and draw loading bars
            age_percent = (selected_creature.age / selected_creature.max_age) * 100
            stats_bars['age'].update_value(age_percent, f"({selected_creature.age})")
            stats_bars['health'].update_value(selected_creature.health)
            stats_bars['energy'].update_value(selected_creature.energy)
            stats_bars['hunger'].update_value(selected_creature.hunger)
            stats_bars['happiness'].update_value(selected_creature.happiness)
            
            for bar in stats_bars.values():
                bar.draw()

# Initial UI position update
update_ui_positions()

# Update method (called on every frame)
def update(dt):
    env.update(dt)  # Update creatures and eggs
    update_stats()  # Update the stats each frame

# Make sure to schedule the initial update
if FPS > 0:
    pyglet.clock.schedule_interval(update, 1.0 / FPS)  # Add this line before pyglet.app.run()

# Run the pyglet application
pyglet.app.run()
