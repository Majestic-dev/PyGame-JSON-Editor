import pygame

from utils import TextInput, DisplayJSONBox, DisplayJSONKeyButtonsDynamically

from keyboard import Keyboard

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("JSON Editor")
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

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

text_box = DisplayJSONBox(
            x=780,
            y=0,
            width=500,
            height=screen.get_height(),
            font=pygame.font.Font(None, 24),
            screen=screen,
            bg_colour=(105, 105, 105)
)
text_box.set_text("test.json")


display_keys = DisplayJSONKeyButtonsDynamically(
            x=15,
            y=400,
            width=750,
            height=300,
            font=pygame.font.Font(None, 24),
            screen=screen,
            button_width=725//5,
            button_height=50,
            button_spacing=5,
            input_box=text_input,
            display_json_box=text_box,
)

keyboard = Keyboard(
            text_input=text_input,
            display_keys=display_keys
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
    clock.tick(100)

    keys = pygame.key.get_pressed()
    user_text = keyboard.handle_backspace(keys, user_text)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            user_text, input_box_active = keyboard.handle_mousedown(user_text, text_input)

        if event.type == pygame.KEYDOWN and input_box_active:
            user_text = keyboard.handle_keydown(event, user_text, text_input, text_input_callback, text_box)
        
        text_box.handle_event(event)
        display_keys.handle_event(event)

    display_keys.set_keys()

    text_box.load_visible_text()
    text_input.draw()
    text_box.draw()
    display_keys.draw()

    pygame.display.update()
    pygame.display.flip()

pygame.quit()