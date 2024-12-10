import pyglet

from utils.constants import *
from managers.game_manager import GameManager
from managers.ui_manager import UIManager

# Create the window
window = pyglet.window.Window(WIDTH, HEIGHT, "Creature Simulation", resizable=False)

# Create managers
game_manager = GameManager()
ui_manager = UIManager(game_manager)
game_manager.set_ui_manager(ui_manager)  # Set the UI manager reference

# Initial UI position update
ui_manager.update_ui_positions()

@window.event
def on_mouse_press(x, y, button, modifiers):
    # Handle grid clicks
    if game_manager.handle_click(x, y):
        return

    # Handle UI clicks
    clicked_button = ui_manager.handle_click(x, y)
    if clicked_button:
        if clicked_button == "pause" and game_manager.current_speed_state != "pause":
            game_manager.current_speed_state = "pause"
            game_manager.update_fps(0)
        elif clicked_button == "play" and game_manager.current_speed_state != "play":
            game_manager.current_speed_state = "play"
            game_manager.update_fps(1)
        elif clicked_button == "fast" and game_manager.current_speed_state != "fast":
            game_manager.current_speed_state = "fast"
            game_manager.update_fps(20)
        
        ui_manager.update_button_states(game_manager.current_speed_state)

@window.event
def on_draw():
    window.clear()
    game_manager.environment.draw(window)
    ui_manager.draw()

# Initial setup
if game_manager.FPS > 0:
    pyglet.clock.schedule_interval(game_manager.update, 1.0 / game_manager.FPS)

# Run the application
pyglet.app.run()