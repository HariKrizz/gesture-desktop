import cv2
import math
import time

import pyautogui

from app.camera.camera import Camera
from app.hand.gestures import is_pinching
from app.hand.detector import HandDetector
from app.config.settings import CAMERA_HEIGHT, CAMERA_WIDTH, WINDOW_NAME

from app.interactions.drag_manager import DragManager
from app.mouse.controller import MouseController
from app.interactions.cursor import CursorMapper

from app.hand.landmarks import (
    draw_landmarks,
    get_index_tip,
    get_thumb_tip,
    landmark_to_pixel
)

def main():

    try:
        camera = Camera()
        detector = HandDetector()
        screen_width, screen_height = pyautogui.size()
    except (RuntimeError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        return

    frame_timestamp = 0
    previous_time = time.perf_counter()

    cursor_mapper = CursorMapper(
        CAMERA_WIDTH, 
        CAMERA_HEIGHT, 
        screen_width, 
        screen_height
    )

    mouse_controller = MouseController()

    drag_manager = DragManager(mouse_controller)

    print("\n======================================\n")
    print(" Hand Gesture Desktop\n")
    print("======================================\n")
    print("Hand tracking started.")
    print("Press Q to quit.\n")


    while True:
        # Read a frame from the camera
        success, frame = camera.read()

        if not success:
            print("Failed to read from camera.")
            break

        # Get the current timestamp in milliseconds
        frame_timestamp += 1

        # Detect hands in the frame
        detection_result = detector.detect(frame, frame_timestamp)

        # If hands are detected, process the landmarks
        if detection_result.hand_landmarks:

            for hand_landmarks in detection_result.hand_landmarks:
                # Draw hand skeleton on the frame
                draw_landmarks(frame, hand_landmarks)

                # Get important landmarks (index finger tip and thumb tip)
                index_tip = get_index_tip(hand_landmarks)
                thumb_tip = get_thumb_tip(hand_landmarks)

                height, width, _ = frame.shape

                index_x, index_y = landmark_to_pixel(
                    index_tip,
                    width,
                    height
                )

                thumb_x, thumb_y = landmark_to_pixel(
                    thumb_tip,
                    width,
                    height
                )

                # Screen mapping for the index finger tip
                screen_x, screen_y = cursor_mapper.map_position(index_x, index_y)
                mouse_controller.move_to(screen_x, screen_y)

                # Draw circles on the index and thumb tips (debugging purposes)
                cv2.circle(
                    frame,
                    (index_x, index_y),
                    10,
                    (255, 0, 0),
                    2
                )

                # Show co-ordinates of the index and thumb with distance between them
                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

                # Check if the pinch gesture is detected
                pinching = is_pinching(distance)
                drag_manager.update(pinching)

                # Show the distance between the index and thumb
                cv2.putText(
                    frame,
                    f"""Index: ({index_x}, {index_y}) | Thumb: ({thumb_x}, {thumb_y}) | Distance: {distance:.1f} | Pinching: {"YES" if pinching else "NO"} | Dragging: {"YES" if drag_manager.is_dragging() else "NO"}""",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA,
                )

        # FPS calculation
        current_time = time.perf_counter()
        elapsed_time = current_time - previous_time
        if elapsed_time > 0:
            fps = 1 / elapsed_time
        else:
            fps = 0
        previous_time = current_time

        # Show information on the frame
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

        # Display the frame
        cv2.imshow(WINDOW_NAME,frame)

        # Exit if 'Q or q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key in [ord("q"), ord("Q")]:
            break

    # Cleanup resources
    drag_manager.release()
    
    camera.release()
    detector.close()
    cv2.destroyAllWindows()

    print("\nHand tracking stopped.")

if __name__ == "__main__":
    main()