import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, font_color, bg_color, hover_color, border_color, border_width, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_color = font_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.screen = screen

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surface.fill(self.hover_color)
        else:
            self.surface.fill(self.bg_color)
            pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), self.border_width)

        self.surface.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.surface, (self.x, self.y))

    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False
    
    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

class TextInput:
    def __init__(self, x, y, width, height, font, font_color, bg_color, border_color, border_width, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.font_color = font_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.screen = screen

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render("", True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

    def draw(self):
        self.surface.fill(self.bg_color)
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), self.border_width)

        self.surface.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.surface, (self.x, self.y))

    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def add_text(self, text):
        current_font_size = self.font.size(' ')[1]

        self.text_surface = self.font.render(text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

        while self.text_surface.get_width() > self.surface.get_width() and current_font_size > 10:
            current_font_size -= 1
            self.font = pygame.font.Font(None, current_font_size)
            self.text_surface = self.font.render(text, True, self.font_color)
            self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
    
    def remove_text(self):
        self.text_surface = self.font.render("", True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))

    def get_text(self):
        return self.text_surface.get_text()