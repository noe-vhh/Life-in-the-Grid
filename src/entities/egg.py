import math
import pyglet

from utils.constants import *

# The egg class to handle egg incubation
class Egg:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.env = environment
        self.timer = 0
        self.hatch_time = EGG_HATCH_TIME
        self.selected = False
        self.ready_to_hatch = False

    def update(self):
        """Increment the egg's timer and check if ready to hatch"""
        if self.timer < self.hatch_time:
            self.timer += 1
        
        if self.timer >= self.hatch_time and not self.ready_to_hatch:
            # Reset egg laying status for nearby parent creatures
            nearby_creatures = [
                creature for creature in self.env.creatures
                if abs(creature.x - self.x) + abs(creature.y - self.y) <= EGG_NEARBY_PARENT_RANGE
                and creature.has_laid_egg
            ]
            for creature in nearby_creatures:
                creature.has_laid_egg = False
            self.ready_to_hatch = True

    def get_progress(self):
        """Return the egg's incubation progress as a percentage"""
        return (self.timer / self.hatch_time) * 100

    def get_time_remaining(self):
        """Return the time remaining until hatching"""
        return max(0, self.hatch_time - self.timer)

    def __str__(self):
        """Return a string representation of the egg's status"""
        progress = min(100, int(self.get_progress()))
        return f"Egg Progress: {progress}%"

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
        
        # Add shine effect
        shine_x = center_x + current_radius * EGG_SHINE_OFFSET
        shine_y = center_y + current_radius * EGG_SHINE_OFFSET
        shapes.append(pyglet.shapes.Circle(
            shine_x, shine_y,
            current_radius * 0.2,
            color=(255, 255, 255, 180),
            batch=batch
        ))
        
        # Progress indicator
        if self.timer > 0:
            progress = min(self.timer / self.hatch_time, 1.0)
            shapes.append(pyglet.shapes.Arc(
                center_x, center_y,
                current_radius + 2,
                color=(255, 255, 255, 150),
                batch=batch,
                angle=progress * math.pi * 2
            ))
        
        return shapes