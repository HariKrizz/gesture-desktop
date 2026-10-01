class CursorMapper:

    """
    Maps the cursor position from the camera to the screen.
    The calculation is based on the camera and screen dimensions.
    This helps in mapping the cursor position more accurately.
    """

    def __init__(
        self,
        camera_width,
        camera_height,
        screen_width,
        screen_height,
        margin_x = 160,
        margin_y = 90,
        smooth_factor = 0.35
    ):
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # control area inside the camera frame
        self.margin_x = margin_x
        self.max_x = camera_width - margin_x
        self.margin_y = margin_y
        self.max_y = camera_height - margin_y

        # smoothing factor for cursor movement
        self.smooth_factor = smooth_factor

        self.prev_x = 0
        self.prev_y = 0

    def map_position(self, x, y):
        screen_x = int(
            x / self.camera_width * self.screen_width
        )

        screen_y = int(
            y / self.camera_height * self.screen_height
        )

        return screen_x, screen_y