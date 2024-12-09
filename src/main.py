import pyglet
import random
import math
import time

from utils.constants import *

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

# Create the window with resizable=False and fixed size
window = pyglet.window.Window(WIDTH, HEIGHT, "Creature Simulation", resizable=False)

# Load images for buttons
pause_unclicked_image = pyglet.resource.image('assets/ui icons/pause-play-unclick.png')
pause_clicked_image = pyglet.resource.image('assets/ui icons/pause-play-click.png')

play_unclicked_image = pyglet.resource.image('assets/ui icons/play-button-unclick.png')
play_clicked_image = pyglet.resource.image('assets/ui icons/play-button-click.png')

fast_forward_unclicked_image = pyglet.resource.image('assets/ui icons/fast-forward-button-unclick.png')
fast_forward_clicked_image = pyglet.resource.image('assets/ui icons/fast-forward-button-click.png')

# Set scale factor
icon_scale = 0.075

# Create panels
control_panel = Panel(
    WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
    HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT,
    SIDEBAR_WIDTH,
    CONTROL_PANEL_HEIGHT,
    ""
)

stats_panel = Panel(
    WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
    HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT - PANEL_SPACING - STATS_PANEL_HEIGHT,
    SIDEBAR_WIDTH,
    STATS_PANEL_HEIGHT
)

legend_panel = Panel(
    WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
    HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT - PANEL_SPACING - 
    STATS_PANEL_HEIGHT - PANEL_SPACING - LEGEND_PANEL_HEIGHT,
    SIDEBAR_WIDTH,
    LEGEND_PANEL_HEIGHT,
    "Legend"
)

# Now create and position the buttons
button_width = pause_unclicked_image.width * icon_scale  # Width of scaled button
button_spacing = 20  # Space between buttons
total_buttons_width = (button_width * 3) + (button_spacing * 2)  # Total width needed

# Calculate starting x position to center the group of buttons within the control panel
start_x = WIDTH - SIDEBAR_WIDTH + (SIDEBAR_WIDTH - total_buttons_width - 30) // 2

# Calculate vertical center of the control panel
vertical_center = HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT//2

# Create sprites for buttons with proper positioning
pause_button = pyglet.sprite.Sprite(
    pause_clicked_image,
    x=start_x,
    y=vertical_center - (pause_clicked_image.height * icon_scale) // 2
)
pause_button.scale = icon_scale

play_button = pyglet.sprite.Sprite(
    play_unclicked_image,
    x=start_x + button_width + button_spacing,
    y=vertical_center - (play_unclicked_image.height * icon_scale) // 2
)
play_button.scale = icon_scale

