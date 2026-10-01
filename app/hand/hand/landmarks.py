import cv2

WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_DIP = 11
MIDDLE_TIP = 12

RING_MCP = 13
RING_PIP = 14
RING_DIP = 15
RING_TIP = 16

PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20


FINGERTIPS = [
    THUMB_TIP,
    INDEX_TIP,
    MIDDLE_TIP,
    RING_TIP,
    PINKY_TIP,
]


def get_index_tip(landmarks):
    return landmarks[INDEX_TIP]


def get_thumb_tip(landmarks):
    return landmarks[THUMB_TIP]


def landmark_to_pixel(landmark, width, height):
    x = int(landmark.x * width)
    y = int(landmark.y * height)

    return x, y

def draw_landmarks(frame, landmarks):
    """Draws the hand landmarks and connections on the frame."""

    height, width, _ = frame.shape

    # Hand connections
    connections = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),

        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),

        (5, 9),
        (9, 10),
        (10, 11),
        (11, 12),

        (9, 13),
        (13, 14),
        (14, 15),
        (15, 16),

        (13, 17),
        (17, 18),
        (18, 19),
        (19, 20),

        (0, 17),
    ]

    # Draw connections
    for start_idx, end_idx in connections:
        start = landmarks[start_idx]
        end = landmarks[end_idx]

        start_point = (int(start.x * width), int(start.y * height))
        end_point = (int(end.x * width), int(end.y * height))

        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

    # Draw landmarks
    for idx, landmark in enumerate(landmarks):
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        # Slightly enlarge the fingertips
        radius = 7 if idx in [4, 8, 12, 16, 20] else 5
        cv2.circle(frame, (x, y), radius, (0, 0, 255), -1)

        # Display the index of the landmark
        cv2.putText(
            frame,     # Where to draw
            str(idx),  # Text: "0", "1", "2", etc.
            (x + 8, y - 8),  # Text position
            cv2.FONT_HERSHEY_SIMPLEX,  # Font
            0.4,   # Font size
            (255, 255, 255),  # Color: white (BGR)
            1, # Thickness
            cv2.LINE_AA # Antialiased line type
        )
