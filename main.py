import pygame

from utils import Button, TextInput

from keyboard import Keyboard

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("JSON Editor")

button = Button(
            x=250,
            y=250,
            width=150,
            height=50,
            font=pygame.font.Font(None, 24),
            screen=screen,
            text="Click Me!"
)

text_input = TextInput(
            x=125, 
            y=125, 
            width=150, 
            height=50, 
            font=pygame.font.Font(None, 24),
            max_length=50,
            screen=screen,
            placeholder="Enter text here"
)

keyboard = Keyboard(
            text_input=text_input
)


user_text = text_input.placeholder

running = True

input_box_active = False

def text_input_callback(text):
    print(text)

def button_callback():
    print("Button clicked!")

while running:
    screen.fill((25, 25, 25))
    clock.tick(60)

    keys = pygame.key.get_pressed()
    user_text = keyboard.handle_backspace(keys, user_text)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            user_text, input_box_active = keyboard.handle_mousedown(user_text, text_input, button, button_callback)

        if event.type == pygame.KEYDOWN and input_box_active:
            user_text = keyboard.handle_keydown(event, user_text, text_input, text_input_callback)
    
    button.draw()
    text_input.draw()

    pygame.display.update()
    pygame.display.flip()

pygame.quit()