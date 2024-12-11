# Window and Display Settings
WIDTH = 1200
HEIGHT = 900
FPS = 0  # Initial FPS (paused)
MIN_FPS = 1
MAX_FPS = 60
fps_input_active = False
current_speed_state = "pause"
selected_creature = None
selected_egg = None

# Grid and Layout
GRID_SIZE = 50
SIDEBAR_WIDTH = 280
TOP_MARGIN = 15
PANEL_SPACING = 15
QUADRANT_OFFSET = 300
icon_scale = 0.075

# Nest Area Configuration
NEST_CENTER_X = WIDTH // 4
NEST_CENTER_Y = HEIGHT // 2
FOOD_STORAGE_RADIUS = 5 * GRID_SIZE
NURSERY_RADIUS = 3 * GRID_SIZE
SLEEPING_RADIUS = 4 * GRID_SIZE

# UI Panel Dimensions
CONTROL_PANEL_HEIGHT = 60
STATS_PANEL_HEIGHT = 220
LEGEND_PANEL_HEIGHT = 440

# Legend Styling
LEGEND_ITEM_SPACING = 24
LEGEND_HEADER_SPACING = 30
LEGEND_GROUP_SPACING = 15
LEGEND_TEXT_SIZE = 10
LEGEND_HEADER_SIZE = 12
LEGEND_ICON_SIZE = 16
LEGEND_TOP_PADDING = 50

# Visual Indicators
INDICATOR_BORDER_WIDTH = 2
SELECTION_RING_SIZE = 4
STATUS_RING_SIZE = 2
INNER_CIRCLE_RATIO = 0.6

# Icon and Animation Settings
ICON_ANIMATION_SPEED = 0.05
ICON_OFFSET_Y = GRID_SIZE // 2
ICON_SIZE = GRID_SIZE // 2
HEART_ANIMATION_SPEED = 2.0

# Creature Features - Eyes
EYE_SIZE = 3
EYE_SPACING = 6
EYE_OFFSET_Y = 2
PUPIL_SIZE = 2
PUPIL_RANGE = 2
BLINK_INTERVAL = 5
BLINK_DURATION = 1

# Creature Features - Antennae
ANTENNA_LENGTH = 8
ANTENNA_WIDTH = 2
ANTENNA_SPACING = 6
ANTENNA_WAVE_SPEED = 0.25
ANTENNA_WAVE_AMOUNT = 0.5

# Creature Features - Mouth
MOUTH_WIDTH = 8
MOUTH_HEIGHT = 4
MOUTH_Y_OFFSET = -8
MOUTH_OPEN_SPEED = 0.1
MAX_MOUTH_OPEN = 6
SMILE_CURVE = 3

# Animation Parameters
BREATH_SPEED = 0.1
BREATH_AMOUNT = 0.05
DEAD_BREATH_AMOUNT = 0.08

# Egg Animation
EGG_PULSE_SPEED = 2.0
EGG_INNER_RATIO = 0.7
EGG_SHINE_OFFSET = 0.3

# Creature Appearance - Patterns
TEXTURE_PATTERNS = {
    "dots": {"chance": 0.25, "density": 8},
    "stripes": {"chance": 0.25, "density": 4},
    "spots": {"chance": 0.25, "density": 5},
    "plain": {"chance": 0.25}
}

# Color Definitions
PATTERN_COLORS = [
    (255, 255, 255),  # White
    (50, 50, 50),     # Dark Gray
    (200, 200, 200),  # Light Gray
    (255, 223, 186),  # Peach
    (255, 218, 233),  # Pink
    (230, 230, 255)   # Light Blue
]

# UI Stats Display
STAT_BAR_HEIGHT = 15
STAT_BAR_PADDING = 5
STAT_BAR_COLORS = {
    'health': (255, 50, 50),     # Red
    'energy': (50, 150, 255),    # Blue
    'hunger': (255, 200, 50),    # Yellow
    'happiness': (255, 100, 255), # Pink
    'age': (100, 255, 100),      # Green
    'decomposition': (139, 69, 19),  # Brown
    'food': (255, 165, 0)        # Orange
}

# Age indicator colors
age_colors = {
    "young_adult": (0, 255, 0),
    "middle_age": (255, 255, 0),
    "elder": (255, 0, 0)
}
    
# Pre-calculate common colors and alpha values
semi_transparent = 230
critical_color = (255, 0, 0, 200)
selection_color = (255, 255, 255, 180)
base_creature_color = (0, 255, 0)

# Decomposition and Growth Settings
DECOMPOSITION_RATE = 0.1  # Rate at which creatures decompose
MAX_DECOMPOSITION = 100
MAX_FERTILITY = 100
GRASS_GROWTH_RATE = 0.1
FERTILITY_SPREAD_RATE = 0.05
GRASS_SPREAD_CHANCE = 0.01