# Imports
from ctypes import wintypes
import pygame.freetype
import subprocess
import pygame
import ctypes
import json
import sys
import os

# Loading dlls
localization_dll = ctypes.CDLL(".\localization.dll")
localization_dll.get_localized_string.restype = ctypes.c_wchar_p

# Functions
def get_localization_resource(language, resource):
    global localization_dll
    return localization_dll.get_localized_string(ctypes.c_wchar_p(resource), ctypes.c_wchar_p(language))

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

def exit():
    save_data(DATA_FILE, data)
    sys.exit(0)

def restart():
    save_data(DATA_FILE, data)
    subprocess.Popen([sys.executable] + sys.argv)
    pygame.event.post(pygame.event.Event(pygame.QUIT))


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
    show_warning("Your device may not compatible with this game; play at your own risk.", "Warning!", True)

# Constants
DATA_FILE = "saves.json"
ORIGINAL_DATA = {
    "settings": 
        {
            "fullscreen": False,
            "lang": "english"
        }
}
FILES_TABLE =  [
    "icon.ico",
    "resources/fonts/Minecraftia-Regular.ttf",
    "resources/images/checkbox_off.png",
    "resources/images/checkbox_on.png",
    "resources/images/back.png",
    "resources/images/back_highlight.png"
]
GAMENAME = "Parkour Survival"
GAMEVER = "v1.0.0"

# Varialbles
data = None
save_delay = 0
is_fullscreen = False
fullscreen_delay = 0
scene = "menu"
is_clicked = False

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

# Checking localization
if get_localization_resource("english", "menu.play_btn") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("russian", "menu.play_btn") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("english", "menu.settings_btn") == "NULLABLE":
    show_error("Localization is not valid!",  "Localization error")
    sys.exit(1)
elif get_localization_resource("russian", "menu.settings_btn") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("english", "settings.name") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("russian", "settings.name") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("english", "settings.lang_text") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("russian", "settings.lang_text") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("english", "settings.lang") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("russian", "settings.lang") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("english", "menu.exit_btn") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)
elif get_localization_resource("russian", "menu.exit_btn") == "NULLABLE":
    show_error("Localization is not valid!", "Localization error")
    sys.exit(1)


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
Checkbox_Off_Image = pygame.transform.scale(pygame.image.load("resources/images/checkbox_off.png").convert_alpha(), (32, 32))
Checkbox_On_Image = pygame.transform.scale(pygame.image.load("resources/images/checkbox_on.png").convert_alpha(), (32, 32))
Back_Image = pygame.transform.scale(pygame.image.load("resources/images/back.png").convert_alpha(), (32, 32))
Back_Highlight_Image = pygame.transform.scale(pygame.image.load("resources/images/back_highlight.png").convert_alpha(), (32, 32))

# Buttons
if data["settings"]["lang"] == "russian":
    play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.play_btn"), size=32, fgcolor=(255, 255, 255))
    play_menu_btn_rect.topleft = (16, 64)
    settings_menu_btn, settings_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.settings_btn"), size=32, fgcolor=(255, 255, 255))
    settings_menu_btn_rect.topleft = (16, 64)
    lang_settings_btn, lang_settings_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "settings.lang"), size=32, fgcolor=(255, 255, 255))
    lang_settings_btn_rect.topleft = (128, 64)
    settings_back_btn_rect = Back_Image.get_rect(topleft=(16, 16))
    exit_menu_btn, exit_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.exit_btn"), size=32, fgcolor=(255, 255, 255))
    exit_menu_btn_rect.topleft = (16, 64)
