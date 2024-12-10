import pyglet

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