import cv2
import time
import numpy as np

from mediapipe import Image, ImageFormat

from hand_tracking.detector import createDetector
from hand_tracking.tracking import *
from hand_tracking.gestures import *
from hand_tracking.camera_switcher import CameraSwitcher
from vfx.filters import *
from vfx.filters import *
from vfx.masks import *
from state.hand_state import *
from state.app_state import *
from config import *

def main():    
    # ===VARS===
    height, width = 0, 0
    
    # ===SETUP===
    detector = createDetector(MODEL_PATH, MIN_DETECTION_CONF, MIN_PRESENCE_CONF, MIN_TRACKING_CONF)
    
    camera = CameraSwitcher()
    
    start_time = time.time()
    
    app_state = AppState()
    app_state.setupInput()

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)

        timestamp_ms = int((time.time() - start_time) * 1000)

        result = detector.detect_for_video(mp_image, timestamp_ms)

        hands = getHands(result, width, height)

        for handedness, hand in hands.items():

            state = hand_states[handedness]

            closed = isClosed(hand)

            if closed:
                state.open_frames = 0

                if state.save_armed:
                    state.saved_position = hand.copy()
                    state.save_armed = False

            else:
                state.open_frames += 1

                if state.open_frames > 10:
                    state.save_armed = True
                    state.saved_position = None


        quad1 = getQuad(hands, (4, 8), (4, 8))
        quad2 = getQuad(hands, (8, 12), (8, 12))
        quad3 = getQuad(hands, (12, 16), (12, 16))


        hex1 = getHex(hands, [4, 12, 20], [4, 12, 20])

        saved_hand_pos_left = hand_states["Left"].saved_position

        mask1 = np.zeros((height, width), dtype=np.uint8)
        mask2 = np.zeros_like(mask1)
        mask3 = np.zeros_like(mask1)

        outFrame = frame.copy()
        
        if app_state.mode == 1:

            if quad1 is not None:
                cv2.fillPoly(mask1 , [quad1], 255)

                cv2.polylines(outFrame, [quad1], True, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                a = applyFilter(frame, ['glass', 'chroma'])

                outFrame = applyMask(outFrame, a, mask1)

            if quad2 is not None:
                cv2.fillPoly(mask2 , [quad2], 255)

                cv2.polylines(outFrame, [quad2], True, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                a = applyFilter(frame, ['invert'])

                outFrame = applyMask(outFrame, a, mask2)

            if quad3 is not None:
                cv2.fillPoly(mask3 , [quad3], 255)

                cv2.polylines(outFrame, [quad3], True, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                a = applyFilter(frame, ['edge'])

                outFrame = applyMask(outFrame, a, mask3)

        if app_state.mode == 3:
            hex1 = getTempHex(hands, "Left", saved_hand_pos_left, [4, 12, 20], [4, 12, 20])

        if app_state.mode == 2 or app_state.mode == 3:
            if hex1 is not None:
                cv2.fillPoly(mask1 , [hex1], 255)

                cv2.polylines(outFrame, [hex1], True, (255, 255, 255), 2, lineType=cv2.LINE_AA)

                a = applyFilter(frame, ['glass', 'chroma'])

                outFrame = applyMask(outFrame, a, mask1)

        
        cv2.imshow("ephemera", outFrame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()