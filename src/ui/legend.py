import pyglet
from utils.constants import *

class Legend:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Define the labels and their corresponding colors/types with groups and headers
        self.labels = [
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
            ("Ready to Lay Egg", (255, 200, 0))
        ]

        # Define colors
        self.age_colors = {
            "young_adult": (0, 255, 0),
            "middle_age": (255, 255, 0),
            "elder": (255, 0, 0)
        }
        
        self.base_creature_color = (0, 255, 0)
        self.selection_color = (255, 255, 255)
        self.critical_color = (255, 0, 0)
        self.semi_transparent = 230
        self.INNER_CIRCLE_RATIO = 0.7

    def draw(self):
        y_offset = self.y + self.height - 20  # Start from the top of the panel
        legend_start_y = y_offset  # Store initial y position

        for label_text, color in self.labels:
            if color == "header":
                # Add extra space before headers (except the first one)
                if y_offset < legend_start_y:
                    y_offset -= LEGEND_GROUP_SPACING
                
                pyglet.text.Label(
                    label_text,
                    font_name='Arial',
                    font_size=LEGEND_HEADER_SIZE,
                    bold=True,
                    x=self.x + 15,
                    y=y_offset,
                    anchor_x='left',
                    anchor_y='center',
                    color=(200, 200, 200, 255)
                ).draw()
                y_offset -= LEGEND_HEADER_SPACING
                continue
                
            # Draw the indicator
            self.draw_indicator(color, y_offset)
            
            # Draw label with refined positioning
            label = pyglet.text.Label(
                label_text,
                font_name='Arial',
                font_size=LEGEND_TEXT_SIZE,
                x=self.x + 45,
                y=y_offset,
                width=self.width - 55,
                multiline=True,
                anchor_x='left',
                anchor_y='center'
            )
            label.draw()
            
            y_offset -= LEGEND_ITEM_SPACING

    def draw_indicator(self, color, y_offset):
        x_pos = self.x + 20 + LEGEND_ICON_SIZE//2

        if color == "dead_with_food":
            # Dead creature with food indicator
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=(100, 0, 0)).draw()
            # Draw green arc to show remaining food
            pyglet.shapes.Arc(x_pos, y_offset, 
                            LEGEND_ICON_SIZE//2 * 0.8,
                            color=(120, 150, 0),
                            start_angle=0,
                            angle=4.71239).draw()
        elif color == "selected":
            # Selection indicator with creature inside
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 + 4, color=self.selection_color).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=self.base_creature_color).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * self.INNER_CIRCLE_RATIO, 
                               color=(0, 255, 0, self.semi_transparent)).draw()
        elif color == "critical":
            # Critical status indicator with creature inside
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 + 2, color=self.critical_color).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=self.base_creature_color).draw()
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * self.INNER_CIRCLE_RATIO, 
                               color=(0, 255, 0, self.semi_transparent)).draw()
        elif color in ["young_adult", "middle_age", "elder"]:
            # Age indicator examples with outer and inner circles
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=self.age_colors[color]).draw()
            if color == "young_adult":
                inner_color = (0, 255, 0)
            elif color == "middle_age":
                inner_color = (255, 255, 0)
            else:  # elder
                inner_color = (255, 0, 0)
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2 * self.INNER_CIRCLE_RATIO, 
                               color=inner_color + (230,)).draw()
        elif isinstance(color, tuple):
            # Regular color indicators (sleeping, carrying food, etc.)
            pyglet.shapes.Circle(x_pos, y_offset, 
                               LEGEND_ICON_SIZE//2, color=color).draw()
            # Add inner circle for consistency if it's a living creature color
            if color != (255, 200, 0):  # Not an egg
                pyglet.shapes.Circle(x_pos, y_offset, 
                                   LEGEND_ICON_SIZE//2 * self.INNER_CIRCLE_RATIO, 
                                   color=color + (230,)).draw()