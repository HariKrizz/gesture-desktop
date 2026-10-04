from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# MediaPipe model
MODEL_PATH = BASE_DIR / "models" / "hand_landmarker.task"

# Application window
WINDOW_NAME = "Gesture Recognition."

# Camera settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# PINCH detection settings
PINCH_THRESHOLD = 60.0

# Cursor calibration settings
CURSOR_MARGIN_X = 160
CURSOR_MARGIN_Y = 90
CURSOR_SMOOTH_FACTOR = 0.35
