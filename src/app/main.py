# Imports
from ctypes import wintypes
import pygame.freetype
import pygame
import ctypes
import json
import sys
import os

# Functions
def show_text(message="Text", title="Text", up=False):
    if up:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40000)
    else:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x0)

def show_info(message="Information", title="Info", up=False):
    if up:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40040)
    else:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)

def show_warning(message="Warning", title="Warning", up=False):
    if up:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40030)
    else:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x30)

def show_error(message="Error!", title="Error", up=True):
    if up:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40010)
    else:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)

def get_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        show_error(f"An unknown error occured while reading the {filename} file!", "Unknown file read error")
        return None

def save_data(filename, to_save):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(to_save, file, ensure_ascii=False, indent=4)
    except:
        show_error(f"An unknown error occured while writing the {filename} file!", "Unknown file write error")

# Checking system requirements
if sys.maxsize > 2**32:
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", wintypes.DWORD),
            ("dwMemoryLoad", wintypes.DWORD),
            ("ullTotalPhys", ctypes.c_uint64),
            ("ullAvailPhys", ctypes.c_uint64),
            ("ullTotalPageFile", ctypes.c_uint64),
            ("ullAvailPageFile", ctypes.c_uint64),
            ("ullTotalVirtual", ctypes.c_uint64),
            ("ullAvailVirtual", ctypes.c_uint64),
            ("ullAvailExtendedVirtual", ctypes.c_uint64),
        ]
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    RAM = round(stat.ullTotalPhys / (1024 ** 3))
else:
    class MEMORYSTATUS(ctypes.Structure):
        _fields_ = [
            ("dwLength", wintypes.DWORD),
            ("dwMemoryLoad", wintypes.DWORD),
            ("ullTotalPhys", ctypes.c_size_t),
            ("ullAvailPhys", ctypes.c_size_t),
            ("ullTotalPageFile", ctypes.c_size_t),
            ("ullAvailPageFile", ctypes.c_size_t),
            ("ullTotalVirtual", ctypes.c_size_t),
            ("ullAvailVirtual", ctypes.c_size_t),
        ]
    stat = MEMORYSTATUS()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    RAM = round(stat.ullTotalPhys / (1024 ** 3))

class OSVERSIONINFOEXW(ctypes.Structure):
    _fields_ = [
        ("dwOSVersionInfoSize", wintypes.DWORD),
        ("dwMajorVersion", wintypes.DWORD),
        ("dwMinorVersion", wintypes.DWORD),
        ("dwBuildNumber", wintypes.DWORD),
        ("dwPlatformId", wintypes.DWORD),
        ("szCSDVersion", wintypes.WCHAR * 128),
        ("wServicePackMajor", wintypes.WORD),
        ("wServicePackMinor", wintypes.WORD),
        ("wSuiteMask", wintypes.WORD),
        ("wProductType", ctypes.c_byte),
        ("wReserved", ctypes.c_byte),
    ]

    def __init__(self):
        super().__init__()
        self.dwOSVersionInfoSize = ctypes.sizeof(self)

os_info = OSVERSIONINFOEXW()

ctypes.windll.ntdll.RtlGetVersion(ctypes.byref(os_info))

NT_VERSION = f"{os_info.dwMajorVersion}.{os_info.dwMinorVersion}"

if RAM > 2 and os_info.dwMajorVersion < 6 and os_info.dwMinorVersion < 1:
    show_warning("Your device may not compatible with this game;play at your own risk.", "Warning!", True)

# Constants
DATA_FILE = "saves.json"
ORIGINAL_DATA = {
    "settings": 
        {
            "fullscreen": False
        }
}
FILES_TABLE =  [
    "icon.ico",
    "resources/fonts/Minecraftia-Regular.ttf"
]
GAMENAME = "Parkour Survival"
GAMEVER = "v1.0.0"

# Varialbles
data = None
save_delay = 0
is_fullscreen = False
fullscreen_delay = 0
scene = "menu"

# Checking files
for file in FILES_TABLE:
    if not os.path.isfile(file):
        show_error(f"The {file} file required for the game to launch the game is missing!", "File not found")
        sys.exit(1)

