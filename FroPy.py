import pygame
from pygame import font
from time import sleep

def scale_text(size, text, color, max_size=128, font_name='Arial'):
    """Returns a fitting text for given size of surface"""
    surface_width, surface_height = size
    lower, upper = 0, max_size
    while True:
        font = pygame.font.SysFont(font_name, max_size)
        font_width = font.size(text)
        font_height = font.size(text)

        if upper - lower <= 1:
            return font.render(text, True, color)
        elif max_size < 1:
            print("ERROR: Text scaled impropertly, try reducing characters", file=sys.stderr)
            raise ValueError
        elif font_width > surface_width or font_height > surface_height:
            upper = max_size
            max_size = (lower + upper) // 2
        elif font_width < surface_width or font_height < surface_height:
            lower = max_size
            max_size = (lower + upper) // 2
        else:
            return font.render(text, True, color)

class Button:
    
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, edge=0, font='Arial', text_color=(0,0,0)):
        """Function to render our button and add a fitting text to it if text is given by the user"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), edge)
        
        if self.text != '':
            text = scale_text((self.width, self.height), self.text, text_color)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def hovered(self, mouse_x, mouse_y):
        if mouse_x < self.x + self.width and mouse_x > self.x:
            if mouse_y < self.y + self.height and mouse_y > self.y:
                return True
        return False
    
    def clicked(self, mouse_x, mouse_y):
        if mouse_x < self.x + self.width and mouse_x > self.x:
            if mouse_y < self.y + self.height and mouse_y > self.y:
                if pygame.mouse.get_pressed()[0] == True:
                    sleep(0.10)
                    return True
        return False

class Checkbox:

    def __init__(self, a_color, b_color, x, y, size, text_pos, text='', state=False):
        self.a_color = a_color # color for when the checkbox is active
        self.b_color = b_color # color for when the checkbox is not active
        self.x = x
        self.y = y
        self.size = size
        self.text_pos = text_pos
        self.text = text
        self.state = state

    def draw(self, screen, mouse_x, mouse_y, style=1, font='Arial', text_color=(0,0,0)):
        """Draw the instance of our checkbox with specified arguments. 
           style = 1 will create a slide style checkbox with no animation
           style = 2 will create a check marker style checkbox
           text_pos = 1 will render text on the left side
           text_pos = 2 will render text on the right side"""
        if style == 1:
            pygame.draw.rect(screen, self.a_color, (self.x, self.y, self.size / 2, self.size / 2))
            pygame.draw.rect(screen, self.b_color, ((self.x + self.size / 2), self.y, self.size / 2, self.size / 2))

            list_size = str(self.size)
            # draw outline
            if list_size[1] != 5 or list_size[1] != 0:
                pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y - 2], [self.x + self.size - 1, self.y - 2], 2)
                pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y - 2], [self.x - 2, self.y + self.size / 2], 2)
                pygame.draw.line(screen, (25, 25, 25), [self.x + self.size - 2, self.y], [self.x + self.size - 2, self.y + self.size / 2 + 1], 2)
                pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y + self.size / 2], [self.x + self.size - 1, self.y + self.size / 2], 2)
            else:
                pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y - 2], [self.x + self.size + 1, self.y - 2], 2)
                pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y - 2], [self.x - 2, self.y + self.size / 2], 2)
                pygame.draw.line(screen, (25, 25, 25), [self.x + self.size, self.y], [self.x + self.size, self.y + self.size / 2 + 1], 2)
                pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y + self.size / 2], [self.x + self.size, self.y + self.size / 2], 2)

            if self.state == True:
                pygame.draw.rect(screen, (255, 255, 255), ((self.x + self.size / 2 - 2), self.y, self.size / 2, self.size / 2), 0)
            else:
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.size / 2, self.size / 2), 0)
        elif style == 2:
            pygame.draw.rect(screen, self.a_color, (self.x, self.y, self.size / 2, self.size / 2))

            # draw outline
            pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y - 2], [self.x + self.size / 2 + 1, self.y - 2], 2)
            pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y - 2], [self.x - 2, self.y + self.size / 2], 2)
            pygame.draw.line(screen, (25, 25, 25), [self.x + self.size / 2, self.y], [self.x + self.size / 2, self.y + self.size / 2 + 1], 2)
            pygame.draw.line(screen, (25, 25, 25), [self.x - 2, self.y + self.size / 2], [self.x + self.size / 2, self.y + self.size / 2], 2)

            if self.state == True:
                pygame.draw.line(screen, self.b_color, [self.x + (self.size / 2) * 0.2, self.y + (self.size / 2) * 0.5],
                                                       [self.x + (self.size / 2) * 0.5, self.y + (self.size / 2) * 0.95],
                                                        7
                                                    )
                pygame.draw.line(screen, self.b_color, [self.x + (self.size / 2) * 0.5, self.y + (self.size / 2) * 0.95],
                                                       [self.x + (self.size / 2) * 0.8, self.y + (self.size / 2) * 0.1],
                                                        7
                                                    )
                                                    

        if self.text != '':
            text = scale_text((self.size * 1.3, self.size * 1.3), self.text, text_color)
            #text = font.render(self.text, 1, text_color)
            if self.text_pos == 1:
                screen.blit(text, (self.x - (text.get_width() + 10), self.y + ((self.size / 2) / 2 - text.get_height() / 2)))
            elif self.text_pos == 2:
                if style == 1:
                    screen.blit(text, (self.x + (self.size + 10), self.y + (text.get_height() / 2)))
                elif style == 2:
                    screen.blit(text, (self.x + (self.size / 2) + 10, self.y + (text.get_height() / 2)))
            else:
                raise ValueError    
    
        if mouse_x < self.x + self.size and mouse_x > self.x:
            if mouse_y < self.y + (self.size / 2) and mouse_y > self.y:
                if pygame.mouse.get_pressed()[0] == True:
                    sleep(0.10)
                    self.state = not self.state

    def get_state(self):
        return self.state

class GroupBox:

    def __init__(self, x, y, width, height, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, mouse_x, mouse_y, outl_color=(0,0,0), bg_color=(25,25,25), text_color=(255,255,255), outl_thickness=5):
        """Draw a box that contains a title and can be moved inside the program, very neat if you want to categorize within your program"""

        # draw the main box
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height))

        # draw box
        # hot sexy maffs that I have no clue about but it seems to work just fine :O
        pygame.draw.line(screen, outl_color, [self.x, self.y], [(self.x + self.width) + (outl_thickness / 2), self.y], outl_thickness)
        pygame.draw.line(screen, outl_color, [self.x, self.y + 1 - (outl_thickness / 2)], [self.x, (self.y + self.height) + (outl_thickness / 2)], outl_thickness)
        pygame.draw.line(screen, outl_color, [self.x, (self.y + self.height)], [(self.x + self.width) + (outl_thickness / 2), (self.y + self.height)], outl_thickness)
        pygame.draw.line(screen, outl_color, [(self.x + self.width), self.y], [(self.x + self.width), (self.y + self.height) + (outl_thickness / 2)], outl_thickness)

        if self.text != '':
            text = scale_text((self.width, (self.height * 0.15)), self.text, text_color)
            #text = font.render(self.text, 1, text_color)
            if self.text != "":
                screen.blit(text, round(self.x + (self.width // 2 - text.get_width() // 2) , self.y + (self.height * 0.02)))
                # draw title line
                pygame.draw.line(screen, outl_color, [self.x, self.y + text.get_height() + (self.height * 0.05)],
                                                     [(self.x + self.width), self.y + text.get_height() + (self.height * 0.05)], outl_thickness
                                                    )
        
        if mouse_x < self.x + self.width and mouse_x > self.x:
            if mouse_y < (self.y + text.get_height() + (self.height * 0.05)) and mouse_y > self.y:
                if pygame.mouse.get_pressed()[0] == True and pygame.key.get_pressed()[pygame.K_RSHIFT] == True or pygame.mouse.get_pressed()[0] == True and pygame.key.get_pressed()[pygame.K_LSHIFT] == True:
                    self.x = mouse_x - (self.width / 2)
                    self.y = mouse_y - (self.height * 0.1)

class InputBox:

    def __init__(self, x, y, width, height, title="", placeholder="", color=(25,25,25), text_color=(255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.title = title
        self.placeholder = placeholder
        self.capture_text = False
        self.text = []
        self.text_width = 0
    
    def draw(self, screen, mouse_x, mouse_y, edge, font="Arial", placeholder_color=(75,75,75)):

        if mouse_x < self.x + self.width and mouse_x > self.x:
            if mouse_y < self.y + self.height and mouse_y > self.y:
                if pygame.mouse.get_pressed()[0] == True:
                    sleep(0.10)
                    self.capture_text = not self.capture_text
            else:
                if pygame.mouse.get_pressed()[0] == True:
                    self.capture_text = False
        else:
            if pygame.mouse.get_pressed()[0] == True:
                    self.capture_text = False
        
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), edge)

        if self.capture_text == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.text = list(self.text)
                    if event.key == pygame.K_BACKSPACE and len(self.text) != 0:
                        self.text.pop()
                    elif event.key == pygame.K_ESCAPE:
                        self.capture_text = False
                    elif event.key != pygame.K_RETURN and self.text_width < self.width and event.key != pygame.K_BACKSPACE:
                        self.text.append(event.unicode)
            if len(list(self.text)) > 0:
                scaled_text = scale_text((self.width, self.height), ''.join(self.text), self.text_color)
                self.text_width = scaled_text.get_width()
                screen.blit(scaled_text, (self.x + (self.width / 2 - scaled_text.get_width() / 2), self.y + (self.height / 2 - scaled_text.get_height() / 2)))
        else:
            if self.capture_text == False:
                scaled_text = scale_text((self.width, self.height), self.placeholder, placeholder_color)
                self.text_width = scaled_text.get_width()
                screen.blit(scaled_text, (self.x + (self.width / 2 - scaled_text.get_width() / 2), self.y + (self.height / 2 - scaled_text.get_height() / 2)))
        
        scaled_title = scale_text((self.width, self.height), self.title, self.text_color)
        screen.blit(scaled_title, (self.x - (scaled_title.get_width() + 10), self.y + (self.height / 2 - scaled_title.get_height() / 2)))

    def get_text(self):
        if len(self.text) > 0:
            return ''.join(self.text)
        else:
            return "Failed to fetch text!"