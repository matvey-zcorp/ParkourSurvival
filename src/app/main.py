# Imports
import pygame
import ctypes
import sys
import os

# Message Boxes
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

# Checking files
files_table =  ["icon.ico"]
for file in files_table:
    if not os.path.isfile(file):
        show_error("A file required for the game to run is missing!", "File not found")
        sys.exit(1)

# Initializing pygame
pygame.init()

# Resize varialbles
width, height = 640, 480
MAIN_WIDTH, MAIN_HEIGHT = 640, 480

# Creating window
display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.RESIZABLE)
screen = pygame.Surface((width, height))
pygame.display.set_caption("Parkour Survival")
pygame.display.set_icon(pygame.image.load("icon.ico").convert_alpha())

# Fullscreen varialbles
is_fullscreen = False
fullscreen_delay = 0

# FPS Clocks
fps = pygame.time.Clock()

# Always cycle
while True:
    # Cleaning window
    screen.fill((0, 0, 0))
    # Test circle
    pygame.draw.circle(screen, (0, 0, 255), (320, 240), 100)
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
    # Event cycle
    for event in pygame.event.get():
        # Window resizing
        if event.type == pygame.VIDEORESIZE:
            width, height = max(event.w, 640), max(event.h, 480)
            display = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.HWSURFACE)
        # Keydown actions
        if event.type == pygame.KEYDOWN:
            # F11
            if event.key == pygame.K_F11:
                # Fullscreen actions
                if not is_fullscreen and fullscreen_delay == 0:
                    is_fullscreen = True
                    fullscreen_delay = 180
                    display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.FULLSCREEN)
                    pygame.display.set_caption("Parkour Survival")
                    pygame.display.set_icon(pygame.image.load("icon.ico").convert_alpha())
                elif is_fullscreen and fullscreen_delay == 0:
                    is_fullscreen = False
                    display = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.HWSURFACE)
                    pygame.display.set_caption("Parkour Survival")
                    pygame.display.set_icon(pygame.image.load("icon.ico").convert_alpha())
        # On exit
        if event.type == pygame.QUIT:
            sys.exit(0)