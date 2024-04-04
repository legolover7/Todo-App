import pygame as pyg
import modules.classes as classes
import modules.task_c as task_c
import modules.chunk_text as chunk_text

# Copy classes
Globals = classes.Globals
DarkMode = classes.DarkMode
Fonts = classes.Fonts
checkMCollision = classes.checkMCollision
Task = task_c.Task

# Class that makes up the List object and contains Tasks
class List:
    def __init__(self, title):
        self.tasks = []
        self.position = [0, 0]
        self.width, self.height = 210, 90
        self.title = title
        self.scroll_offset = 0
        self.max_scroll = 0
        self.index = 0

        self.max_line_width = (self.width - 2) // Fonts.list_font.size("A")[0]
        self.title_height = len(chunk_text.Chunk(title, max_length=self.max_line_width)) * 17 + 15

        for task in self.tasks:
            self.height = min(Globals.HEIGHT - 200, self.height + task.height + 5)

    def draw(self):
        '''Draws the list at its given location'''
        self.height = 90
        sum_sizes = 0
        for task in self.tasks:
            sum_sizes += task.height + 5
        self.height = min(Globals.HEIGHT - 200, self.height + sum_sizes)
        self.max_scroll = sum_sizes - (self.height-65)

        # Draw body
        pyg.draw.rect(Globals.WINDOW, DarkMode.list_color, (self.position[0], self.position[1], self.width, self.height), border_radius=5)

        
        # Draw tasks
        task_h_offset = self.position[1] + self.title_height
        for task in self.tasks:
            task.position[0] = self.position[0] + 5
            task.position[1] = task_h_offset - self.scroll_offset
            task.draw()
            task_h_offset += task.height + 5

        # Draw title
        text = chunk_text.Chunk(self.title, max_length=self.max_line_width)
        pyg.draw.rect(Globals.WINDOW, DarkMode.list_color, (self.position[0], self.position[1], self.width, 15 + len(text) * 17), border_radius=5)
        for i in range(len(text)):
            Globals.WINDOW.blit(Fonts.list_font.render(text[i], True, DarkMode.text_color), (self.position[0] + 8, self.position[1] + 8 + i * 17))

        # Draw add new task button
        pyg.draw.rect(Globals.WINDOW, DarkMode.list_color, (self.position[0] + 5, self.position[1] + self.height - 35, self.width - 10, 25))
        color = DarkMode.hover_color if checkMCollision(box=(self.position[0] + 5, self.position[1] + self.height - 30, self.width - 10, 25)) else DarkMode.task_color
        pyg.draw.rect(Globals.WINDOW, color, (self.position[0] + 5, self.position[1] + self.height - 30, self.width - 10, 25), border_radius=5)
        Globals.WINDOW.blit(Fonts.list_font.render("Add new task", True, DarkMode.text_color), (self.position[0] + 10, self.position[1] + self.height - 25))
        Globals.WINDOW.blit(Fonts.board_title_font.render("+", True, DarkMode.text_color), (self.position[0] + self.width - 28, self.position[1] + self.height - 32))
        
        # Draw scrollbar
        if sum_sizes >= self.height - 65 and self.max_scroll > 0:
            ratio = sum_sizes / (sum_sizes + self.height-65)
            percentage = self.scroll_offset / self.max_scroll
            pyg.draw.rect(Globals.WINDOW, DarkMode.hover_color, (self.position[0] + self.width - 4, 130 + percentage * self.height * ratio, 2, self.height * (1 - ratio)))

        # Mask overflow tasks
        pyg.draw.rect(Globals.WINDOW, DarkMode.list_color, (self.position[0] + 5, self.position[1] + self.height - 5, self.width - 10, 5))
        pyg.draw.rect(Globals.WINDOW, DarkMode.background, (self.position[0], self.position[1] + Globals.HEIGHT-200, self.width, 200))
    

    def checkMPress(self, button):
        '''Check what item was clicked within this list'''
        # Check if a task was pressed
        for i in range(len(self.tasks)):
            press = self.tasks[i].checkMPress(button)
            if press == "clicked":
                return "task_clicked"
            elif press == "delete":
                self.tasks.pop(i)
                return "active"

        # Check if a left click was pressed on the add new task button
        if checkMCollision(box=(self.position[0] + 5, self.position[1] + self.height - 30, self.width - 10, 25)) and button == 1:
            self.addTask("Example Task " + str(len(self.tasks) + 1), "Example Description")

        # Check if a right click was pressed on the header
        elif button == 3 and checkMCollision(box=(self.position[0], self.position[1], self.width, 30)):
            return "delete"
        
        elif len(self.tasks) == 0 and checkMCollision(box=(self.position[0], self.position[1], self.width, 55)):
            return "delete"
        
        return "active"


    def addTask(self, title, desc):
        '''Adds a task with the given title and description'''
        self.tasks.append(Task(title, desc))

    def scroll(self, direction):
        '''Scrolls the content within the list'''
        sum_sizes = 0
        for task in self.tasks:
            sum_sizes += task.height + 5

        if sum_sizes - (self.height-65) < 0:
            return
        self.scroll_offset = min(max(0, self.scroll_offset + -direction * 10), self.max_scroll)