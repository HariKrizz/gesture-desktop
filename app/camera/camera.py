import cv2

from app.config.settings import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
)


class Camera:

    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cap.isOpened():
            raise RuntimeError(
                "Could not open webcam."
            )

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH,
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT,
        )

    def read(self):
        """
        Read one frame from the webcam.

        Returns:
            success, frame
        """

        success, frame = self.cap.read()

        if not success:
            return False, None

        # Mirror the camera image
        frame = cv2.flip(frame, 1)

        return True, frame

    def release(self):
        """Release the webcam."""
        self.cap.release()