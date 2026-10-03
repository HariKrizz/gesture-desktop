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
        self.min_x = margin_x
        self.max_x = camera_width - margin_x

        self.min_y = margin_y
        self.max_y = camera_height - margin_y

        # smoothing factor for cursor movement
        self.smooth_factor = smooth_factor

        self.prev_x = None
        self.prev_y = None

    def map_position(self, x, y):
        # Clamp the x and y values to the defined margins
        x = max(self.min_x, min(x, self.max_x))
        y = max(self.min_y, min(y, self.max_y))

        # Convert camera coordinates to 0-1
        normalized_x = (
            (x - self.min_x)
            / (self.max_x - self.min_x)
        )

        normalized_y = (
            (y - self.min_y)
            / (self.max_y - self.min_y)
        )

        # Convert 0-1 to screen coordinates
        screen_x = normalized_x * self.screen_width
        screen_y = normalized_y * self.screen_height

        if self.prev_x == None:
            self.prev_x = screen_x
            self.prev_y = screen_y

        # Apply smoothing
        smoothed_screen_x = int(
            self.prev_x + (screen_x - self.prev_x) * self.smooth_factor
        )

        smoothed_screen_y = int(
            self.prev_y + (screen_y - self.prev_y) * self.smooth_factor
        )

        self.prev_x = smoothed_screen_x
        self.prev_y = smoothed_screen_y

        return smoothed_screen_x, smoothed_screen_y 