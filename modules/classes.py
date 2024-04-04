# Import statements
import pygame as pyg
import copy
pyg.init()

import modules.chunk_text as chunk_text

class Globals:
    # Display stuff
    cursor = 0
    mouse_position = (0, 0)
    mouse_pressed = False
    WIDTH, HEIGHT = (0, 0)
    WINDOW = 0

    # Timing stuff
    current_time = 0
    cursor_delay = 0
    startup_time = 0
    previous_frames = []

    # Editing stuff
    active_list = -1
    editing_task = None
    edit_box = ""

    board_dict = {}
    hovered_board = {}
    settings = {}

# Class that holds the color theme variables
class DarkMode:
    background = (25, 25, 25)
    hover_color = (100, 100, 100)
    task_color = (60, 60, 60)
    text_color = (255, 255, 255)
    list_color = (40, 40, 40)
    green = (0, 200, 0)
    red = (200, 0, 0)

# Class that holds the font variables
class Fonts:
    board_title_font = pyg.font.SysFont("consolas", 30)
    edit_font = pyg.font.SysFont("consolas", 24)
    list_font = pyg.font.SysFont("consolas", 16)
    task_font = pyg.font.SysFont("consolas", 14)


def checkMCollision(object=None, box=[]):
    '''Returns True if the mouse is colliding with the given object/box'''
    if object is not None:
        if object.position[0] <= Globals.mouse_position[0] <= object.position[0] + object.width and object.position[1] <= Globals.mouse_position[1] <= object.position[1] + object.height:
            return True
            
    elif box[0] <= Globals.mouse_position[0] <= box[0] + box[2] and box[1] <= Globals.mouse_position[1] <= box[1] + box[3]:
        return True

    return False
    