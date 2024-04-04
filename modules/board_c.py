import pygame as pyg
import modules.classes as classes
import modules.list_c as list_c
import modules.chunk_text as chunk_text

# Copy classes
Globals = classes.Globals
DarkMode = classes.DarkMode
Fonts = classes.Fonts
checkMCollision = classes.checkMCollision
List = list_c.List

# Class that makes up the Board object and contains Lists
class Board:
    def __init__(self, title):
        self.lists = []
        self.title = title
        self.menu_collapsed = False
        self.scroll_offset = 0
        self.max_scroll = 0

    def draw(self):
        '''Draws the board to the screen'''
        # Calculate base position
        self.position[0] = 50 if self.menu_collapsed else 230
        # Calculate the maxmimum scroll amount
        if len(self.lists) > 0:
            self.max_scroll = (len(self.lists) - 7) * (self.lists[0].width + 20) + 150

        if len(self.lists) < 7:
            self.scroll_offset = 0

        # Calculate variables for scroll bar
        self.position[0] -= self.scroll_offset
        self.width = Globals.WIDTH - self.position[0]
        self.height = Globals.HEIGHT - self.position[1]
        sum_sizes = 0
        for list in self.lists:
            sum_sizes += list.width + 20

        # Draw lists
        list_w_offset = self.position[0]
        for i in range(len(self.lists)):
            self.lists[i].index = i
            self.lists[i].position = [self.position[0] + i * (self.lists[i].width + 20), self.position[1]]
            self.lists[i].draw()
            list_w_offset += self.lists[i].width + 20

        # Draw title bar
        pyg.draw.rect(Globals.WINDOW, DarkMode.task_color, (0, -5, Globals.WIDTH, 65), border_radius=10)
        Globals.WINDOW.blit(Fonts.board_title_font.render("Todo App | Your Workspace", True, DarkMode.text_color), (20, 15))
        pyg.draw.rect(Globals.WINDOW, DarkMode.background, (self.position[0], 60, Globals.WIDTH, 40))

        # Draw menu
        if self.menu_collapsed:
            pyg.draw.rect(Globals.WINDOW, DarkMode.list_color, (0, 60, 20, Globals.HEIGHT), border_radius=10)
        else:
            pyg.draw.rect(Globals.WINDOW, DarkMode.list_color, (0, 60, 200, Globals.HEIGHT), border_radius=10)
            text = chunk_text.Chunk(self.title, max_length=20)
            for i in range(len(text)):
                Globals.WINDOW.blit(Fonts.list_font.render(text[i], True, DarkMode.text_color), (10, 75 + i * 17))

            pyg.draw.rect(Globals.WINDOW, DarkMode.hover_color, (0, 85 + (len(text)) * 17, 200, 2))
            offset_h = 100 + (len(text)) * 17
            for i in range(len(classes.Globals.board_dict)):
                title = classes.Globals.board_dict[i]["title"]
                if title != self.title:
                    text = chunk_text.Chunk(title, max_length=20)
                    if checkMCollision(box=(0, offset_h, 200, len(text) * 17)):
                        pyg.draw.rect(classes.Globals.WINDOW, classes.DarkMode.hover_color, (2, offset_h-2, 196, len(text) * 17+4), border_radius=5)
                    for line in text:
                        classes.Globals.WINDOW.blit(classes.Fonts.list_font.render(line, True, classes.DarkMode.text_color), (10, offset_h))
                        offset_h += 17
                    offset_h += 10

        # Draw scrollbar
        if len(self.lists) >= 7 and self.max_scroll > 0:
            ratio = sum_sizes / (sum_sizes + self.width)
            percentage = self.scroll_offset / self.max_scroll
            temp = 30 if self.menu_collapsed else 210
            pyg.draw.rect(Globals.WINDOW, DarkMode.hover_color, (temp + percentage * (Globals.WIDTH - temp + 20) * ratio, Globals.HEIGHT-2, (Globals.WIDTH - temp - 40) * (1 - ratio), 2))

        # Draw add new list button
        color = DarkMode.hover_color if checkMCollision(box=(list_w_offset, self.position[1], 210, 30)) else DarkMode.list_color
        pyg.draw.rect(Globals.WINDOW, color, (list_w_offset, self.position[1], 210, 30), border_radius=5)
        Globals.WINDOW.blit(Fonts.list_font.render("Add new list", True, DarkMode.text_color), (list_w_offset + 5, self.position[1] + 7))
        Globals.WINDOW.blit(Fonts.board_title_font.render("+", True, DarkMode.text_color), (list_w_offset + 185, self.position[1]))

        # Draw active list indicator
        if Globals.active_list >= 0:
            pyg.draw.rect(Globals.WINDOW, DarkMode.hover_color, (self.position[0] + Globals.active_list * (self.lists[Globals.active_list].width + 20), self.position[1] - 10, self.lists[Globals.active_list].width, 2))


    def addList(self, title):
        '''Adds a new list to the board'''
        self.lists.append(List(title))
        Globals.active_list = -1


    def checkMPress(self, button):
        '''Handler that runs when a mouse button is pressed'''
        if classes.Globals.editing_task is None:
            classes.Globals.active_list = -1
            classes.Globals.editing_task = None
            list_w_offset = self.position[0]
            for list in self.lists:
                list_w_offset += list.width + 20

            # Check if the new list button was pressed
            if checkMCollision(box=(list_w_offset, self.position[1], 210, 40)) and button == 1:
                self.addList("Example List " + str(len(self.lists) + 1))

            # Check if a list was pressed
            for i in range(len(self.lists)):
                if checkMCollision(object=self.lists[i]):
                    press = self.lists[i].checkMPress(button)
                    if press == "active":
                        self.lists[i].is_active = True
                        Globals.active_list = i
                    elif press == "delete":
                        self.lists.pop(i)
                        return
                else:
                    self.lists[i].is_active = False

            # Sidebar board hovering
            if not self.menu_collapsed and checkMCollision(box=(0, 100 + (len(chunk_text.Chunk(self.title, max_length=20))) * 17, 200, Globals.HEIGHT)):
                offset_h = 100 + (len(chunk_text.Chunk(self.title, max_length=20))) * 17
                for dict in classes.Globals.board_dict:
                    if dict["title"] != self.title:
                        text = chunk_text.Chunk(dict["title"], max_length=20)
                        if offset_h <= classes.Globals.mouse_position[1] <= offset_h + len(text) * 17:
                            return dict
                        
                        offset_h += len(text) * 17 + 10
        else:
            # Calculate the extra size of the boxes
            title_text = chunk_text.Chunk(classes.Globals.editing_task.title, content_width=530, char_size=classes.Fonts.edit_font.size("A")[0])
            desc_text = chunk_text.Chunk(classes.Globals.editing_task.description, content_width=530, char_size=classes.Fonts.list_font.size("A")[0])
            # Close the editing pane if clicked outside
            if not checkMCollision(box=(Globals.WIDTH/2 - 300, Globals.HEIGHT/2 - 400, 600, 800)):
                classes.Globals.editing_task = None
                classes.Globals.active_list = -1
                classes.Globals.edit_box = ""

            # Clicked on the title box
            elif checkMCollision(box=(classes.Globals.WIDTH/2 - 290, classes.Globals.HEIGHT/2 - 375, 540, max(45 + (len(title_text) - 1) * 25, 45))):
                classes.Globals.edit_box = "title"
                classes.Globals.cursor = len(classes.Globals.editing_task.title)
                classes.Globals.cursor_delay = 40

            # Clicked on the description box
            elif checkMCollision(box=(classes.Globals.WIDTH/2 - 290, classes.Globals.HEIGHT/2 - 300, 450, max(150, 150 + (len(desc_text) - 7) * 17))):
                classes.Globals.edit_box = "desc"
                classes.Globals.cursor = len(classes.Globals.editing_task.description)
                classes.Globals.cursor_delay = 40
                
            # Clicked elsewhere
            else:
                classes.Globals.edit_box = ""
                

    def checkMScroll(self, direction):
        '''Handler that runs when the mouse wheel is scrolled'''
        if classes.Globals.editing_task is None:
            for list in self.lists:
                if checkMCollision(object=list):
                    list.scroll(direction)
                    return
                
            if checkMCollision(box=(self.position[0] + self.scroll_offset, self.position[1], classes.Globals.WIDTH, classes.Globals.HEIGHT)):
                if len(self.lists) >= 7:
                    self.scroll_offset = min(max(0, self.scroll_offset - 20 * direction), self.max_scroll)