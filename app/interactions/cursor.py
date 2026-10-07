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
        monitors,
        desktop_x,
        desktop_y,
        desktop_width,
        desktop_height,
        # screen_width,
        # screen_height,
        margin_x = 160,
        margin_y = 90,
        smooth_factor = 0.35
    ):
        self.camera_width = camera_width
        self.camera_height = camera_height

        # For monitor awareness
        self.monitors = monitors

        # For multi-monitor support
        self.desktop_x = desktop_x
        self.desktop_y = desktop_y
        self.desktop_width = desktop_width
        self.desktop_height = desktop_height

        # self.screen_width = screen_width
        # self.screen_height = screen_height

        # Control area inside the camera frame
        self.min_x = margin_x
        self.max_x = camera_width - margin_x

        self.min_y = margin_y
        self.max_y = camera_height - margin_y

        # Smoothing factor for cursor movement
        self.smooth_factor = smooth_factor

        self.previous_x = None
        self.previous_y = None

    def map_position(self, x, y):

        # Clamping the x and y for camera frame margins.
        x = max(self.min_x, min(x, self.max_x))
        y = max(self.min_y, min(y, self.max_y))

        # Normalizing the camera co-ordinates.
        normalized_x = (
            (x - self.min_x)
            / (self.max_x - self.min_x)
        )

        normalized_y = (
            (y - self.min_y)
            / (self.max_y - self.min_y)
        )

        # Maps the normalized hand position onto the entire virtual desktop
        desktop_x = (
            self.desktop_x
            + normalized_x * self.desktop_width
        )

        # Find the active monitor based on the desktop_x and desktop_y coordinates
        active_monitor = self._get_monitor_x(desktop_x)

        if active_monitor:
            desktop_y = (
                active_monitor["y"]
                + normalized_y * active_monitor["height"]
            )
        else:
            # Fallback to virtual desktop
            desktop_y = (
                self.desktop_y
                + normalized_y * self.desktop_height
            )

        # Initialize the smoothing variables if they are None
        if self.previous_x is None:
            self.previous_x = desktop_x
            self.previous_y = desktop_y

        smoothed_x = (
            self.previous_x
            + (desktop_x - self.previous_x)
            * self.smooth_factor
        )

        smoothed_y = (
            self.previous_y
            + (desktop_y - self.previous_y)
            * self.smooth_factor
        )

        self.previous_x = smoothed_x
        self.previous_y = smoothed_y

        return int(smoothed_x), int(smoothed_y)

    def _get_monitor_x(self, desktop_x):
        """
        Returns the monitor that contains the given desktop_x coordinate.
        If no monitor is found, returns None.
        """
        for monitor in self.monitors:
            monitor_left = monitor["x"]
            monitor_right = monitor["x"] + monitor["width"]

            if monitor_left <= desktop_x < monitor_right:
                return monitor
        return None