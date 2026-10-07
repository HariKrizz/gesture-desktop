class DragManager:

    HAND_MISSING_THRESHOLD = 5  # Number of frames to wait before releasing drag

    def __init__(self, mouse_controller):
        self.dragging = False
        self.was_pinching = False
        self.hand_missing_frames = 0
        self.mouse_controller = mouse_controller

        # After an automatic release, do not immediately
        # start another drag if the hand comes back still pinching.
        self.waiting_for_pinch_release = False


    def update(self, pinching, hand_found=True) -> None:
        
        # Hand missing logic
        if not hand_found:
            self.hand_missing_frames += 1
            if self.hand_missing_frames >= self.HAND_MISSING_THRESHOLD:
                if self.dragging:
                    self.mouse_controller.mouse_up()
                    self.dragging = False
                
                self.was_pinching = False

                # Avoid immediate re-drag if hand comes back still pinching.
                self.waiting_for_pinch_release = True

            return

        # Hand present logic
        self.hand_missing_frames = 0

        # Wait to release the pinch gesture
        if self.waiting_for_pinch_release:
            if not pinching:
                self.waiting_for_pinch_release = False

            self.was_pinching = pinching
            return
        
        # Pinch and select logic
        pinch_started = pinching and not self.was_pinching
        if pinch_started:
            if not self.dragging:
                self.mouse_controller.mouse_down()
                self.dragging = True
                print("Drag started.")
            else:
                self.mouse_controller.mouse_up()
                self.dragging = False
                print("Drag stopped.")

        self.pinching = pinching

    def is_dragging(self) -> bool:
        return self.dragging

    def release(self) -> None:
        """
        Normal cleanup.
        Always make sure the left mouse button is released.
        """
        if self.dragging:
            self.mouse_controller.mouse_up()
            print("Mouse button released in normal cleanup.")
        
        self.dragging = False
        self.was_pinching = False
        self.hand_missing_frames = 0
        self.waiting_for_pinch_release = False

    def emergency_release(self) -> None:
        """
        Emergency cleanup.
        Always make sure the left mouse button is released.
        """
        if self.dragging:
            self.mouse_controller.mouse_up()
            print("Mouse button released in emergency cleanup.")

        self.dragging = False
        self.was_pinching = False
        self.hand_missing_frames = 0
        self.waiting_for_pinch_release = False
    