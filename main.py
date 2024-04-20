import pygame

from utils import Button, TextInput

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("JSON Editor")

button = Button(
            x=250, 
            y=250, 
            width=150, 
            height=50, 
            text="Button", 
            font=pygame.font.Font(None, 24), 
            font_color=(0, 0, 0), 
            bg_color=(255, 255, 255), 
            hover_color=(79,66,181), 
            border_color=(0, 0, 0), 
            border_width=2, 
            screen=screen)

text_input = TextInput(
            x=125, 
            y=125, 
            width=150, 
            height=50, 
            font=pygame.font.Font(None, 24), 
            font_color=(0, 0, 0), 
            bg_color=(255, 255, 255), 
            border_color=(0, 0, 0), 
            border_width=2, 
            screen=screen)

user_text = ""

running = True

backspace_held = False

input_box_active = False

while running:
    screen.fill((25, 25, 25))
    clock.tick(60)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        if backspace_start_time is None:
            backspace_start_time = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - backspace_start_time >= 750 or backspace_held:
            backspace_held = True
            if pygame.time.get_ticks() - backspace_start_time >= 50:
                user_text = user_text[:-1]
                text_input.add_text(user_text)
                backspace_start_time = pygame.time.get_ticks()
    else:
        backspace_start_time = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                backspace_held = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_input.is_clicked():
                input_box_active = True
            else:
                input_box_active = False

        if event.type == pygame.KEYDOWN and input_box_active:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
            text_input.add_text(user_text)
    
    button.draw()
    text_input.draw()

    pygame.display.update()
    pygame.display.flip()

pygame.quit()