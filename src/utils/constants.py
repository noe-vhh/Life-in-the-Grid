# Core Display Configuration
WIDTH = 1200
HEIGHT = 900
SIDEBAR_WIDTH = 280
TOP_MARGIN = 15
PANEL_SPACING = 15
GRID_SIZE = 50

# Performance Settings
FPS = 0  # Initial FPS (paused)
MIN_FPS = 1
MAX_FPS = 60
fps_input_active = False
current_speed_state = "pause"

# Interactive State
selected_creature = None
selected_egg = None
icon_scale = 0.075

# Colony Layout Configuration
NEST_CENTER_X = WIDTH // 4
NEST_CENTER_Y = HEIGHT // 2
QUADRANT_OFFSET = 300

# Zone Radii (in grid units)
FOOD_STORAGE_RADIUS = 5 * GRID_SIZE
NURSERY_RADIUS = 3 * GRID_SIZE
SLEEPING_RADIUS = 4 * GRID_SIZE

# UI Panel Dimensions and Styling
CONTROL_PANEL_HEIGHT = 60
STATS_PANEL_HEIGHT = 220
LEGEND_PANEL_HEIGHT = 440

# Legend Configuration
LEGEND_ITEM_SPACING = 24
LEGEND_HEADER_SPACING = 30
LEGEND_GROUP_SPACING = 15
LEGEND_TEXT_SIZE = 10
LEGEND_HEADER_SIZE = 12
LEGEND_ICON_SIZE = 16
LEGEND_TOP_PADDING = 50

# Visual Feedback Constants
INDICATOR_BORDER_WIDTH = 2
SELECTION_RING_SIZE = 4
STATUS_RING_SIZE = 2
INNER_CIRCLE_RATIO = 0.6

# Animation Timing
ICON_ANIMATION_SPEED = 0.05
HEART_ANIMATION_SPEED = 2.0
BREATH_SPEED = 0.1
BREATH_AMOUNT = 0.05
DEAD_BREATH_AMOUNT = 0.08

# Icon Positioning
ICON_OFFSET_Y = GRID_SIZE // 2
ICON_SIZE = GRID_SIZE // 2

# Creature Feature Dimensions - Eyes
EYE_SIZE = 3
EYE_SPACING = 6
EYE_OFFSET_Y = 2
PUPIL_SIZE = 2
PUPIL_RANGE = 2
BLINK_INTERVAL = 5
BLINK_DURATION = 1

# Creature Feature Dimensions - Antennae
ANTENNA_LENGTH = 8
ANTENNA_WIDTH = 2
ANTENNA_SPACING = 6
ANTENNA_WAVE_SPEED = 0.25
ANTENNA_WAVE_AMOUNT = 0.5

# Creature Feature Dimensions - Mouth
MOUTH_WIDTH = 8
MOUTH_HEIGHT = 4
MOUTH_Y_OFFSET = -8
MOUTH_OPEN_SPEED = 0.1
MAX_MOUTH_OPEN = 6
SMILE_CURVE = 3

# Egg Visualization
EGG_PULSE_SPEED = 2.0
EGG_INNER_RATIO = 0.7
EGG_SHINE_OFFSET = 0.3

# Creature Appearance Patterns
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

# UI Status Bar Configuration
STAT_BAR_HEIGHT = 15
STAT_BAR_PADDING = 5
STAT_BAR_COLORS = {
    'health': (255, 50, 50),      # Red
    'energy': (50, 150, 255),     # Blue
    'hunger': (255, 200, 50),     # Yellow
    'happiness': (255, 100, 255),  # Pink
    'age': (100, 255, 100),       # Green
    'decomposition': (139, 69, 19),# Brown
    'food': (255, 165, 0)         # Orange
}

# Age Stage Colors
age_colors = {
    "young_adult": (0, 255, 0),
    "middle_age": (255, 255, 0),
    "elder": (255, 0, 0)
}

# Common Color Presets
semi_transparent = 230
critical_color = (255, 0, 0, 200)
selection_color = (255, 255, 255, 180)
base_creature_color = (0, 255, 0)

# Simulation Rate Constants
DECOMPOSITION_RATE = 0.1
MAX_DECOMPOSITION = 100
MAX_FERTILITY = 100
GRASS_GROWTH_RATE = 0.1
FERTILITY_SPREAD_RATE = 0.05
GRASS_SPREAD_CHANCE = 0.01

# Egg Constants
EGG_HATCH_TIME = 300  # Time until egg hatches
EGG_NEARBY_PARENT_RANGE = 3  # Range to check for parent creatures

# Environment Area Scaling
MAX_AREA_SCALE = 1.5
AREA_SCALE_FACTOR = 0.3

# Movement Constants
DIAGONAL_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
CARDINAL_MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Egg Finding Range
EGG_SPOT_SEARCH_RANGE = 4  # Maximum distance to search for egg spots