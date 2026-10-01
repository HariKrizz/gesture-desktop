from pathlib import Path

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from app.config.settings import MODEL_PATH

class HandDetector:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Hand Landmarker model not found. Expected location: {MODEL_PATH}"
            )
        
        # MediaPipe Hand Landmarker configuration
        base_options = python.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame, timestamp):

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe Image from the RGB frame
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Perform hand detection and return the detection result
        return self.detector.detect_for_video(
            mp_image, 
            timestamp
        )

    def close(self):
        """Release MediaPipe detector."""
        self.detector.close()