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

        # Individual Monitors
        self.monitors = []
        self._get_monitors()

    # retrieve the position and dimensions of all monitors on a Windows desktop
    def _get_monitors(self):
        
        class RECT(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)
            ]

        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", ctypes.c_ulong)
            ]

        monitor_enum_proc = ctypes.WINFUNCTYPE(
            ctypes.c_bool,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.POINTER(RECT),
            ctypes.c_double
        )

        def monitor_callback(h_monitor, hdc_monitor, lprc_monitor, data):
            monitor_info = MONITORINFO()
            monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
            result = self.user32.GetMonitorInfoW(h_monitor, ctypes.byref(monitor_info))

            if result:
                rect = monitor_info.rcMonitor
                self.monitors.append({
                    "x": rect.left,
                    "y": rect.top,
                    "width": rect.right - rect.left,
                    "height": rect.bottom - rect.top
                })
            return 1

        callback = monitor_enum_proc(monitor_callback)
        self.user32.EnumDisplayMonitors(None, None, callback, 0)

    def get_bounds(self):
        return (self.x, self.y, self.screen_width, self.screen_height)

    def print_info(self):
        print("\n======================================")
        print(" Monitors")
        print("======================================")

        for index, monitor in enumerate(self.monitors, start=1):
            print(f"Monitor {index}")
            print(f"X      : {monitor['x']}")
            print(f"Y      : {monitor['y']}")
            print(f"Width  : {monitor['width']}")
            print(f"Height : {monitor['height']}")
            print("--------------------------------------")

        print("Virtual Desktop")
        print("--------------------------------------")
        print(f"X      : {self.x}")
        print(f"Y      : {self.y}")
        print(f"Width  : {self.screen_width}")
        print(f"Height : {self.screen_height}")
        print("======================================\n")

if __name__ == "__main__":
    desktop = Desktop()
    desktop.print_info()