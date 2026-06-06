from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def createDetector(model_path, min_hand_detection_confidence, min_hand_presence_confidence, min_tracking_confidence):

  BaseOptions = python.BaseOptions
  HandLandmarker = vision.HandLandmarker
  HandLandmarkerOptions = vision.HandLandmarkerOptions
  VisionRunningMode = vision.RunningMode

  options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2,

    min_hand_detection_confidence=min_hand_detection_confidence,
    min_hand_presence_confidence=min_hand_presence_confidence,
    min_tracking_confidence=min_tracking_confidence   
  )

  return vision.HandLandmarker.create_from_options(options)