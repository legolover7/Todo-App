import pygame as pyg
import modules.classes as classes
import modules.chunk_text as chunk_text

# Copy classes
Globals = classes.Globals
DarkMode = classes.DarkMode
Fonts = classes.Fonts
checkMCollision = classes.checkMCollision

# Class that makes up the Task object
class Task:    
    def __init__(self, title, desc):
        self.position = [0, 0]
        self.width, self.height = 200, 30
        self.title = title
        self.description = desc

        # Max_line_width is the maximum amount of characters per line based on the width of the task
        self.max_line_width = (self.width - 2) // Fonts.task_font.size("A")[0]
        self.height = max(30 + (len(chunk_text.Chunk(title, self.max_line_width)) - 1) * 15, 30)


    def draw(self):
        '''Draws the task at its given location'''
        color = DarkMode.hover_color if checkMCollision(object=self) else DarkMode.task_color
        pyg.draw.rect(Globals.WINDOW, color, (self.position[0], self.position[1], self.width, self.height), border_radius=5)

        # Display the title text
        text = chunk_text.Chunk(self.title, self.max_line_width)
        self.height = max(30 + (len(chunk_text.Chunk(self.title, self.max_line_width)) - 1) * 15, 30)
        for i in range(len(text)):
            Globals.WINDOW.blit(Fonts.task_font.render(text[i], True, DarkMode.text_color), (self.position[0] + 5, self.position[1] + 7 + i * 15))


    def checkMPress(self, button):
        if checkMCollision(object=self):
            if button == 1:
                classes.Globals.editing_task = self
                classes.Globals.active_list = -1
                return "clicked"
            elif button == 3:
                return "delete"