fast_forward_button = pyglet.sprite.Sprite(
    fast_forward_unclicked_image,
    x=start_x + (button_width + button_spacing) * 2,
    y=vertical_center - (fast_forward_unclicked_image.height * icon_scale) // 2
)
fast_forward_button.scale = icon_scale

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
        
        # Add texture-related attributes
        self.pattern = random.choices(
            list(TEXTURE_PATTERNS.keys()),
            weights=[p["chance"] for p in TEXTURE_PATTERNS.values()]
        )[0]
        self.pattern_color = random.choice(PATTERN_COLORS)
        self.pattern_offset = random.uniform(0, 2 * math.pi)  # Random starting offset
        self.pattern_scale = random.uniform(0.8, 1.2)  # Random scale variation

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
        # Calculate common animation values once
        animation_sin = math.sin(self.animation_timer * 3)
        continuous_angle = (self.animation_timer * HEART_ANIMATION_SPEED + self.heart_animation_offset) % (2 * math.pi)
        
        # Use these values instead of recalculating throughout the method
        y_offset = animation_sin * 5  # For bobbing motion
        opacity = int(180 + 75 * animation_sin)  # For opacity transitions
        
        # Calculate common values once at the start
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        base_radius = GRID_SIZE // 2
        current_radius = base_radius * (1.0 + math.sin(self.animation_timer * BREATH_SPEED * math.pi + self.breath_offset) * (DEAD_BREATH_AMOUNT if self.dead else BREATH_AMOUNT))

        # Use these cached values throughout the method instead of recalculating
        shapes = []
        
        # Selection indicator
        if self.selected:
            shapes.append(pyglet.shapes.Circle(
                center_x, center_y,
                current_radius + SELECTION_RING_SIZE,
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

        # Add texture pattern after drawing main body but before other features
        if self.pattern != "plain":
            pattern_shapes = self.draw_pattern(center_x, center_y, current_radius, batch)
            shapes.extend(pattern_shapes)

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

    def draw_pattern(self, center_x, center_y, radius, batch):
        """Draw the creature's texture pattern"""
        shapes = []
        pattern_info = TEXTURE_PATTERNS[self.pattern]
        
        if self.pattern == "dots":
            dot_size = radius * 0.15 * self.pattern_scale
            for i in range(pattern_info["density"]):
                angle = (i / pattern_info["density"] * 2 * math.pi + self.pattern_offset) % (2 * math.pi)
                dist = radius * 0.6  # Keep dots within 60% of radius
                x = center_x + math.cos(angle) * dist
                y = center_y + math.sin(angle) * dist
                shapes.append(pyglet.shapes.Circle(
                    x, y, dot_size,
                    color=self.pattern_color,
                    batch=batch
                ))

        elif self.pattern == "stripes":
            stripe_width = radius * 0.15 * self.pattern_scale
            for i in range(pattern_info["density"]):
                angle = (i / pattern_info["density"] * math.pi + self.pattern_offset) % math.pi
                shapes.append(pyglet.shapes.Line(
                    center_x - radius * math.cos(angle),
                    center_y - radius * math.sin(angle),
                    center_x + radius * math.cos(angle),
                    center_y + radius * math.sin(angle),
                    width=stripe_width,
                    color=self.pattern_color,
                    batch=batch
                ))

        elif self.pattern == "spots":

            spot_size = radius * 0.25 * self.pattern_scale
            for i in range(pattern_info["density"]):
                angle = (i / pattern_info["density"] * 2 * math.pi + self.pattern_offset) % (2 * math.pi)
                dist = radius * random.uniform(0.2, 0.7)  # Random distance from center
                spot_x = center_x + math.cos(angle) * dist
                spot_y = center_y + math.sin(angle) * dist
                
                # Create a simpler circular spot instead of polygon
                shapes.append(pyglet.shapes.Circle(
                    spot_x, spot_y,
                    spot_size * random.uniform(0.8, 1.2),  # Random size variation
                    color=self.pattern_color,
                    batch=batch
                ))

        return shapes

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

    def update_spatial_grid(self):
        """Update the spatial grid with current positions of all entities."""
        self.spatial_grid.clear()
        for creature in self.creatures:
            cell_x, cell_y = self.get_cell(creature.x, creature.y)
            if (cell_x, cell_y) not in self.spatial_grid:
                self.spatial_grid[(cell_x, cell_y)] = []
            self.spatial_grid[(cell_x, cell_y)].append(creature)
        for egg in self.eggs:
            cell_x, cell_y = self.get_cell(egg.x, egg.y)
            if (cell_x, cell_y) not in self.spatial_grid:
                self.spatial_grid[(cell_x, cell_y)] = []
            self.spatial_grid[(cell_x, cell_y)].append(egg)

    def get_cell(self, x, y):
        """Get the cell coordinates for a given position."""
        return x // self.cell_size, y // self.cell_size

    def get_nearby_entities(self, x, y, radius=3):
        """Get entities in nearby cells."""
        nearby = []
        cell_x, cell_y = self.get_cell(x, y)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.spatial_grid:
                    nearby.extend(self.spatial_grid[cell])
        return nearby

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

        self.update_spatial_grid()  # Update spatial grid at the start of each update

    def draw(self, screen):
        batch = pyglet.graphics.Batch()
        shapes = []
        
        # Draw grid lines first (so they appear behind everything else)
        # Vertical lines
        for x in range(0, self.width + 1):
            x_pos = x * GRID_SIZE
            shapes.append(pyglet.shapes.Line(
                x_pos, 0,
                x_pos, self.height * GRID_SIZE,
                color=(50, 50, 50, 100),  # Dark grey with some transparency
                width=1,
                batch=batch
            ))
        
        # Horizontal lines
        for y in range(0, self.height + 1):
            y_pos = y * GRID_SIZE
            shapes.append(pyglet.shapes.Line(
                0, y_pos,
                self.width * GRID_SIZE, y_pos,
                color=(50, 50, 50, 100),  # Dark grey with some transparency
                width=1,
                batch=batch
            ))
        
        # Draw thicker lines every 5 cells for better readability
        for x in range(0, self.width + 1, 5):
            x_pos = x * GRID_SIZE
            shapes.append(pyglet.shapes.Line(
                x_pos, 0,
                x_pos, self.height * GRID_SIZE,
                color=(70, 70, 70, 150),  # Slightly darker and more opaque
                width=2,
                batch=batch
            ))
        
        for y in range(0, self.height + 1, 5):
            y_pos = y * GRID_SIZE
            shapes.append(pyglet.shapes.Line(
                0, y_pos,
                self.width * GRID_SIZE, y_pos,
                color=(70, 70, 70, 150),  # Slightly darker and more opaque
                width=2,
                batch=batch
            ))
        
        # Draw colony areas first with improved visuals
        areas = [
            ("food", FOOD_STORAGE_RADIUS * self.food_area_scale, (150, 80, 50), "Food Zone", 
             [(200, 120, 70), (130, 60, 30)]),  # Gradient colors for food zone
            ("nursery", NURSERY_RADIUS * self.nursery_area_scale, (70, 150, 70), "Nursery Zone",
             [(90, 170, 90), (50, 130, 50)]),   # Gradient colors for nursery
            ("sleeping", SLEEPING_RADIUS * self.sleeping_area_scale, (70, 70, 150), "Sleeping Zone",
             [(90, 90, 170), (50, 50, 130)])    # Gradient colors for sleeping area
        ]

        for area_type, radius, base_color, label, gradient_colors in areas:
            center = self.get_area_center(area_type)
            
            # Draw multiple concentric circles with gradient effect
            num_rings = 5
            for i in range(num_rings):
                ring_radius = radius * (1 - i/num_rings)
                # Alternate between gradient colors
                color = gradient_colors[i % 2]
                
                # Draw filled circle with very low opacity
                shapes.append(pyglet.shapes.Circle(
                    center[0], center[1], ring_radius,
                    color=(*color, 15),  # Very transparent
                    batch=batch
                ))
                
                # Draw ring outline with slightly higher opacity
                shapes.append(pyglet.shapes.Circle(
                    center[0], center[1], ring_radius,
                    color=(*color, 30),  # More visible outline
                    batch=batch
                ))

            # Add subtle pattern effect (dots or lines based on area type)
            if area_type == "food":
                # Food area: scattered dots pattern
                for _ in range(20):
                    angle = random.random() * 2 * math.pi
                    dist = random.random() * radius * 0.9
                    dot_x = center[0] + math.cos(angle) * dist
                    dot_y = center[1] + math.sin(angle) * dist
                    shapes.append(pyglet.shapes.Circle(
                        dot_x, dot_y, 3,
                        color=(*gradient_colors[0], 40),
                        batch=batch
                    ))
            
            elif area_type == "nursery":
                # Nursery area: nested hexagons pattern
                for i in range(3):
                    size = radius * (0.8 - i * 0.2)
                    points = []
                    for j in range(6):
                        angle = j * math.pi / 3
                        px = center[0] + math.cos(angle) * size
                        py = center[1] + math.sin(angle) * size
                        points.extend([px, py])
                    
                    shapes.append(pyglet.shapes.Line(
                        points[0], points[1],
                        points[2], points[3],
                        color=(*gradient_colors[0], 40),
                        batch=batch
                    ))
                    # ... add more lines to complete hexagon
            
            elif area_type == "sleeping":
                # Sleeping area: curved lines pattern
                num_curves = 8
                for i in range(num_curves):
                    angle = (i / num_curves) * 2 * math.pi
                    start_x = center[0] + math.cos(angle) * radius * 0.3
                    start_y = center[1] + math.sin(angle) * radius * 0.3
                    end_x = center[0] + math.cos(angle) * radius * 0.8
                    end_y = center[1] + math.sin(angle) * radius * 0.8
                    shapes.append(pyglet.shapes.Line(
                        start_x, start_y, end_x, end_y,
                        color=(*gradient_colors[0], 40),
                        batch=batch
                    ))

            # Add pulsing border effect
            border_scale = 1 + math.sin(time.time() * 2) * 0.02  # Subtle pulse
            shapes.append(pyglet.shapes.Circle(
                center[0], center[1], radius * border_scale,
                color=(*base_color, 50),  # Semi-transparent border
                batch=batch
            ))
            
            # Draw zone label with improved visibility
            # Calculate label position based on area type
            if area_type == "food":
                label_x = center[0]
                label_y = center[1] - radius - 25  # Below food zone
            elif area_type == "nursery":
                label_x = center[0]
                label_y = center[1] + radius + 25  # Above nursery zone
            elif area_type == "sleeping":
                label_x = center[0]
                label_y = center[1] - radius - 25  # Below sleeping zone

            # Ensure labels stay within screen bounds
            label_x = min(max(label_x, 100), WIDTH - SIDEBAR_WIDTH - 100)
            label_y = min(max(label_y, 30), HEIGHT - 30)

            # Draw label background with gradient
            bg_width = len(label) * 8 + 20
            bg_height = 30
            for i in range(bg_height):
                alpha = int(80 * (1 - i/bg_height))  # Gradient transparency
                pyglet.shapes.Rectangle(
                    label_x - bg_width/2,
                    label_y - bg_height/2 + i,
                    bg_width,
                    1,
                    color=(0, 0, 0, alpha)
                ).draw()
            
            # Draw label text with shadow
            # Shadow
            pyglet.text.Label(
                label,
                font_name='Arial',
                font_size=14,
                bold=True,
                x=label_x + 1,
                y=label_y - 1,
                anchor_x='center',
                anchor_y='center',
                color=(0, 0, 0, 200)
            ).draw()
            
            # Main text
            pyglet.text.Label(
                label,
                font_name='Arial',
                font_size=14,
                bold=True,
                x=label_x,
                y=label_y,
                anchor_x='center',
                anchor_y='center',
                color=(255, 255, 255, 230)
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
        
        # Use spatial partitioning to check nearby cells first
        nearby_entities = self.get_nearby_entities(x, y, 5)  # Increased radius for food search
        
        for entity in nearby_entities:
            if isinstance(entity, Creature) and entity.dead and entity.food_value > 0:
                # Calculate base distance
                distance = abs(x - entity.x) + abs(y - entity.y)
                
                # Check if there's too many creatures already targeting this food
                nearby_creatures = sum(1 for c in self.get_nearby_entities(entity.x, entity.y)
                                     if not c.dead)
                
                # Add penalty to distance based on nearby creatures
                distance += nearby_creatures * 2
                
                food_sources.append((entity.x, entity.y, distance))
        
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
        return sum(1 for entity in self.get_nearby_entities(x, y)
              if isinstance(entity, Creature) and not entity.dead)

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
        # Correct the distance calculation
        distance = ((px - center[0])**2 + (py - center[1])**2) ** 0.5
        
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
        if entity.dead:
            return False

        # Calculate movement deltas once
        dx = target_x - entity.x
        dy = target_y - entity.y
        
        # Calculate absolute values once
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        
        # If already at target, no need to move
        if dx == 0 and dy == 0:
            return True

        # Get normalized directions once
        dir_x = dx // abs_dx if dx != 0 else 0
        dir_y = dy // abs_dy if dy != 0 else 0
        
        # Use these cached values throughout the method
        possible_moves = []
        if abs_dx > abs_dy:
            if dx != 0:
                possible_moves.append((dir_x, 0))
                if dy != 0:
                    possible_moves.append((dir_x, dir_y))
                    possible_moves.append((0, dir_y))
        else:
            if dy != 0:
                possible_moves.append((0, dir_y))
                if dx != 0:
                    possible_moves.append((dir_x, dir_y))
                    possible_moves.append((dir_x, 0))

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
        if num_creatures == 0:
            return
        
        max_scale = 1.5
        scale_factor = 0.3
        
        self.sleeping_area_scale = min(max_scale, 1.0 + scale_factor)
        self.food_area_scale = min(max_scale, 1.0 + (sum(c.dead for c in self.creatures) / num_creatures) * scale_factor)
        self.nursery_area_scale = min(max_scale, 1.0 + (len(self.eggs) / num_creatures) * scale_factor)

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
    """Update the stats display with loading bars"""
    global selected_creature, selected_egg
    
    # Calculate common panel values once
    panel_center_x = stats_panel.x + (stats_panel.width / 2)
    base_x = panel_center_x - (SIDEBAR_WIDTH - 30) / 2
    base_y = stats_panel.y + stats_panel.height - 40
    bar_width = SIDEBAR_WIDTH - 30
    
    # Use these cached values throughout the method
    if selected_creature:
        pyglet.text.Label(
            "Creature Stats",
            font_name='Arial',
            font_size=12,
            bold=True,
            x=panel_center_x,
            y=base_y + 20,
            anchor_x='center',
            anchor_y='center'
        ).draw()
        
        if not selected_creature.dead:
            # Health bar
            draw_stat_bar(
                base_x, base_y - STAT_BAR_HEIGHT - STAT_BAR_PADDING,
                bar_width, selected_creature.health, 100,
                STAT_BAR_COLORS['health'], "Health", None
            )
            
            # Energy bar
            draw_stat_bar(
                base_x, base_y - (STAT_BAR_HEIGHT + STAT_BAR_PADDING) * 2,
                bar_width, selected_creature.energy, 100,
                STAT_BAR_COLORS['energy'], "Energy", None
            )
            
            # Hunger bar
            draw_stat_bar(
                base_x, base_y - (STAT_BAR_HEIGHT + STAT_BAR_PADDING) * 3,
                bar_width, selected_creature.hunger, 100,
                STAT_BAR_COLORS['hunger'], "Hunger", None
            )
            
            # Happiness bar
            draw_stat_bar(
                base_x, base_y - (STAT_BAR_HEIGHT + STAT_BAR_PADDING) * 4,
                bar_width, selected_creature.happiness, 100,
                STAT_BAR_COLORS['happiness'], "Happiness", None
            )
            
            # Age bar
            age_percentage = (selected_creature.age / selected_creature.max_age) * 100
            draw_stat_bar(
                base_x, base_y - (STAT_BAR_HEIGHT + STAT_BAR_PADDING) * 5,
                bar_width, age_percentage, 100,
                STAT_BAR_COLORS['age'], "Age", None,
                age_value=selected_creature.age  # Pass the actual age value
            )
            
            # Replace text status with icons
            if not selected_creature.dead:
                # Calculate starting position for status icons
                icon_y = base_y - (STAT_BAR_HEIGHT + STAT_BAR_PADDING) * 7  # Lower the icons
                icon_spacing = ICON_SIZE * 1.5  # Space between icons
                
                # Create list of active status icons
                active_statuses = []
                
                # Critical Status (low health/energy/hunger)
                if (selected_creature.health < 30 or 
                    selected_creature.energy < 30 or 
                    selected_creature.hunger < 30):
                    active_statuses.append("critical")
                
                # Moving to Target
                if selected_creature.target and not selected_creature.sleeping:
                    active_statuses.append("moving")
                
                # Sleeping
                if selected_creature.sleeping:
                    active_statuses.append("sleeping")
                
                # Eating
                if selected_creature.eating:
                    active_statuses.append("eating")
                
                # Carrying Food
                if selected_creature.carrying_food:
                    active_statuses.append("carrying")
                
                # Has Laid Egg
                if selected_creature.has_laid_egg:
                    active_statuses.append("egg")
                
                # Happy
                if selected_creature.happiness > 80:
                    active_statuses.append("happy")
                
                # Resting (when in sleep area but not sleeping)
                if (env.is_in_area(selected_creature.x, selected_creature.y, "sleeping") 
                    and not selected_creature.sleeping):
                    active_statuses.append("resting")
                
                # Looking for Food
                if selected_creature.target == "food":
                    active_statuses.append("seeking_food")
                
                # Looking for Nursery
                if selected_creature.target == "nursery":
                    active_statuses.append("seeking_nursery")
                
                # Social (nearby creatures)
                nearby_creatures = sum(1 for c in env.creatures 
                                     if c != selected_creature 
                                     and abs(c.x - selected_creature.x) + abs(c.y - selected_creature.y) <= 2)
                if nearby_creatures > 0:
                    active_statuses.append("social")
                
                # Elderly
                if selected_creature.age > selected_creature.max_age * 0.7:
                    active_statuses.append("elderly")
                
                # Calculate total width and center position
                total_width = len(active_statuses) * icon_spacing
                current_x = panel_center_x - (total_width / 2) + (icon_spacing / 2)
                
                # Draw all active status icons
                for status in active_statuses:
                    if status == "critical":
                        # Pulsing exclamation mark
                        opacity = int(180 + 75 * math.sin(selected_creature.animation_timer * 3))
                        pyglet.text.Label(
                            "!",
                            font_name='Arial',
                            font_size=ICON_SIZE,
                            bold=True,
                            x=current_x,
                            y=icon_y,
                            anchor_x='center',
                            anchor_y='center',
                            color=(255, 50, 50, opacity)
                        ).draw()
                    
                    elif status == "moving":
                        # Animated arrow
                        arrow_size = ICON_SIZE // 2
                        offset = math.sin(selected_creature.animation_timer * 3) * 3
                        pyglet.shapes.Line(
                            current_x - arrow_size, icon_y,
                            current_x + arrow_size + offset, icon_y,
                            width=2,
                            color=(200, 200, 200, 255)
                        ).draw()
                        # Arrow head
                        pyglet.shapes.Triangle(
                            current_x + arrow_size + offset, icon_y,
                            current_x + arrow_size - 4 + offset, icon_y + 4,
                            current_x + arrow_size - 4 + offset, icon_y - 4,
                            color=(200, 200, 200, 255)
                        ).draw()
                    
                    elif status == "sleeping":
                        # Z's animation (existing code)
                        for i in range(3):
                            z_label = pyglet.text.Label(
                                "Z",
                                font_name='Arial',
                                font_size=ICON_SIZE//2,
                                bold=True,
                                x=current_x + (i * ICON_SIZE//4),
                                y=icon_y + (i * ICON_SIZE//4),
                                anchor_x='center',
                                anchor_y='center',
                                color=(200, 200, 255, 255)
                            )
                            z_label.draw()
                    
                    elif status == "eating":
                        # Fork icon (existing code)
                        fork_height = ICON_SIZE
                        fork_width = ICON_SIZE // 3
                        pyglet.shapes.Rectangle(
                            current_x - fork_width//2,
                            icon_y - fork_height//2,
                            fork_width,
                            fork_height,
                            color=(255, 200, 0, 255)
                        ).draw()
                    
                    elif status == "carrying":
                        # Package icon
                        package_size = ICON_SIZE // 2
                        y_offset = math.sin(selected_creature.animation_timer * 3) * 2
                        pyglet.shapes.Rectangle(
                            current_x - package_size//2,
                            icon_y + y_offset - package_size//2,
                            package_size,
                            package_size,
                            color=(200, 150, 50)
                        ).draw()
                    
                    elif status == "egg":
                        # Egg icon (existing code)
                        pyglet.shapes.Circle(
                            current_x,
                            icon_y,
                            ICON_SIZE//2,
                            color=(255, 200, 0, 200)
                        ).draw()
                    
                    elif status == "happy":
                        # Floating heart
                        heart_y = icon_y + math.sin(selected_creature.animation_timer * 3) * 3
                        opacity = int(180 + 75 * math.sin(selected_creature.animation_timer * 3))
                        pyglet.text.Label(
                            "♥",
                            font_name='Arial',
                            font_size=ICON_SIZE//2,
                            x=current_x,
                            y=heart_y,
                            anchor_x='center',
                            anchor_y='center',
                            color=(255, 150, 150, opacity)
                        ).draw()
                    
                    elif status == "resting":
                        # Pause icon
                        bar_width = ICON_SIZE // 4
                        bar_height = ICON_SIZE // 2
                        spacing = ICON_SIZE // 4
                        pyglet.shapes.Rectangle(
                            current_x - spacing - bar_width//2,
                            icon_y - bar_height//2,
                            bar_width,
                            bar_height,
                            color=(150, 150, 255)
                        ).draw()
                        pyglet.shapes.Rectangle(
                            current_x + spacing - bar_width//2,
                            icon_y - bar_height//2,
                            bar_width,
                            bar_height,
                            color=(150, 150, 255)
                        ).draw()
                    
                    elif status == "seeking_food":
                        # Magnifying glass
                        glass_radius = ICON_SIZE // 3
                        handle_length = ICON_SIZE // 2
                        pyglet.shapes.Circle(
                            current_x - 2,
                            icon_y + 2,
                            glass_radius,
                            color=(200, 200, 200),
                            batch=None
                        ).draw()
                        pyglet.shapes.Line(
                            current_x + glass_radius - 2,
                            icon_y - glass_radius + 2,
                            current_x + glass_radius + handle_length - 2,
                            icon_y - glass_radius - handle_length + 2,
                            width=2,
                            color=(200, 200, 200)
                        ).draw()
                    
                    elif status == "seeking_nursery":
                        # Nest icon
                        nest_size = ICON_SIZE // 2
                        pyglet.shapes.Arc(
                            current_x,
                            icon_y,
                            nest_size,
                            color=(150, 100, 50),
                            batch=None,
                            angle=math.pi
                        ).draw()
                        # Add small egg in nest
                        pyglet.shapes.Circle(
                            current_x,
                            icon_y,
                            nest_size//3,
                            color=(255, 200, 0, 200)
                        ).draw()
                    
                    elif status == "social":
                        # Speech bubble
                        bubble_size = ICON_SIZE // 2
                        pyglet.shapes.Circle(
                            current_x,
                            icon_y + bubble_size//2,
                            bubble_size,
                            color=(255, 255, 255, 150)
                        ).draw()
                        # Small triangle for bubble tail
                        pyglet.shapes.Triangle(
                            current_x - bubble_size//2,
                            icon_y,
                            current_x - bubble_size//4,
                            icon_y + bubble_size//4,
                            current_x,
                            icon_y,
                            color=(255, 255, 255, 150)
                        ).draw()
                    
                    elif status == "elderly":
                        # Clock icon (existing code)
                        clock_radius = ICON_SIZE//2
                        pyglet.shapes.Circle(
                            current_x,
                            icon_y,
                            clock_radius,
                            color=(200, 200, 200, 200)
                        ).draw()
                        # Clock hands
                        pyglet.shapes.Line(
                            current_x, icon_y,
                            current_x + math.cos(math.pi/4) * clock_radius * 0.5,
                            icon_y + math.sin(math.pi/4) * clock_radius * 0.5,
                            width=2,
                            color=(100, 100, 100, 255)
                        ).draw()
                        pyglet.shapes.Line(
                            current_x, icon_y,
                            current_x + math.cos(-math.pi/6) * clock_radius * 0.7,
                            icon_y + math.sin(-math.pi/6) * clock_radius * 0.7,
                            width=2,
                            color=(100, 100, 100, 255)
                        ).draw()
                    
                    current_x += icon_spacing
        else:
            # Dead creature stats (centered)
            pyglet.text.Label(
                "DEAD CREATURE",
                font_name='Arial',
                font_size=12,
                bold=True,
                x=panel_center_x,
                y=base_y,
                anchor_x='center',
                anchor_y='top',
                color=(255, 100, 100, 255)
            ).draw()
            
            # Draw cause of death (centered)
            pyglet.text.Label(
                f"Cause: {selected_creature.death_cause}",
                font_name='Arial',
                font_size=10,
                x=panel_center_x,
                y=base_y - 25,
                anchor_x='center',
                anchor_y='top',
                color=(255, 255, 255, 255)
            ).draw()
            
            # Draw food bar (centered)
            draw_stat_bar(
                base_x,
                base_y - 65,
                bar_width,
                selected_creature.food_value/2,
                100,
                (150, 200, 50),
                "Food",
                None
            )
    
    elif selected_egg:
        panel_center_x = stats_panel.x + (stats_panel.width / 2)  # Center of the panel
        base_x = panel_center_x - (SIDEBAR_WIDTH - 30) / 2  # Center the content
        base_y = stats_panel.y + stats_panel.height - 40
        bar_width = SIDEBAR_WIDTH - 30
        
        # Title (centered)
        pyglet.text.Label(
            "Egg Status",
            font_name='Arial',
            font_size=12,
            bold=True,
            x=panel_center_x,
            y=base_y + 20,
            anchor_x='center',
            anchor_y='center'
        ).draw()
        
        # Progress bar
        progress = (selected_egg.timer / selected_egg.hatch_time) * 100
        draw_stat_bar(
            base_x, base_y - STAT_BAR_HEIGHT - STAT_BAR_PADDING,
            bar_width, progress, 100,
            (255, 200, 0), "Progress", None
        )

    else:
        # Draw "Nothing selected" message centered in stats panel
        pyglet.text.Label(
            "Nothing selected",
            font_name='Arial',
            font_size=14,
            x=stats_panel.x + stats_panel.width // 2,
            y=stats_panel.y + stats_panel.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)  # White color
        ).draw()

def draw_stat_bar(x, y, width, value, max_value, color, label, batch, age_value=None):
    """Draw a single stat bar with label and optional age value"""
    # Draw label text
    pyglet.text.Label(
        label,
        font_name='Arial',
        font_size=10,
        x=x,
        y=y + STAT_BAR_HEIGHT//2,
        anchor_x='left',
        anchor_y='center',
        color=(255, 255, 255, 255)
    ).draw()
    
    # Calculate bar dimensions
    bar_x = x + 70  # Offset for label
    bar_width = width - 80  # Adjust width to account for label
    
    # Draw background (dark gray)
    pyglet.shapes.Rectangle(
        bar_x, y,
        bar_width,
        STAT_BAR_HEIGHT,
        color=(50, 50, 50)
    ).draw()
    
    # Draw border
    border_color = (100, 100, 100)  # Light gray border
    border_thickness = 2
    
    # Top border
    pyglet.shapes.Line(
        bar_x, y + STAT_BAR_HEIGHT,
        bar_x + bar_width, y + STAT_BAR_HEIGHT,
        border_thickness,
        border_color
    ).draw()
    
    # Bottom border
    pyglet.shapes.Line(
        bar_x, y,
        bar_x + bar_width, y,
        border_thickness,
        border_color
    ).draw()
    
    # Left border
    pyglet.shapes.Line(
        bar_x, y,
        bar_x, y + STAT_BAR_HEIGHT,
        border_thickness,
        border_color
    ).draw()
    
    # Right border
    pyglet.shapes.Line(
        bar_x + bar_width, y,
        bar_x + bar_width, y + STAT_BAR_HEIGHT,
        border_thickness,
        border_color
    ).draw()
    
    # Draw progress bar
    progress_width = bar_width * (value / max_value)
    if progress_width > 0:
        pyglet.shapes.Rectangle(
            bar_x,
            y,
            progress_width,
            STAT_BAR_HEIGHT,
            color=color
        ).draw()
    
    # Draw value percentage (centered in the bar)
    percentage_text = f"{int(value)}%"
    if label == "Age" and age_value is not None:
        percentage_text = f"{int(value)}% ({int(age_value)} days)"
        
    pyglet.text.Label(
        percentage_text,
        font_name='Arial',
        font_size=9,
        x=bar_x + (bar_width / 2),
        y=y + STAT_BAR_HEIGHT//2,
        anchor_x='center',
        anchor_y='center',
        color=(255, 255, 255, 255)
    ).draw()

# Create the environment with only one creature
env = Environment((WIDTH - SIDEBAR_WIDTH) // GRID_SIZE, HEIGHT // GRID_SIZE)

# Update the legend labels to include groups and headers
legend_labels = [
    # Group 1: Basic States
    ("Basic States", "header"),
    ("Normal Creature", (0, 255, 0)),
    ("Dead Creature (with food)", "dead_with_food"),
    ("Egg", (255, 200, 0)),
    
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

def update_ui_positions():
    """Update all UI element positions with refined spacing"""
    # Calculate positions from top-right
    start_y = HEIGHT - TOP_MARGIN
    
    # Update panel positions
    control_panel.update_position(
        WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
        start_y - CONTROL_PANEL_HEIGHT
    )
    
    stats_panel.update_position(
        WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
        start_y - CONTROL_PANEL_HEIGHT - PANEL_SPACING - STATS_PANEL_HEIGHT
    )
    
    legend_panel.update_position(
        WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
        start_y - CONTROL_PANEL_HEIGHT - PANEL_SPACING - 
        STATS_PANEL_HEIGHT - PANEL_SPACING - LEGEND_PANEL_HEIGHT
    )
    
    # Remove the duplicate button positioning code since it's handled in the sprite creation

@window.event
def on_draw():
    window.clear()
    
    # Draw environment first
    env.draw(window)
    
    # Draw panels
    control_panel.draw()
    stats_panel.draw()
    legend_panel.draw()
    
    # Draw buttons with updated positions
    if current_speed_state == "pause":
        pause_button.draw()
        play_button.image = play_unclicked_image
        play_button.draw()
        fast_forward_button.image = fast_forward_unclicked_image
        fast_forward_button.draw()
    elif current_speed_state == "play":
        pause_button.image = pause_unclicked_image
        pause_button.draw()
        play_button.draw()
        fast_forward_button.image = fast_forward_unclicked_image
        fast_forward_button.draw()
    else:  # fast forward
        pause_button.image = pause_unclicked_image
        pause_button.draw()
        play_button.image = play_unclicked_image
        play_button.draw()
        fast_forward_button.draw()
    
    # Draw legend with adjusted starting position
    legend_start_y = legend_panel.y + legend_panel.height - LEGEND_TOP_PADDING
    y_offset = legend_start_y
    
    # Pre-calculate common colors and alpha values
    semi_transparent = 230
    critical_color = (255, 0, 0, 200)
    selection_color = (255, 255, 255, 180)
    base_creature_color = (0, 255, 0)
    
    # Age indicator colors
    age_colors = {
        "young_adult": (0, 255, 0),
        "middle_age": (255, 255, 0),
        "elder": (255, 0, 0)
    }
    
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
                               LEGEND_ICON_SIZE//2 + 4, color=selection_color).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=base_creature_color).draw()
            # Add inner circle to match actual creature appearance
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * INNER_CIRCLE_RATIO, 
                               color=(0, 255, 0, semi_transparent)).draw()
        elif color == "critical":
            # Critical status indicator with creature inside
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 + 2, color=critical_color).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=base_creature_color).draw()
            # Add inner circle to match actual creature appearance
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * INNER_CIRCLE_RATIO, 
                               color=(0, 255, 0, semi_transparent)).draw()
        elif color in ["young_adult", "middle_age", "elder"]:
            # Age indicator examples with outer and inner circles
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=age_colors[color]).draw()
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
    
    # Draw stats
    update_stats()

# Initial UI position update
update_ui_positions()

# Update method (called on every frame)
def update(dt):
    env.update(dt)  # Update creatures and eggs
    update_stats()  # Update the stats each frame

# Make sure to schedule the initial update
if FPS > 0:
    pyglet.clock.schedule_interval(update, 1.0 / FPS)

# Run the pyglet application
pyglet.app.run()