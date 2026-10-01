import time
import cv2

from hand.landmarks import (
    get_index_tip, 
    get_thumb_tip, 
    landmark_to_pixel
)