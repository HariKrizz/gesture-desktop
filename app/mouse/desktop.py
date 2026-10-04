import ctypes

class Desktop:

    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79

    def __init__(self):
        self.user32 = ctypes.windll.user32
        
        self.screen_width = self.user32.GetSystemMetrics(self.SM_CXVIRTUALSCREEN)
        self.screen_height = self.user32.GetSystemMetrics(self.SM_CYVIRTUALSCREEN)
        
        self.x = self.user32.GetSystemMetrics(self.SM_XVIRTUALSCREEN)
        self.y = self.user32.GetSystemMetrics(self.SM_YVIRTUALSCREEN)

    def get_bounds(self):
        return (self.x, self.y, self.screen_width, self.screen_height)

    def print_info(self):
        print("\n======================================")
        print(" Virtual Desktop")
        print("======================================")
        print(f"X      : {self.x}")
        print(f"Y      : {self.y}")
        print(f"Width  : {self.screen_width}")
        print(f"Height : {self.screen_height}")
        print("======================================\n")

if __name__ == "__main__":
    desktop = Desktop()
    desktop.print_info()