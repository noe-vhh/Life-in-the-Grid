import pyglet

from utils.constants import *
from environment.environment import Environment
from ui.stats import update_stats

class GameManager:
    def __init__(self):
        self.current_speed_state = "pause"
        self.FPS = 0
        self.selected_creature = None
        self.selected_egg = None
        self.environment = Environment((WIDTH - SIDEBAR_WIDTH) // GRID_SIZE, HEIGHT // GRID_SIZE, self)
        self.ui_manager = None

    def set_ui_manager(self, ui_manager):
        """Set the UI manager reference"""
        self.ui_manager = ui_manager

    def update_fps(self, new_fps):
        """Update the FPS and reschedule the update function"""
        self.FPS = new_fps
        pyglet.clock.unschedule(self.update)
        if self.FPS > 0:
            pyglet.clock.schedule_interval(self.update, 1.0 / self.FPS)

    def handle_click(self, x, y):
        if x < WIDTH - SIDEBAR_WIDTH:  # Grid area click
            grid_x = x // GRID_SIZE
            grid_y = y // GRID_SIZE
            self._handle_grid_click(grid_x, grid_y)
            return True
        return False

    def _handle_grid_click(self, grid_x, grid_y):
        creature_found = False
        egg_found = False

        # Check for creature click
        for creature in self.environment.creatures:
            if creature.x == grid_x and creature.y == grid_y:
                self._select_creature(creature)
                creature_found = True
                break

        # Check for egg click
        if not creature_found:
            for egg in self.environment.eggs:
                if egg.x == grid_x and egg.y == grid_y:
                    self._select_egg(egg)
                    egg_found = True
                    break

        # Deselect if clicking empty space
        if not creature_found and not egg_found:
            self._deselect_all()

    def _select_creature(self, creature):
        if self.selected_creature != creature:
            self._deselect_all()
            self.selected_creature = creature
            self.selected_creature.selected = True

    def _select_egg(self, egg):
        """Select an egg and deselect any previously selected entities"""
        self._deselect_all()  # Deselect everything first
        self.selected_egg = egg
        egg.selected = True  # Make sure to set the selected flag

    def _deselect_all(self):
        if self.selected_creature:
            self.selected_creature.selected = False
            self.selected_creature = None
        if self.selected_egg:
            self.selected_egg.selected = False
            self.selected_egg = None

    def update(self, dt):
        """Update game state"""
        self.environment.update(dt)
        
        # Deselect if selected creature was removed
        if self.selected_creature and self.selected_creature not in self.environment.creatures:
            self.selected_creature = None

        if self.ui_manager:
            update_stats(self.selected_creature, self.selected_egg, self.ui_manager.stats_panel, self.environment)