# Import statements
import pygame as pyg

import modules.classes as classes
import modules.chunk_text as chunk_text

Globals = classes.Globals

# Controls the drawing to the screen
def draw(board, quitout_menu):
    mouse_pos = Globals.mouse_position
    Globals.WINDOW.fill(classes.DarkMode.background)
    board.draw()

    # Draw editing pane if a task is being edited
    if Globals.editing_task is not None:
        # Editing pane
        task = Globals.editing_task
        top, left = Globals.HEIGHT/2 - 400,  Globals.WIDTH/2 - 300
        width, height = 600, 800
        pyg.draw.rect(Globals.WINDOW, classes.DarkMode.hover_color, (left, top, width, height), border_radius=10)
        pyg.draw.rect(Globals.WINDOW, classes.DarkMode.list_color, (left + 4, top + 4, width-8, height-8), border_radius=10)

        # Title
        title_text = chunk_text.Chunk(task.title, content_width=width-70, char_size=classes.Fonts.edit_font.size("A")[0])

        if (CheckCollisions(mouse_pos, box=(left + 10, top + 25, width - 60, max(45 + (len(title_text) - 1) * 25, 45))) or classes.Globals.edit_box == "title"):
            color = classes.DarkMode.hover_color
        else:
            color = classes.DarkMode.task_color
        
        pyg.draw.rect(Globals.WINDOW, color, (left + 10, top + 25, width - 60, max(45 + (len(title_text) - 1) * 25, 45)), border_radius=5)
        for i in range(len(title_text)):
            Globals.WINDOW.blit(classes.Fonts.edit_font.render(title_text[i].replace("\n", ""), True, classes.DarkMode.text_color), (left + 20, top + 35 + i * 25))

        if classes.Globals.edit_box == "title" and classes.Globals.cursor_delay > 0:
            cursor = classes.Globals.cursor
            cursor_y = 0
            offset_w = 0
            for line in title_text:
                if cursor > len(line) and len(line) != 0:
                    cursor_y += 1
                    cursor -= len(line)
                else:
                    break
                
            if len(title_text) > 0:
                offset_w = classes.Fonts.edit_font.size(title_text[cursor_y][:cursor])[0]
            pyg.draw.rect(Globals.WINDOW, classes.DarkMode.text_color, (left + 20 + offset_w, top + 35 + cursor_y * 25, 2, 24))

        # Description
        offset = max(0, (len(title_text) - 1) * 25)

        desc_text = chunk_text.Chunk(task.description, content_width=width-160, char_size=classes.Fonts.list_font.size("A")[0])
        if CheckCollisions(mouse_pos, box=(left + 10, top + 100, width - 150, max(150, 150 + (len(desc_text) - 7) * 17))) or classes.Globals.edit_box == "desc":
            color = classes.DarkMode.hover_color 
        else:
            color = classes.DarkMode.task_color

        pyg.draw.rect(Globals.WINDOW, color, (left + 10, top + 100 + offset, width - 150, max(150, 150 + (len(desc_text) - 7) * 17)), border_radius=5)
        for i in range(len(desc_text)):
            Globals.WINDOW.blit(classes.Fonts.list_font.render(desc_text[i], True, classes.DarkMode.text_color), (left + 20, top + 110 + i * 17 + offset))

        if classes.Globals.edit_box == "desc" and classes.Globals.cursor_delay > 0:
            cursor = classes.Globals.cursor
            cursor_y = 0
            offset_w = 0
            for line in desc_text:
                if cursor > len(line) and len(line) != 0:
                    cursor_y += 1
                    cursor -= len(line)
                else:
                    break

            if len(desc_text) > 0:
                offset_w = classes.Fonts.list_font.size(desc_text[cursor_y][:cursor])[0]
            pyg.draw.rect(Globals.WINDOW, classes.DarkMode.text_color, (left + 20 + offset_w, top + 110 + cursor_y * 17 + max(0, (len(title_text) - 1) * 25), 2, 16))


    # Close menu
    if quitout_menu != "":
        pyg.draw.rect(Globals.WINDOW, classes.DarkMode.task_color, (Globals.WIDTH/2-160, Globals.HEIGHT/2-100, 320, 150))
        pyg.draw.rect(Globals.WINDOW, classes.DarkMode.red, (Globals.WIDTH/2-150, Globals.HEIGHT/2-20, 145, 60))
        pyg.draw.rect(Globals.WINDOW, classes.DarkMode.green, (Globals.WIDTH/2+5, Globals.HEIGHT/2-20, 145, 60))
        text_width, text_height = classes.Fonts.task_font.size("No")
        Globals.WINDOW.blit(classes.Fonts.task_font.render("No", True, classes.DarkMode.text_color), ((Globals.WIDTH-text_width)/2-74, (Globals.HEIGHT-text_height)/2+10))
        text_width, text_height = classes.Fonts.task_font.size("Yes")
        Globals.WINDOW.blit(classes.Fonts.task_font.render("Yes", True, classes.DarkMode.text_color), ((Globals.WIDTH-text_width)/2+78, (Globals.HEIGHT-text_height)/2+10))

        text_width = classes.Fonts.task_font.size("Are you sure you want to")[0]
        Globals.WINDOW.blit(classes.Fonts.task_font.render("Are you sure you want to", True, classes.DarkMode.text_color), ((Globals.WIDTH-text_width)/2, Globals.HEIGHT/2-80))
        if quitout_menu == "exit":
            text_width = classes.Fonts.task_font.size("save and exit?")[0]
            Globals.WINDOW.blit(classes.Fonts.task_font.render("save and exit?", True, classes.DarkMode.text_color), ((Globals.WIDTH-text_width)/2, Globals.HEIGHT/2-60))
        else:
            text_width = classes.Fonts.task_font.size("exit without saving?")[0]
            Globals.WINDOW.blit(classes.Fonts.task_font.render("exit without saving?", True, classes.DarkMode.text_color), ((Globals.WIDTH-text_width)/2, Globals.HEIGHT/2-60))


    # Settings stuff
    if classes.Globals.settings["fps-visible"]:
        fps = 0
        try:
            temp_frame_list = []
            for i in range(len(classes.Globals.previous_frames)-1):
                temp_frame_list += [classes.Globals.previous_frames[i+1] - classes.Globals.previous_frames[i]]
            for frame in temp_frame_list:
                fps += 1/frame
            fps += classes.Globals.current_time - classes.Globals.previous_frames[-1]
            fps = round(fps / (len(temp_frame_list) + 1))
        except:
            pass
        classes.Globals.WINDOW.blit(classes.Fonts.task_font.render(str(fps), True, classes.DarkMode.text_color), (2, 2))
    pyg.display.update()


def CheckCollisions(location, box=()):
    '''Returns true if the location collides with the given object'''
    if box != ():
        if box[0] <= location[0] <= box[0] + box[2] and box[1] <= location[1] <= box[1] + box[3]:
            return True
        
    return False