else:
    play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.play_btn"), size=32, fgcolor=(255, 255, 255))
    play_menu_btn_rect.topleft = (16, 64)
    settings_menu_btn, settings_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.settings_btn"), size=32, fgcolor=(255, 255, 255))
    settings_menu_btn_rect.topleft = (16, 64)
    lang_settings_btn, lang_settings_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "settings.lang"), size=32, fgcolor=(255, 255, 255))
    lang_settings_btn_rect.topleft = (128, 64)
    settings_back_btn_rect = Back_Image.get_rect(topleft=(16, 16))
    exit_menu_btn, exit_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.exit_btn"), size=32, fgcolor=(255, 255, 255))
    exit_menu_btn_rect.topleft = (16, 64)

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
    # Scenes
    if scene == "menu":
        # Texts & icon
        screen.blit(Icon_Image, (16, 16))
        Minecraftia_Font.render_to(screen, (64, 16), GAMENAME, size=32, fgcolor=(255, 255, 255))
        Minecraftia_Font.render_to(screen, (382, 48), GAMEVER, size=8, fgcolor=(255, 255, 255))
        # Buttons
        screen.blit(play_menu_btn, play_menu_btn_rect)
        if data["settings"]["lang"] == "russian":
            if play_menu_btn_rect.collidepoint(mouse):
                play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.play_btn"), size=36, fgcolor=(0, 255, 0))
                play_menu_btn_rect.topleft = (16, 64)
                if pygame.mouse.get_pressed()[0]:
                    pass
            else:
                play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.play_btn"), size=32, fgcolor=(255, 255, 255))
                play_menu_btn_rect.topleft = (16, 64)
        else:
            if play_menu_btn_rect.collidepoint(mouse):
                play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.play_btn"), size=36, fgcolor=(0, 255, 0))
                play_menu_btn_rect.topleft = (16, 64)
                if pygame.mouse.get_pressed()[0]:
                    pass
            else:
                play_menu_btn, play_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.play_btn"), size=32, fgcolor=(255, 255, 255))
                play_menu_btn_rect.topleft = (16, 64)
        screen.blit(settings_menu_btn, settings_menu_btn_rect)
        if data["settings"]["lang"] == "russian":
            if settings_menu_btn_rect.collidepoint(mouse):
                settings_menu_btn, settings_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.settings_btn"), size=36, fgcolor=(0, 255, 0))
                settings_menu_btn_rect.topleft = (16, 112)
                if pygame.mouse.get_pressed()[0]:
                    scene = "settings"
            else:
                settings_menu_btn, settings_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.settings_btn"), size=32, fgcolor=(255, 255, 255))
                settings_menu_btn_rect.topleft = (16, 112)
        else:
            if settings_menu_btn_rect.collidepoint(mouse):
                settings_menu_btn, settings_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.settings_btn"), size=36, fgcolor=(0, 255, 0))
                settings_menu_btn_rect.topleft = (16, 112)
                if pygame.mouse.get_pressed()[0]:
                    scene = "settings"
            else:
                settings_menu_btn, settings_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.settings_btn"), size=32, fgcolor=(255, 255, 255))
                settings_menu_btn_rect.topleft = (16, 112)
        if data["settings"]["lang"] == "russian":
            if exit_menu_btn_rect.collidepoint(mouse):
                exit_menu_btn, exit_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.exit_btn"), size=36, fgcolor=(255, 0, 0))
                exit_menu_btn_rect.topleft = (16, 160)
                if pygame.mouse.get_pressed()[0]:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            else:
                exit_menu_btn, exit_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "menu.exit_btn"), size=32, fgcolor=(255, 255, 255))
                exit_menu_btn_rect.topleft = (16, 160)
        else:
            if exit_menu_btn_rect.collidepoint(mouse):
                exit_menu_btn, exit_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.exit_btn"), size=36, fgcolor=(255, 0, 0))
                exit_menu_btn_rect.topleft = (16, 160)
                if pygame.mouse.get_pressed()[0]:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            else:
                exit_menu_btn, exit_menu_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "menu.exit_btn"), size=32, fgcolor=(255, 255, 255))
                exit_menu_btn_rect.topleft = (16, 160)
        screen.blit(exit_menu_btn, exit_menu_btn_rect)  
    elif scene == "settings":
        if data["settings"]["lang"] == "russian":
            Minecraftia_Font.render_to(screen, (64, 16), get_localization_resource("russian", "settings.name"), size=32, fgcolor=(255, 255, 255))
        else:
            Minecraftia_Font.render_to(screen, (64, 16), get_localization_resource("english", "settings.name"), size=32, fgcolor=(255, 255, 255))
        if data["settings"]["lang"] == "russian":
            Minecraftia_Font.render_to(screen, (16, 64), get_localization_resource("russian", "settings.lang_text"), size=32, fgcolor=(255, 255, 255))
        else:
            Minecraftia_Font.render_to(screen, (16, 64), get_localization_resource("english", "settings.lang_text"), size=32, fgcolor=(255, 255, 255))

        # Buttons
        if settings_back_btn_rect.collidepoint(mouse):
            screen.blit(Back_Highlight_Image, (16, 16))
            if pygame.mouse.get_pressed()[0]:
                scene = "menu"
        else:
            screen.blit(Back_Image, (16, 16))
        if lang_settings_btn_rect.collidepoint(mouse):
            if data["settings"]["lang"] == "russian":
                lang_settings_btn, lang_settings_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "settings.lang"), size=32, fgcolor=(0, 255, 0))
                lang_settings_btn_rect.topleft = (128, 64)
            else:
                lang_settings_btn, lang_settings_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "settings.lang"), size=32, fgcolor=(0, 255, 0))
                lang_settings_btn_rect.topleft = (128, 64)
            
            if pygame.mouse.get_pressed()[0]:
                if not is_clicked:
                    if data["settings"]["lang"] == "russian":
                        data["settings"]["lang"] = "english"
                    else:
                        data["settings"]["lang"] = "russian"
                    is_clicked = True
            else:
                is_clicked = False
        else:
            if data["settings"]["lang"] == "russian":
                lang_settings_btn, lang_settings_btn_rect = Minecraftia_Font.render(get_localization_resource("russian", "settings.lang"), size=32, fgcolor=(255, 255, 255))
                lang_settings_btn_rect.topleft = (128, 64)
            else:
                lang_settings_btn, lang_settings_btn_rect = Minecraftia_Font.render(get_localization_resource("english", "settings.lang"), size=32, fgcolor=(255, 255, 255))
                lang_settings_btn_rect.topleft = (128, 64)

        screen.blit(lang_settings_btn, lang_settings_btn_rect)
    else:
        show_error("Invalid scene, The game will be restarted", "Inavlid scene")
        restart()
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
            exit()