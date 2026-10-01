import pyautogui

class MouseController:

    def move_to(self, x, y):
        pyautogui.moveTo(x, y)

    def mouse_down(self):
        pyautogui.mouseDown(button='left')

    def mouse_up(self):
        pyautogui.mouseUp(button='left')

