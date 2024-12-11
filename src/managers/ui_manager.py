import pyglet

from utils.constants import *
from ui.panel import Panel
from ui.stats import update_stats
from ui.legend import Legend

class UIManager:
    def __init__(self, game_manager):
        self.game_manager = game_manager

        # Load button images
        self.pause_unclicked_image = pyglet.resource.image('assets/ui icons/pause-play-unclick.png')
        self.pause_clicked_image = pyglet.resource.image('assets/ui icons/pause-play-click.png')
        self.play_unclicked_image = pyglet.resource.image('assets/ui icons/play-button-unclick.png')
        self.play_clicked_image = pyglet.resource.image('assets/ui icons/play-button-click.png')
        self.fast_forward_unclicked_image = pyglet.resource.image('assets/ui icons/fast-forward-button-unclick.png')
        self.fast_forward_clicked_image = pyglet.resource.image('assets/ui icons/fast-forward-button-click.png')

        # Create panels as instance variables
        self.control_panel = Panel(
            WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
            HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT,
            SIDEBAR_WIDTH,
            CONTROL_PANEL_HEIGHT,
            ""
        )

        self.stats_panel = Panel(
            WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
            HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT - PANEL_SPACING - STATS_PANEL_HEIGHT,
            SIDEBAR_WIDTH,
            STATS_PANEL_HEIGHT
        )

        self.legend_panel = Panel(
            WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
            HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT - PANEL_SPACING - 
            STATS_PANEL_HEIGHT - PANEL_SPACING - LEGEND_PANEL_HEIGHT,
            SIDEBAR_WIDTH,
            LEGEND_PANEL_HEIGHT
        )

        # Initialize buttons
        self._init_buttons()

        # Initialize legend with the panel's position and size
        self.legend = Legend(
            self.legend_panel.x,
            self.legend_panel.y,
            self.legend_panel.width,
            self.legend_panel.height
        )

    def _init_buttons(self):
        # Calculate button positions
        button_width = self.pause_unclicked_image.width * icon_scale
        button_spacing = 20
        total_buttons_width = (button_width * 3) + (button_spacing * 2)
        start_x = WIDTH - SIDEBAR_WIDTH + (SIDEBAR_WIDTH - total_buttons_width - 30) // 2
        vertical_center = HEIGHT - TOP_MARGIN - CONTROL_PANEL_HEIGHT//2

        # Create button sprites
        self.pause_button = self._create_button(
            self.pause_clicked_image,
            start_x,
            vertical_center
        )

        self.play_button = self._create_button(
            self.play_unclicked_image,
            start_x + button_width + button_spacing,
            vertical_center
        )

        self.fast_forward_button = self._create_button(
            self.fast_forward_unclicked_image,
            start_x + (button_width + button_spacing) * 2,
            vertical_center
        )

    def _create_button(self, image, x, y):
        button = pyglet.sprite.Sprite(
            image,
            x=x,
            y=y - (image.height * icon_scale) // 2
        )
        button.scale = icon_scale
        return button

    def handle_click(self, x, y):
        # Return the clicked button type or None
        button_width = 38
        button_height = 38
        
        # Check pause button
        if (self.pause_button.x <= x <= self.pause_button.x + button_width and 
            self.pause_button.y <= y <= self.pause_button.y + button_height):
            return "pause"
            
        # Check play button
        elif (self.play_button.x <= x <= self.play_button.x + button_width and 
              self.play_button.y <= y <= self.play_button.y + button_height):
            return "play"
            
        # Check fast forward button
        elif (self.fast_forward_button.x <= x <= self.fast_forward_button.x + button_width and 
              self.fast_forward_button.y <= y <= self.fast_forward_button.y + button_height):
            return "fast"
        
        return None

    def update_button_states(self, current_speed_state):
        # Update button images based on current state
        self.pause_button.image = (self.pause_clicked_image if current_speed_state == "pause" 
                                 else self.pause_unclicked_image)
        self.play_button.image = (self.play_clicked_image if current_speed_state == "play" 
                                else self.play_unclicked_image)
        self.fast_forward_button.image = (self.fast_forward_clicked_image if current_speed_state == "fast" 
                                        else self.fast_forward_unclicked_image)

    def draw(self):
        # Draw panels
        self.control_panel.draw()
        self.stats_panel.draw()
        self.legend_panel.draw()
        
        # Draw legend and stats content
        self.draw_legend_content()
        self.draw_stats_content()
        
        # Draw buttons
        self.pause_button.draw()
        self.play_button.draw()
        self.fast_forward_button.draw()

    def update_ui_positions(self):
        """Update all UI element positions with refined spacing"""
        start_y = HEIGHT - TOP_MARGIN
        
        self.control_panel.update_position(
            WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
            start_y - CONTROL_PANEL_HEIGHT
        )
        
        self.stats_panel.update_position(
            WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
            start_y - CONTROL_PANEL_HEIGHT - PANEL_SPACING - STATS_PANEL_HEIGHT
        )
        
        self.legend_panel.update_position(
            WIDTH - SIDEBAR_WIDTH - TOP_MARGIN,
            start_y - CONTROL_PANEL_HEIGHT - PANEL_SPACING - 
            STATS_PANEL_HEIGHT - PANEL_SPACING - LEGEND_PANEL_HEIGHT
        )

    def draw_legend_content(self):
        # Call the legend's draw method
        self.legend.draw()

    def draw_stats_content(self):
        selected_creature = self.game_manager.selected_creature
        selected_egg = self.game_manager.selected_egg
        selected_tile = self.game_manager.selected_tile
        update_stats(selected_creature, selected_egg, selected_tile, 
                    self.stats_panel, self.game_manager.environment)