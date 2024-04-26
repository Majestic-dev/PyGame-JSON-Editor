import pygame
import json
import ast
import os

from typing import Optional, Tuple
from collections import deque


def convert_str(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            try:
                return ast.literal_eval(s)
            except (ValueError, SyntaxError):
                return s
            
def line_generator(filename: str):
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


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
    
    def add_json(self, filename: str, keys: list, value):
        value = convert_str(value)
        with open(filename, 'r') as file:
            data = json.load(file)

        temp = data
        for key in keys[:-1]:
            temp = temp[key]
        temp[keys[-1]] = value

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def get_text(self):
        return self.text_surface
    
class DisplayJSONBox:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 font: pygame.font.Font,
                 screen: pygame.display.set_mode,
                 text: Optional[str] = "",
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
        self.text = text
        self.font_colour = font_colour
        self.bg_colour = bg_colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.screen = screen

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.text, True, self.font_colour)
        self.text_rect = self.text_surface.get_rect(topleft=(10, 10))

        self.scroll_bar_width = 10
        self.scroll_bar_height = 0
        self.scroll_bar_colour = (128, 128, 128)

        self.vertical_scroll_bar_dragging = False
        self.vertical_scroll_bar_enabled = False

        self.horizontal_scroll_bar_dragging = False
        self.horizontal_scroll_bar_enabled = False
        
        self.text_width = 0
        self.text_height = 0
        
        self.scroll_bar_x = 0
        self.scroll_bar_y = 0

        self.scroll_bar_drag_start_x = 0
        self.scroll_offset_x = 0

        self.scroll_bar_drag_start_y = 0
        self.scroll_offset_y = 0

        self.scroll_speed = 10

        self.text_surfaces = []


    def draw(self):
        self.surface.fill(self.bg_colour)

        if self.text_height > self.height:
            pygame.draw.rect(self.surface, self.scroll_bar_colour, (self.width - self.scroll_bar_width, self.scroll_bar_y, self.scroll_bar_width, self.scroll_bar_height))
            self.vertical_scroll_bar_enabled = True
        else:
            self.vertical_scroll_bar_enabled = False
            self.scroll_offset_y = 0
            self.scroll_bar_y = 0

        if self.text_width > self.width:
            pygame.draw.rect(self.surface, self.scroll_bar_colour, (self.scroll_bar_x, self.height - self.scroll_bar_width, self.scroll_bar_width, self.scroll_bar_width))
            self.horizontal_scroll_bar_enabled = True
        else:
            self.horizontal_scroll_bar_enabled = False
            self.scroll_offset_x = 0
            self.scroll_bar_x = 0

        for i, text_surface in enumerate(self.text_surfaces):
            y = i * self.font.get_height() + 10
            self.surface.blit(text_surface, (10 - self.scroll_offset_x, y))

        self.screen.blit(self.surface, (self.x, self.y))

    def set_text(self, filename: str):
        self.filename = filename
        with open(filename, 'r') as file:
            self.lines = [line.rstrip('\n') for line in file]
        self.total_lines = len(self.lines)
        self.text_height = self.total_lines * self.font.get_height()
        self.scroll_bar_height = max(self.height * self.height / max(self.text_height, self.height), 20)
        self.file_size = os.path.getsize(filename)
        pygame.display.set_caption(f"JSON Editor ({filename} - {self.file_size / (1024 * 1024):.2f} MB)")
        self.load_visible_text()

    def load_visible_text(self):
        start_line = max(int(self.scroll_offset_y / self.font.get_height()), 0)
        end_line = min(start_line + int(self.height / self.font.get_height()) + 1, self.total_lines)
        self.text = self.lines[start_line:end_line]
        self.text_surfaces = [self.font.render(line, True, self.font_colour) for line in self.text]
        self.text_width = max(self.font.size(line)[0] for line in self.text)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= self.x
                mouse_y -= self.y
                if self.width - self.scroll_bar_width <= mouse_x <= self.width and 0 <= mouse_y <= self.height:
                    self.vertical_scroll_bar_dragging = True
                    self.scroll_bar_drag_start_y = mouse_y - self.scroll_bar_y
                elif 0 <= mouse_x <= self.width and self.height - self.scroll_bar_height <= mouse_y <= self.height:
                    self.horizontal_scroll_bar_dragging = True
                    self.scroll_bar_drag_start_x = mouse_x - self.scroll_bar_x
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x -= self.x
            mouse_y -= self.y
            if event.button == 4:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if (self.height - self.scroll_bar_height - self.scroll_bar_width <= mouse_y <= self.height) and self.horizontal_scroll_bar_enabled:
                        self.scroll_left()
                    else:
                        if self.vertical_scroll_bar_enabled:
                            self.scroll_up()
            elif event.button == 5:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if (self.height - self.scroll_bar_height - self.scroll_bar_width <= mouse_y <= self.height) and self.horizontal_scroll_bar_enabled:
                        self.scroll_right()
                    else:
                        if self.vertical_scroll_bar_enabled:
                            self.scroll_down()
            self.draw()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.vertical_scroll_bar_dragging = False
                self.horizontal_scroll_bar_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.vertical_scroll_bar_dragging and self.vertical_scroll_bar_enabled:
                _, mouse_y = pygame.mouse.get_pos()
                mouse_y -= self.y
                self.scroll_bar_y = min(max(mouse_y - self.scroll_bar_drag_start_y, 0), self.height - self.scroll_bar_height)
                self.scroll_offset_y = self.scroll_bar_y * (self.text_height - self.height) / (self.height - self.scroll_bar_height)
            elif self.horizontal_scroll_bar_dragging and self.horizontal_scroll_bar_enabled:
                mouse_x, _ = pygame.mouse.get_pos()
                mouse_x -= self.x
                self.scroll_bar_x = min(max(mouse_x - self.scroll_bar_drag_start_x, 0), self.width - self.scroll_bar_width)
                self.scroll_offset_x = self.scroll_bar_x * (self.text_width - self.width) / (self.width - self.scroll_bar_width)
            self.draw()

    def scroll_left(self):
        self.scroll_bar_x = max(self.scroll_bar_x - self.scroll_speed, 0)
        self.scroll_offset_x = self.scroll_bar_x * (self.text_width - self.width) / (self.width - self.scroll_bar_width)

    def scroll_right(self):
        self.scroll_bar_x = min(self.scroll_bar_x + self.scroll_speed, self.width - self.scroll_bar_width)
        self.scroll_offset_x = self.scroll_bar_x * (self.text_width - self.width) / (self.width - self.scroll_bar_width)

    def scroll_up(self):
        self.scroll_bar_y = max(self.scroll_bar_y - self.scroll_speed, 0)
        self.scroll_offset_y = self.scroll_bar_y * (self.text_height - self.height) / (self.height - self.scroll_bar_height)

    def scroll_down(self):
        self.scroll_bar_y = min(self.scroll_bar_y + self.scroll_speed, self.height - self.scroll_bar_height)
        self.scroll_offset_y = self.scroll_bar_y * (self.text_height - self.height) / (self.height - self.scroll_bar_height)