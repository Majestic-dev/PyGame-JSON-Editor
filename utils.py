import pygame
import json
import string
import random
import ast
import os

from typing import Optional, Tuple, Callable


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
                 border_width: int = 2,
                 border_radius: int = 0,
                 screen_x: int = 0,
                 screen_y: int = 0,
                 callback: Callable = None,
                 sprite: Optional[pygame.image.load] = None,
                 dark_sprite: Optional[pygame.image.load] = None
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
        self.border_radius = border_radius
        self.screen = screen
        self.screen_x = screen_x
        self.screen_y = screen_y

        self.callback = callback

        self.sprite = sprite if sprite else None
        self.dark_sprite = dark_sprite if dark_sprite else None

        self.surface = pygame.Surface((self.width, self.height))

        if self.screen_x == 0 and self.screen_y == 0:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            self.rect = pygame.Rect(self.screen_x, self.screen_y, self.width, self.height)

        self.set_text(self.text)

        self.is_dragging = False

    def draw(self):
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 0))

        mask_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255), (0, 0, self.width, self.height), border_radius=self.border_radius)

        if self.sprite:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.dark_sprite:
                    temp_surface = pygame.transform.scale(self.dark_sprite, (self.width, self.height))
                else:
                    temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pygame.draw.rect(temp_surface, self.hover_colour, (0, 0, self.width, self.height), border_radius=self.border_radius)
            else:
                temp_surface = pygame.transform.scale(self.sprite, (self.width, self.height))

            button_surface.blit(temp_surface, (0, 0))
            button_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(button_surface, self.hover_colour, (0, 0, self.width, self.height), border_radius=self.border_radius)
            else:
                pygame.draw.rect(button_surface, self.bg_colour, (0, 0, self.width, self.height), border_radius=self.border_radius)

        pygame.draw.rect(button_surface, self.border_colour, (0, 0, self.width, self.height), self.border_width, self.border_radius)
        button_surface.blit(self.text_surface, self.text_rect)
        self.screen.blit(button_surface, (self.x, self.y))

    def set_text(self, text: str):
        self.text = text

        self.text_surface = self.font.render(self.text, True, self.font_colour)
        text_width = self.text_surface.get_width()

        while text_width > self.width - 10:
            self.text = self.text[:-4] + '...'
            self.text_surface = self.font.render(self.text, True, self.font_colour)
            text_width = self.text_surface.get_width()

        self.text_rect = self.text_surface.get_rect(center=(self.width/2, self.height/2))

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

    def callback(self):
        if self.callback:
            self.callback()

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

        self.path = []

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

    def add_json(self, filename: str, value):
        value = convert_str(value)
        with open(filename, 'r') as file:
            data = json.load(file)

        if self.path:
            temp = data
            for key in self.path[:-1]:
                temp = temp[key]
            temp[self.path[-1]] = value

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
        self.filename = None

        self.scroll_bar_width = 10
        self.scroll_bar_height = 0
        self.scroll_bar_colour = (150, 150, 150)

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

        self.dict: dict = {}


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

    def set_text(self, filename: str, force_reload: bool = False):
        if force_reload or not self.filename or not self.lines:
            self.filename = filename
            with open(filename, 'r') as file:
                lines = []
                for line in file:
                    lines.append(line.rstrip('\n'))
                self.lines = lines
                self.dict = json.loads(''.join(lines))
        self.total_lines = len(self.lines)
        self.text_height = self.total_lines * self.font.get_height()
        self.scroll_bar_height = max(self.height * self.height / max(self.text_height, self.height), 20)
        self.file_size = os.path.getsize(filename)
        pygame.display.set_caption(f"JSON Editor ({filename} - {self.file_size / (1024 * 1024):.2f} MB)")

    def load_visible_text(self):
        start_line = max(int(self.scroll_offset_y / self.font.get_height()), 0)
        end_line = min(start_line + int(self.height / self.font.get_height()) + 1, self.total_lines)

        self.text = self.lines[start_line:end_line]
        self.text_surfaces = [self.font.render(line, True, self.font_colour) for line in self.text]

        if self.text_width == 0:
            self.text_width = max(self.font.size(line)[0] for line in self.lines) + 10

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

