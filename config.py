from pathlib import Path

BASE_DIR = Path(__file__).parent
MODEL_PATH = str(BASE_DIR / "mediapipe_tasks" / "hand_landmarker.task")

MIN_DETECTION_CONF = 0.3
MIN_PRESENCE_CONF = 0.3
MIN_TRACKING_CONF = 0.3

CAMERA_INDEX = 1