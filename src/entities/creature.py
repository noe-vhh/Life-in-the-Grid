import pyglet
import random
import math
import time

from utils.constants import *
from entities.egg import Egg

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
        self.decomposition = 0  # Add this line
        self.death_cause = None  # Add this line
        
        # Animation properties
        self.animation_timer = 0
        self.animation_frame = 0
        self.animation_speed = 0.016
        self.last_update_time = time.time()
        self.heart_animation_offset = random.random() * math.pi * 2  # Random start phase
        self.frame_update_interval = 0.2  # Time between frame updates in seconds
        self.accumulated_time = 0  # Track time between frames
        
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

        # Always update animations based on real time, regardless of game speed
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update animations even when game is at 1 FPS
        self.animation_timer += elapsed_time
        self.accumulated_time += elapsed_time

        # Update animation frame based on accumulated time
        if self.accumulated_time >= self.frame_update_interval:
            self.animation_frame = (self.animation_frame + 1) % 3
            self.accumulated_time = 0  # Reset accumulated time

        # Update other animations (eyes, mouth, etc.)
        self.update_mouth()
        self.update_eyes()

        # Only process game logic updates when not paused
        if self.env.game_manager.current_speed_state != "pause":
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
            if self.happiness > 80 and not self.sleeping:
                # Calculate position with smooth animation
                continuous_angle = (self.animation_timer * HEART_ANIMATION_SPEED) % (2 * math.pi)
                x_offset = math.cos(continuous_angle) * 3
                y_offset = math.sin(continuous_angle) * 3
                
                # Position the heart above other icons (add GRID_SIZE to raise it higher)
                icon_y = center_y + GRID_SIZE
                
                # Calculate opacity with smoother animation
                opacity = int(180 + 75 * math.sin(self.animation_timer * 3))
                
                # Create heart label and add it to the batch
                heart = pyglet.text.Label(
                    "♥",
                    font_name='Arial',
                    font_size=14,
                    x=center_x + x_offset,
                    y=icon_y + y_offset,  # Use icon_y for consistent positioning
                    anchor_x='center',
                    anchor_y='center',
                    color=(255, 150, 150, opacity),
                    batch=batch
                )
                shapes.append(heart)

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