class DisplayJSONKeyButtonsDynamically:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 font: pygame.font.Font,
                 screen: pygame.display.set_mode,
                 button_width: int,
                 button_height: int,
                 button_spacing: int,
                 input_box: TextInput,
                 display_json_box: DisplayJSONBox
                 ):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.screen = screen
        self.button_width = button_width
        self.button_height = button_height
        self.input_box = input_box
        self.display_json_box = display_json_box

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttons = []
        self.keys = []
        self.total_keys = 0

        self.scroll_bar_width = 10
        self.scroll_bar_height = 0
        self.scroll_bar_colour = (100, 100, 100)
        self.vertical_scroll_bar_dragging = False
        self.vertical_scroll_bar_enabled = True
        self.scroll_bar_y = 0
        self.scroll_bar_drag_start_y = 0
        self.scroll_offset_y = 0
        self.scroll_speed = 10

        self.button_spacing = button_spacing

        self.total_button_height = 0
        self.current_dict = display_json_box.dict
        self.json_data = self.current_dict = display_json_box.dict
        self.keys = list(self.current_dict.keys())
        self.current_key = None

        self.at_root = True

        self.navigation_stack = []

        self.back_button_sprite = pygame.image.load("assets/back_button.jpg")
        self.back_button_dark_sprite = self.back_button_sprite.copy()
        self.back_button_dark_sprite.fill((128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)

        self.back_button = Button(
                                x=660,
                                y=360,
                                width=100,
                                height=30,
                                font=self.font,
                                screen=self.screen,
                                text="Back",
                                bg_colour=(178,34,34),
                                hover_colour=(139,0,0),
                                border_radius=5,
                                sprite=self.back_button_sprite,
                                dark_sprite=self.back_button_dark_sprite,
                                )
        
        self.sprite = pygame.image.load("assets/normal_button.jpg")
        self.dark_sprite = self.sprite.copy()
        self.dark_sprite.fill((128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)


    def set_keys(self, force_reload: bool = False):
        if force_reload:
            self.keys = list(self.current_dict.keys())
        self.total_keys = len(self.keys)
        self.total_button_height = ((self.total_keys + 4) // 5) * self.button_height
        total_lines = (self.total_keys + 4) // 5
        visible_lines = self.height // self.button_height
        if total_lines == 0:
            self.scroll_bar_height = 0
        else:
            self.scroll_bar_height = max((visible_lines / total_lines) * self.height, 20)
        self.load_visible_buttons()

    def update_keys_and_buttons(self, key):
        if isinstance(self.current_dict[key], dict):
            self.current_key = key
            self.navigation_stack.append((self.current_dict, self.keys, self.current_key))
            self.input_box.path.append(str(key))
            self.current_dict = self.current_dict[key]
            self.set_keys(force_reload=True)
            self.at_root = False
        else:
            self.at_root = False
            self.current_key = key
            self.input_box.path.append(str(key))
            self.navigation_stack.append((self.current_dict, self.keys, self.current_key))
            self.current_dict = {}
            self.keys = []
            self.buttons = []
        self.total_keys = len(self.keys)
        self.total_button_height = ((self.total_keys + 4) // 5) * self.button_height

        if self.keys:
            self.load_visible_buttons()
            self.draw()
        return bool(self.keys)
    
    def print_tree(self, json_obj, indent=0):
        if isinstance(json_obj, dict):
            for key in json_obj:
                print('  ' * indent + str(key))
                self.print_tree(json_obj[key], indent + 1)
        elif isinstance(json_obj, list):
            for i in range(len(json_obj)):
                print('  ' * indent + str(i))
                self.print_tree(json_obj[i], indent + 1)
        else:
            print('  ' * indent + str(json_obj))
    
    def go_back(self):
        if self.navigation_stack:
            self.current_dict, self.keys, self.current_key = self.navigation_stack.pop()
            self.input_box.path.pop()
            self.set_keys(force_reload=True)
            self.at_root = len(self.navigation_stack) == 0

    def delete_key(self, filename: str):
        if self.navigation_stack:
            parent_dict, _, current_key = self.navigation_stack[-1]
            if current_key in parent_dict:
                del parent_dict[current_key]
                with open(filename, 'w') as file:
                    json.dump(self.json_data, file, indent=4)
                self.display_json_box.set_text(filename, force_reload=True)
                self.set_keys(force_reload=True) 
                self.go_back()

    def load_visible_buttons(self):
        if not self.keys:
            self.visible_keys = []
            self.buttons = []

            start_row = max(int(self.scroll_offset_y / self.button_height), 0)

            last_button_index = 0
            last_button_x = (last_button_index % 5) * (self.button_width + self.button_spacing)
            last_button_y = ((last_button_index // 5) - start_row) * (self.button_height + self.button_spacing)
            last_button_screen_x = (last_button_index % 5) * self.button_width + self.x
            last_button_screen_y = ((last_button_index // 5) - start_row) * self.button_height + self.y

            self.last_button = Button(
                x=last_button_x,
                y=last_button_y,
                width=self.button_width,
                height=self.button_height,
                font=self.font,
                screen=self.surface,
                text='-',
                bg_colour=(178, 34, 34),
                hover_colour=(139, 0, 0),
                border_width=2,
                border_radius=5,
                screen_x=last_button_screen_x,
                screen_y=last_button_screen_y,
                callback=lambda: self.delete_key("test.json"),
                sprite=self.back_button_sprite,
                dark_sprite=self.back_button_dark_sprite
            )

            self.buttons.append(self.last_button)

            return
        
        elif self.keys:
            start_row = max(int(self.scroll_offset_y / self.button_height), 0)
            end_row = min(start_row + int(self.height / self.button_height) + 2, int(self.total_keys / 5) + 1)
            start_key = start_row * 5
            end_key = min(end_row * 5, self.total_keys)
            self.visible_keys = self.keys[start_key:end_key]
            
            self.buttons = [Button(
                x=(i % 5) * (self.button_width + self.button_spacing),
                y=((i // 5) - start_row) * (self.button_height + self.button_spacing),
                width=self.button_width,
                height=self.button_height,
                font=self.font,
                screen=self.surface,
                text=key,
                bg_colour=(169, 169, 169),
                border_width=2,
                border_radius=5,
                screen_x=(i % 5) * self.button_width + self.x,
                screen_y=((i // 5) - start_row) * self.button_height + self.y,
                callback=lambda key=key: self.update_keys_and_buttons(key),
                sprite=self.sprite,
                dark_sprite=self.dark_sprite
            ) for i, key in enumerate(self.visible_keys, start=start_key)]

            last_button_index = len(self.visible_keys)
            last_button_x = (last_button_index % 5) * (self.button_width + self.button_spacing)
            last_button_y = ((last_button_index // 5) - start_row) * (self.button_height + self.button_spacing)
            last_button_screen_x = (last_button_index % 5) * self.button_width + self.x
            last_button_screen_y = ((last_button_index // 5) - start_row) * self.button_height + self.y
            
            self.last_button = Button(
                x=last_button_x,
                y=last_button_y,
                width=self.button_width,
                height=self.button_height,
                font=self.font,
                screen=self.surface,
                text='-',
                bg_colour=(178, 34, 34),
                hover_colour=(139, 0, 0),
                border_width=2,
                border_radius=5,
                screen_x=last_button_screen_x,
                screen_y=last_button_screen_y,
                callback=lambda: self.delete_key("test.json"),
                sprite=self.back_button_sprite,
                dark_sprite=self.back_button_dark_sprite
            )

            self.buttons.append(self.last_button)

    def draw(self):
        self.surface.fill((25, 25, 25))

        total_lines = (len(self.keys) + 4) // 5
        visible_lines = self.height // self.button_height

        self.load_visible_buttons()

        if not self.at_root:
            self.back_button.draw()

        if not self.keys:
            self.buttons = []
            self.load_visible_buttons()

        for button in self.buttons:
            if self.at_root and button == self.last_button:
                continue
            button.draw()

        if total_lines > visible_lines:
            self.scroll_bar_height = max((visible_lines / total_lines) * self.height, 20)
            pygame.draw.rect(self.surface, self.scroll_bar_colour, (self.width - self.scroll_bar_width, self.scroll_bar_y, self.scroll_bar_width, self.scroll_bar_height))
            self.vertical_scroll_bar_enabled = True
        else:
            self.vertical_scroll_bar_enabled = False
            self.scroll_offset_y = 0
            self.scroll_bar_y = 0

        self.screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= self.x
                mouse_y -= self.y
                if self.width - self.scroll_bar_width <= mouse_x <= self.width and 0 <= mouse_y <= self.height:
                    self.vertical_scroll_bar_dragging = True
                    self.scroll_bar_drag_start_y = mouse_y - self.scroll_bar_y
                if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.go_back()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_x + self.x, mouse_y + self.y):
                        button.callback()
                        break   
            elif event.button == 4:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.vertical_scroll_bar_enabled:
                        self.scroll_up()
            elif event.button == 5:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.vertical_scroll_bar_enabled:
                        self.scroll_down()
            if self.keys:
                self.draw()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.vertical_scroll_bar_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.vertical_scroll_bar_dragging and self.vertical_scroll_bar_enabled:
                _, mouse_y = pygame.mouse.get_pos()
                mouse_y -= self.y
                self.scroll_bar_y = min(max(mouse_y - self.scroll_bar_drag_start_y, 0), self.height - self.scroll_bar_height)
                self.scroll_offset_y = (self.scroll_bar_y / (self.height - self.scroll_bar_height)) * max(self.total_button_height - self.height, 0)
                self.scroll_offset_y = min(self.scroll_offset_y, max(self.total_button_height - self.height, 0))
            if self.keys:
                self.draw()

    def scroll_down(self):
        max_scroll = max(self.total_button_height - self.height + self.button_height, 0)
        self.scroll_bar_y = min(self.scroll_bar_y + self.scroll_speed, self.height - self.scroll_bar_height)
        self.scroll_offset_y = (self.scroll_bar_y / (self.height - self.scroll_bar_height)) * max_scroll
        self.scroll_offset_y = min(self.scroll_offset_y, max_scroll)

    def scroll_up(self):
        max_scroll = max(self.total_button_height - self.height + self.button_height, 0)
        self.scroll_bar_y = max(self.scroll_bar_y - self.scroll_speed, 0)
        self.scroll_offset_y = (self.scroll_bar_y / (self.height - self.scroll_bar_height)) * max_scroll
        self.scroll_offset_y = max(self.scroll_offset_y, 0)


class TreeMinimap:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 screen: pygame.display.set_mode,
                 input_box: TextInput,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.input_box = input_box

        self.screen = screen

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.items = []

        self.sprite = pygame.image.load("assets/tree_box.jpg")
        self.dark_sprite = self.sprite.copy()
        self.dark_sprite.fill((128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)

        self.scroll_bar_width = 10
        self.scroll_bar_height = 0
        self.scroll_bar_colour = (150, 150, 150)

        self.vertical_scroll_bar_dragging = False
        self.vertical_scroll_bar_enabled = False

        self.horizontal_scroll_bar_dragging = False
        self.horizontal_scroll_bar_enabled = False

        self.text_width = 0

        self.text_surfaces = []


    def unique_id(self):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(4))

    def set_text(self):
        x = 0
        y = 0
        path = []
        for key in self.input_box.path:
            path.append(key)
            path_str = '.'.join(path)
            if path_str not in self.items:
                self.items.append(path_str)
            self.surface.blit(self.input_box.font.render(key, True, (192,192,192)), (x + 10, y + 5))
            y += 20
            x += 5

        lines = []
        for item in self.items:
            lines.append(item)

    def draw(self):
        for i, text_surface in enumerate(self.text_surfaces):
            y = i * self.font.get_height() + 10
            self.surface.blit(text_surface, (10 - self.scroll_offset_x, y))

        self.screen.blit(self.surface, (self.x, self.y))

        if self.sprite:
            if self.dark_sprite:
                temp_surface = pygame.transform.scale(self.dark_sprite, (self.width, self.height))
            else:
                temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(temp_surface, (128, 128, 128), (0, 0, self.width, self.height), border_radius=5)
        else:
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, (128, 128, 128), (0, 0, self.width, self.height), border_radius=5)

        self.surface.blit(temp_surface, (0, 0))
        self.set_text()

    def load_visible_text(self):
        start_line = max(int(self.scroll_offset_y / self.font.get_height()), 0)
        end_line = min(start_line + int(self.height / self.font.get_height()) + 1, self.total_lines)

        self.text = self.lines[start_line:end_line]
        self.text_surfaces = [self.font.render(line, True, self.font_colour) for line in self.text]

        if self.text_width == 0:
            self.text_width = max(self.font.size(line)[0] for line in self.lines) + 10