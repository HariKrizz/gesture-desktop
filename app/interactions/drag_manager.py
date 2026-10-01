class DragManager:
    def __init__(self, mouse_controller):
        self.dragging = False
        self.pinching = False
        self.mouse_controller = mouse_controller


    def update(self, is_pinching) -> None:
        pinch_started = is_pinching and not self.pinching
        if pinch_started:
            if not self.dragging:
                self.mouse_controller.mouse_down()
                self.dragging = True
            else:
                self.mouse_controller.mouse_up()
                self.dragging = False

        self.pinching = is_pinching

    def is_dragging(self) -> bool:
        return self.dragging

    def release(self) -> None:
        if self.dragging:
            self.mouse_controller.mouse_up()
            self.dragging = False
        
        self.pinching = False
    