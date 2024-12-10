import pyglet
import math

from utils.constants import *

def format_stats(creature):
    """Format creature stats in a more readable way"""
    if not creature:
        return "No creature selected"
    
    return str(creature)  # Use the creature's string representation

def update_stats(selected_creature, selected_egg, stats_panel, env):
    """Update the stats display with loading bars"""
    # Calculate common panel values once
    panel_center_x = stats_panel.x + (stats_panel.width / 2)
    base_x = panel_center_x - (SIDEBAR_WIDTH - 30) / 2
    base_y = stats_panel.y + stats_panel.height - 40
    bar_width = SIDEBAR_WIDTH - 30
    
    # Draw title
    if selected_creature or selected_egg:
        title = "Creature Stats" if selected_creature else "Egg Status"
        pyglet.text.Label(
            title,
            font_name='Arial',
            font_size=12,
            bold=True,
            x=panel_center_x,
            y=stats_panel.y + stats_panel.height - 20,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)
        ).draw()
    
    if selected_creature:
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
            if selected_creature:  # Add null check
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
                death_cause = getattr(selected_creature, 'death_cause', 'Unknown')  # Default to 'Unknown' if not set
                pyglet.text.Label(
                    f"Cause: {death_cause}",
                    font_name='Arial',
                    font_size=10,
                    x=panel_center_x,
                    y=base_y - 25,
                    anchor_x='center',
                    anchor_y='top',
                    color=(255, 255, 255, 255)
                ).draw()
                
                # Draw food bar (centered)
                food_value = getattr(selected_creature, 'food_value', 0)  # Default to 0 if not set
                draw_stat_bar(
                    base_x,
                    base_y - 65,
                    bar_width,
                    food_value/2,
                    100,
                    (150, 200, 50),
                    "Food",
                    None
                )
    
    elif selected_egg:
        # Progress bar using egg's get_progress method
        progress = selected_egg.get_progress()
        draw_stat_bar(
            base_x, base_y - STAT_BAR_HEIGHT - STAT_BAR_PADDING,
            bar_width, progress, 100,
            (255, 200, 0), "Progress", None
        )

        # Status
        status = "Ready to hatch!" if selected_egg.ready_to_hatch else "Incubating..."
        pyglet.text.Label(
            status,
            font_name='Arial',
            font_size=10,
            x=panel_center_x,
            y=base_y - (STAT_BAR_HEIGHT + STAT_BAR_PADDING) * 2.5,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 100, 255) if selected_egg.ready_to_hatch else (255, 255, 255, 255)
        ).draw()

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