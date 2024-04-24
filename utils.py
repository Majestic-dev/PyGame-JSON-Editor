import pygame

from typing import Optional, Tuple


class Button:
    def __init__(self, 
                 x: int, 
                 y: int, 
                 width: int, 
                 height: int, 
                 font: pygame.font.Font,
                 screen: pygame.display.set_mode, 
                 text: Optional[str] = None,
                 font_colour: Tuple[int, int, int] = (0, 0, 0), 
                 bg_colour: Tuple[int, int, int] = (255, 255, 255),
                 hover_colour: Tuple[int, int, int] = (128, 128, 128),
                 border_colour: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2
                 ):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_colour = font_colour
        self.bg_colour = bg_colour
        self.hover_colour = hover_colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.screen = screen

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

        self.is_dragging = False

    def draw(self):
        self.surface.fill(self.bg_colour)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surface.fill(self.hover_colour)
        else:
            self.surface.fill(self.bg_colour)
        
        pygame.draw.rect(self.surface, self.border_colour, (0, 0, self.width, self.height), self.border_width)
        self.surface.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.surface, (self.x, self.y))

    def move_on_hold(self):
        self.surface.fill(self.hover_colour)

        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.is_dragging = True

        if self.is_dragging:
            self.x = pygame.mouse.get_pos()[0] - self.width/2
            self.y = pygame.mouse.get_pos()[1] - self.height/2
            self.rect.topleft = (self.x, self.y)

        if not pygame.mouse.get_pressed()[0]:
            self.is_dragging = False

    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False
    
    def set_text(self, text: str):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

class TextInput:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 font: pygame.font.Font,
                 max_length: int,
                 screen: pygame.display.set_mode,
                 placeholder: Optional[str] = "",
                 font_colour: Tuple[int, int, int] = (0, 0, 0),
                 bg_colour: Tuple[int, int, int] = (255, 255, 255),
                 border_colour: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2
                 ):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.max_length = max_length
        self.placeholder = placeholder
        self.font_colour = font_colour
        self.bg_colour = bg_colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.screen = screen

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.placeholder, True, self.font_colour)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

        self.activated = False

    def draw(self):
        self.surface.fill(self.bg_colour)
        pygame.draw.rect(self.surface, self.border_colour, (0, 0, self.width, self.height), self.border_width)

        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_visible(True)
        elif self.rect.collidepoint(pygame.mouse.get_pos()) and self.activated:
            pygame.mouse.set_visible(False)

        self.surface.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.surface, (self.x, self.y))

    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.activated = True
            return True
        return False
    
    def add_text(self, text: str):
        if len(text) < self.max_length:
            current_font_size = self.font.size(' ')[1]

            self.text_surface = self.font.render(text, True, self.font_colour)
            self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

            while self.text_surface.get_width() > self.surface.get_width():
                current_font_size -= 1
                self.font = pygame.font.Font(None, current_font_size)
                self.text_surface = self.font.render(text, True, self.font_colour)
                self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

            while self.text_surface.get_width() < self.surface.get_width() * 0.9 and current_font_size < self.height:
                current_font_size += 1
                self.font = pygame.font.Font(None, current_font_size)
                self.text_surface = self.font.render(text, True, self.font_colour)
                self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

    def get_text(self):
        return self.text_surface