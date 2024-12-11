import random
import math
import pyglet
import time

from entities.creature import Creature
from utils.constants import *

# The environment where creatures live
class Environment:
    def __init__(self, width, height, game_manager=None):
        # Adjust width to account for sidebar
        self.width = (WIDTH - SIDEBAR_WIDTH) // GRID_SIZE  # Use adjusted width
        self.height = height
        self.game_manager = game_manager
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
        self.fertilizer = {}  # (x,y) -> fertilizer amount
        self.grass = {}       # (x,y) -> grass amount
        
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
        
        # Update creatures and handle decomposition
        decomposing_positions = []  # Track positions of decomposing creatures
        for creature in self.creatures:
            if not creature.dead:
                old_x, old_y = creature.x, creature.y
                creature.update()
                
                # Update grid if position changed
                if (creature.x, creature.y) != (old_x, old_y):
                    self.grid.pop((old_x, old_y), None)
                    self.grid[(creature.x, creature.y)] = creature
            else:
                # Handle dead creature decomposition
                if creature.decomposition < MAX_DECOMPOSITION:
                    creature.decomposition += DECOMPOSITION_RATE
                    # Add fertilizer as creature decomposes
                    self.add_fertilizer(creature.x, creature.y, DECOMPOSITION_RATE * 0.5)
                    decomposing_positions.append((creature.x, creature.y))
                # Remove dead creatures with no food value and full decomposition
                if creature.food_value <= 0 and creature.decomposition >= MAX_DECOMPOSITION:
                    self.creatures_to_remove.append(creature)
        
        # Update eggs
        for egg in self.eggs[:]:  # Create a copy of the list to iterate over
            egg.update()
            if egg.ready_to_hatch:
                # Unselect the egg if it is selected
                if egg.selected:
                    egg.selected = False
                    # Update game manager's selected egg through environment
                    if self.game_manager:
                        self.game_manager.selected_egg = None

                # Create new creature at egg's position
                new_creature = Creature(egg.x, egg.y, self)
                self.creatures.append(new_creature)
                self.grid[(egg.x, egg.y)] = new_creature
                # Remove the hatched egg
                self.hatch_egg(egg)
                self.eggs.remove(egg)
                self.grid.pop((egg.x, egg.y), None)
        
        # Remove dead creatures
        for creature in self.creatures_to_remove:
            if creature in self.creatures:
                self.creatures.remove(creature)
                self.grid.pop((creature.x, creature.y), None)
        self.creatures_to_remove.clear()
        
        # Update fertilizer spread and grass growth only near decomposing bodies
        new_fertilizer = self.fertilizer.copy()
        new_grass = self.grass.copy()
        
        # Define spread radius (how far fertilizer and grass can spread)
        SPREAD_RADIUS = 2
        
        # Only process cells near decomposing creatures
        for decomp_x, decomp_y in decomposing_positions:
            # Check cells within spread radius
            for dx in range(-SPREAD_RADIUS, SPREAD_RADIUS + 1):
                for dy in range(-SPREAD_RADIUS, SPREAD_RADIUS + 1):
                    x, y = decomp_x + dx, decomp_y + dy
                    
                    # Skip if position is invalid or too far (using Manhattan distance)
                    if not self.is_valid_position(x, y) or abs(dx) + abs(dy) > SPREAD_RADIUS:
                        continue
                    
                    # Handle fertilizer spread
                    if (decomp_x, decomp_y) in self.fertilizer:
                        amount = self.fertilizer[(decomp_x, decomp_y)]
                        spread_amount = amount * FERTILIZER_SPREAD_RATE
                        if (x, y) not in new_fertilizer:
                            new_fertilizer[(x, y)] = 0
                        new_fertilizer[(x, y)] = min(MAX_FERTILIZER, 
                            new_fertilizer[(x, y)] + spread_amount)
                    
                    # Handle grass growth where there's fertilizer
                    if (x, y) in new_fertilizer and new_fertilizer[(x, y)] > 0:
                        if (x, y) not in new_grass:
                            new_grass[(x, y)] = 0
                        new_grass[(x, y)] = min(100, new_grass.get((x, y), 0) + GRASS_GROWTH_RATE)
        
        self.fertilizer = new_fertilizer
        self.grass = new_grass

    def draw(self, screen):
        batch = pyglet.graphics.Batch()
        shapes = []

        # Layer 1: Draw fertilizer and grass with low opacity
        for (x, y), fertilizer_amount in self.fertilizer.items():
            if fertilizer_amount > 0:
                alpha = int((fertilizer_amount / MAX_FERTILIZER) * 80)  # Very transparent
                shapes.append(pyglet.shapes.Rectangle(
                    x * GRID_SIZE, y * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE,
                    color=(139, 69, 19, alpha),
                    batch=batch
                ))
        
        for (x, y), grass_amount in self.grass.items():
            if grass_amount > 0:
                alpha = int((grass_amount / 100) * 80)  # Very transparent
                shapes.append(pyglet.shapes.Rectangle(
                    x * GRID_SIZE, y * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE,
                    color=(34, 139, 34, alpha),
                    batch=batch
                ))

        # Layer 2: Draw colony areas
        areas = [
            ("food", FOOD_STORAGE_RADIUS * self.food_area_scale, (150, 80, 50), "Food Zone", 
             [(200, 120, 70), (130, 60, 30)]),
            ("nursery", NURSERY_RADIUS * self.nursery_area_scale, (70, 150, 70), "Nursery Zone",
             [(90, 170, 90), (50, 130, 50)]),
            ("sleeping", SLEEPING_RADIUS * self.sleeping_area_scale, (70, 70, 150), "Sleeping Zone",
             [(90, 90, 170), (50, 50, 130)])
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

        # Layer 3: Draw grid lines
        for x in range(0, self.width + 1):
            x_pos = x * GRID_SIZE
            shapes.append(pyglet.shapes.Line(
                x_pos, 0,
                x_pos, HEIGHT,
                color=(50, 50, 50),
                batch=batch
            ))

        for y in range(0, self.height + 1):
            y_pos = y * GRID_SIZE
            shapes.append(pyglet.shapes.Line(
                0, y_pos,
                WIDTH - SIDEBAR_WIDTH, y_pos,
                color=(50, 50, 50),
                batch=batch
            ))

        # Layer 4: Draw creatures and eggs
        for egg in self.eggs:
            egg_shapes = egg.draw(batch)
            if egg_shapes:
                shapes.extend(egg_shapes)

        for creature in self.creatures:
            creature_shapes = creature.draw(batch)
            if creature_shapes:
                shapes.extend(creature_shapes)

        # Draw everything at once using the batch
        batch.draw()

        return shapes

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

    def add_fertilizer(self, x, y, amount):
        """Add fertilizer to a position"""
        if (x, y) not in self.fertilizer:
            self.fertilizer[(x, y)] = 0
        self.fertilizer[(x, y)] = min(MAX_FERTILIZER, self.fertilizer[(x, y)] + amount)

    def hatch_egg(self, egg):
        """Handle egg hatching and create a new creature"""
        # Create a new creature at the egg's position
        new_creature = Creature(egg.x, egg.y, self)
        self.creatures.append(new_creature)
        self.grid[(egg.x, egg.y)] = new_creature