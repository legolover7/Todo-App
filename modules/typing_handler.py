import pygame as pyg

import modules.classes as classes
import modules.chunk_text as chunk_text

# Keyboard input for text boxes
def handler(content, key, mods, cursor):
    '''
    Keyboard handler, edits the given content based on the keys pressed
    Parameters: The content to be edited, the event.key from pygame, the current keyboard mods, and the current cursor location
    Returns: The edited content and the adjusted cursor
    '''
    shift, caps, ctrl = mods

    # if type == "setting_box":
    #     if 48 <= key <= 57:
    #         content = str(content) + "0123456789"[key-48]
    #     elif key == pyg.K_BACKSPACE:
    #         if ctrl:
    #             content = ""
    #         else:
    #             content = str(content)[:-1]
    #     return (cursor, content)

    char = ""
    if 97 <= key <= 122:
        char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[key-97] if caps or shift else "abcdefghijklmnopqrstuvwxyz"[key-97]
        cursor += 1
    if 44 <= key <= 57:
        char = "<->?)!@#$%^&*("[key-44] if shift else ",_./0123456789"[key-44]
        cursor += 1

    if key == 39:
        char = "\"" if shift else "'"
        cursor += 1
    if key == 96:
        char = "~" if shift else "`"
        cursor += 1
    if key == 61:
        char = "+" if shift else "="
        cursor += 1
    if key == 59:
        char = ":" if shift else ";"
        cursor += 1
    if key == 91:
        char = "{" if shift else "["
        cursor += 1
    if key == 93:
        char = "}" if shift else "]"
        cursor += 1
    if key == pyg.K_SPACE:
        char = " " 
        cursor += 1
        
    content = content[:cursor-1] + char + content[cursor-1:]

    # Ctrl/Backspace
    if key == pyg.K_BACKSPACE and len(content) > 0 and cursor != 0:
        if not ctrl:
            content = content[:cursor-1] + content[cursor:]
            cursor = max(cursor-1, 0)
        else:
            content += " " 
            for i in range(cursor, 0, -1):
                i -= 1
                if content[i] == " ":
                    break
            content = content[:i] + content[cursor:]
            cursor = i
            content = content[:-1]

    # Ctrl/Delete
    if key == pyg.K_DELETE and len(content) > 0 and cursor != len(content):
        if not ctrl:
            content = content[:cursor] + content[cursor+1:]
        else:
            for i in range(cursor, len(content)):
                if content[i] == " ":
                    break
            content = content[:cursor] + content[i+1:]

    # Left/right arrows
    if key == pyg.K_LEFT:
        if ctrl:
            j = cursor
            for i in range(cursor, 0, -1):
                    j -= 1
                    if content[j] == " ":
                        break
            cursor = j
        else:
            cursor = max(0, cursor - 1)
    elif key == pyg.K_RIGHT:
        if ctrl:
            j = cursor
            for j in range(cursor, len(content)):
                    if content[j] == " " and j != cursor:
                        break
            cursor = j
        else:
            cursor = min(cursor + 1, len(content))

    # Up/down arrows
    elif (key == pyg.K_UP or key == pyg.K_DOWN) and len(content) > 0:
        if classes.Globals.edit_box == "title":
            text = chunk_text.Chunk(classes.Globals.editing_task.title, content_width=530, char_size=classes.Fonts.edit_font.size("A")[0])
        elif classes.Globals.edit_box == "desc":
            text = chunk_text.Chunk(classes.Globals.editing_task.description, content_width=440, char_size=classes.Fonts.list_font.size("A")[0])

        if cursor <= len(text[0]) and key == pyg.K_UP:
            cursor = 0
        elif cursor >= len(content) - len(text[-1]) and key == pyg.K_DOWN:
            cursor = len(content)
        else:
            temp_cursor = cursor
            cursor_y = 0
            for line in text:
                if temp_cursor > len(line):
                    cursor_y += 1
                    temp_cursor -= len(line)
                else:
                    break

            if key == pyg.K_UP:
                cursor = max(0, cursor - len(text[cursor_y-1]))
            else:
                cursor = min(len(content), cursor + len(text[cursor_y]))


    return content, cursor
