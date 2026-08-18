import ctypes

ctypes.windll.user32.MessageBoxW(0, "Hello, World!", "Hello, World!", 0x00000000 | 0x40)