# Checking data file
if not os.path.isfile(DATA_FILE):
    save_data(DATA_FILE, ORIGINAL_DATA)
    data = get_data(DATA_FILE)
else:
    data = get_data(DATA_FILE)
    is_fullscreen = data["settings"]["fullscreen"]

# Initializing pygame
pygame.init()

# Resize varialbles
width, height = 640, 480

# Creating window
if is_fullscreen:
    display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.FULLSCREEN)
else:
    display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.RESIZABLE)

# Resources
# Fonts
Minecraftia_Font = pygame.freetype.Font("resources/fonts/Minecraftia-Regular.ttf")
# Images
Icon_Image = pygame.image.load("icon.ico").convert_alpha()

# Buttons
play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render("Play!", size=32, fgcolor=(255, 255, 255))
play_menu_btn_rect.topleft = (16, 64)

# Resizable, caption & icon settings.
screen = pygame.Surface((width, height))
pygame.display.set_caption(f"{GAMENAME} {GAMEVER}")
pygame.display.set_icon(Icon_Image)

# FPS Clocks
fps = pygame.time.Clock()

# Always cycle
while True:
    # Getting mouse pos
    mouse = pygame.mouse.get_pos()
    # Cleaning window
    screen.fill((0, 0, 0))
    # Menu scene
    if scene == "menu":
        # Texts & icon
        screen.blit(Icon_Image, (16, 16))
        Minecraftia_Font.render_to(screen, (64, 16), GAMENAME, size=32, fgcolor=(255, 255, 255))
        Minecraftia_Font.render_to(screen, (382, 48), GAMEVER, size=8, fgcolor=(255, 255, 255))
        # Buttons
        screen.blit(play_menu_btn, play_menu_btn_rect)
        if play_menu_btn_rect.collidepoint(mouse):
            play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render("Play!", size=36, fgcolor=(0, 255, 0))
            play_menu_btn_rect.topleft = (16, 64)
            if pygame.mouse.get_pressed()[0]:
                pass
        else:
            play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render("Play!", size=32, fgcolor=(255, 255, 255))
            play_menu_btn_rect.topleft = (16, 64)
    scaled_display = pygame.transform.scale(screen, (width, height))
    # Bliting image to window
    display.blit(scaled_display, (0, 0))
    # Updating window
    pygame.display.flip()
    # Set FPS to 60
    fps.tick(60)
    # Fullscreen delay 
    if not fullscreen_delay == 0:
        fullscreen_delay -= 1
    # Save data & delay
    if not save_delay == 0:
        save_delay -= 1
    else:
        save_data(DATA_FILE, data)
        save_delay = 900
    # Event cycle
    for event in pygame.event.get():
        # Window resizing
        if event.type == pygame.VIDEORESIZE:
            width, height = max(event.w, 640), max(event.h, 480)
            display = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.HWSURFACE)
            pygame.display.set_caption(f"{GAMENAME} {GAMEVER}")
            pygame.display.set_icon(Icon_Image)
        # Keydown actions
        if event.type == pygame.KEYDOWN:
            # F11
            if event.key == pygame.K_F11:
                # Fullscreen actions
                if not is_fullscreen and fullscreen_delay == 0:
                    is_fullscreen = True
                    fullscreen_delay = 180
                    display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.FULLSCREEN)
                    pygame.display.set_caption(f"{GAMENAME} {GAMEVER}")
                    pygame.display.set_icon(Icon_Image)
                elif is_fullscreen and fullscreen_delay == 0:
                    is_fullscreen = False
                    display = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.HWSURFACE)
                    pygame.display.set_caption(f"{GAMENAME} {GAMEVER}")
                    pygame.display.set_icon(Icon_Image)
                    fullscreen_delay = 180
                data["settings"]["fullscreen"] = is_fullscreen
            # F2
            if event.key == pygame.K_F2:
                save_data(DATA_FILE, data)
        # On exit
        if event.type == pygame.QUIT:
            save_data(DATA_FILE, data)
            sys.exit(0)