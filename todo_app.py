# Built in modules
import subprocess
import json
import time
import sys
import os

#  Attempt to import modules, if they're not found, install them
try:
    import pygame as pyg
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pygame"], stdout=subprocess.DEVNULL)
    import pygame as pyg
try:
    from screeninfo import get_monitors
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "screeninfo"], stdout=subprocess.DEVNULL)
    from screeninfo import get_monitors

# Custom modules
import modules.board_c as board_c
import modules.classes as classes
import modules.draw as draw
import modules.typing_handler as typ

# Get screen size based on primary monitor
for m in get_monitors():
    if m.is_primary:
        WIDTH, HEIGHT = m.width, m.height

# Initialize window
pyg.init()
WINDOW = pyg.display.set_mode((WIDTH, HEIGHT))

classes.Globals.WINDOW = WINDOW
classes.Globals.WIDTH = WIDTH
classes.Globals.HEIGHT = HEIGHT
classes.Globals.active_list = -1
classes.Globals.startup_time = time.time() 

pyg.display.set_caption("Todo App")
os.system("cls")

# Main control function
def Main():
    # Local variables
    mouse_pos = (0, 0)

    # Control variables
    clock = pyg.time.Clock()
    FPS = 60

    # Load board from file
    file = json.load(open("storage/workspaces.json", "r"))
    board_dict = file["Your Workspace"]
    classes.Globals.board_dict = board_dict
    board = board_c.Board(board_dict[0]["title"])
    board.position = [300, 100]

    # Create lists
    for list in board_dict[0]["lists"]:
        board.addList(list["title"])
        # Create tasks
        for task in list["tasks"]:
            board.lists[-1].addTask(task["title"], task["desc"])

    # Load settings from file
    settings = json.load(open("storage/settings.json", "r"))
    classes.Globals.settings = settings
    
    quitout_menu = ""

    # Infinite loop
    while True:
        classes.Globals.current_time = time.time()
        # Cursor blinking
        if classes.Globals.cursor_delay > -40:
            classes.Globals.cursor_delay -= 1
        if classes.Globals.cursor_delay == -40:
            classes.Globals.cursor_delay = 40
            
        active_list = classes.Globals.active_list
        # Gets the most recent event (mouse click/movement, key press, etc.)
        for event in pyg.event.get():
            mouse_pos = pyg.mouse.get_pos()
            classes.Globals.mouse_position = mouse_pos

            # Window closed
            if event.type == pyg.QUIT:
                quitout_menu = "exit"

            # Key pressed
            elif event.type == pyg.KEYDOWN:
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                if quitout_menu != "":
                    if key == pyg.K_RETURN:
                        Close(board, quitout_menu)
                    elif key == pyg.K_ESCAPE:
                        quitout_menu = ""
                    
                # Exit key
                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()
                    quitout_menu = "quit"
                
                elif key == pyg.K_F2:
                    quitout_menu = "exit"

                if classes.Globals.editing_task is not None and quitout_menu == "":
                    if classes.Globals.edit_box == "title":
                        classes.Globals.editing_task.title, classes.Globals.cursor = typ.handler(classes.Globals.editing_task.title, key, (shift, caps, ctrl), classes.Globals.cursor)
                    elif classes.Globals.edit_box == "desc":
                        classes.Globals.editing_task.description, classes.Globals.cursor = typ.handler(classes.Globals.editing_task.description, key, (shift, caps, ctrl), classes.Globals.cursor)

                    classes.Globals.cursor_delay = 40
                    

                elif key == pyg.K_LEFTBRACKET and quitout_menu == "":
                    board.menu_collapsed = not board.menu_collapsed

                elif ctrl and quitout_menu == "":
                    # Adding new list
                    if key == pyg.K_n and not shift:
                        board.addList("Example List " + str(len(board.lists) + 1))
                    # Adding new task to the selected list
                    elif key == pyg.K_n and shift and active_list != -1:
                        board.lists[active_list].addTask("Example Task " + str(len(board.lists[active_list].tasks) + 1), "Example Description")
                            
            
            # LMB pressed
            elif event.type == pyg.MOUSEBUTTONDOWN:
                # Close menu
                if quitout_menu != "":
                    # Clicked on yes
                    if CheckCollisions(mouse_pos, box=(WIDTH/2+5, HEIGHT/2-20, 145, 60)):
                        Close(board, quitout_menu)
                    # Clicked on no/outside menu
                    elif CheckCollisions(mouse_pos, box=(WIDTH/2-150, HEIGHT/2-20, 145, 60)) or not CheckCollisions(mouse_pos, box=(WIDTH/2-160, HEIGHT/2-100, 320, 150)):
                        quitout_menu = ""
                else:
                    classes.Globals.mouse_pressed = True
                    ret_dict = board.checkMPress(event.button)
                    if ret_dict is not None:
                        board.title = ret_dict["title"]
                        board.lists.clear()
                        board.position = [300, 100]
                        # Create lists
                        for list in ret_dict["lists"]:
                            board.addList(list["title"])
                            # Create tasks
                            for task in list["tasks"]:
                                board.lists[-1].addTask(task["title"], task["desc"])

            # Mouse unpressed
            elif event.type == pyg.MOUSEBUTTONUP:
                classes.Globals.mouse_pressed = False

            # Mousewheel movement
            elif event.type == pyg.MOUSEWHEEL and quitout_menu == "":
                board.checkMScroll(event.y)
        
        # Refresh screen
        draw.draw(board, quitout_menu)
        classes.Globals.previous_frames += [time.time()]
        if len(classes.Globals.previous_frames) > 60:
            classes.Globals.previous_frames.pop(0)
        clock.tick(FPS)

# Exits the program, saving unless quitout_menu == "quit" (F1 key)
def Close(board, quitout_menu):
    if quitout_menu == "quit":
        pyg.quit()
        sys.exit()

    else:
        print("Saving..")
        output_dict = {"title": board.title, "lists": []}
        for list in board.lists:
            temp_list = {"title": list.title, "tasks": []}
            for task in list.tasks:
                temp_list["tasks"] += [{"title": task.title, "desc": task.description}]

            output_dict["lists"] += [temp_list]

        try:
            file = json.load(open("storage/workspaces.json", "r"))
        except json.decoder.JSONDecodeError:
            file = {}

        for i in range(len(file["Your Workspace"])):
            if file["Your Workspace"][i]["title"] == board.title:
                file["Your Workspace"][i] = output_dict
                with open("storage/workspaces.json", "w") as outfile:
                    outfile.write(json.dumps(file, indent=4))
        pyg.quit()
        sys.exit()


def CheckCollisions(location, box=()):
    '''Returns true if the location collides with the given object'''
    if box != ():
        if box[0] <= location[0] <= box[0] + box[2] and box[1] <= location[1] <= box[1] + box[3]:
            return True
        
    return False

if __name__ == "__main__":
    Main()
