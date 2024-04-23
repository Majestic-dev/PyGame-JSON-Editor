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

user_text = text_input.placeholder

running = True

backspace_held = False
start_length = 0
letters_deleted = 0

input_box_active = False

def text_input_callback(text):
    print(text)

def button_callback():
    print("Button clicked!")

while running:
    screen.fill((25, 25, 25))
    clock.tick(60)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        if backspace_start_time is None:
            backspace_start_time = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - backspace_start_time >= 600 or backspace_held:
            backspace_held = True
            if pygame.time.get_ticks() - backspace_start_time >= 50:
                if letters_deleted >= (start_length * 0.6):
                    user_text = ""
                    letters_deleted = 0
                    start_length = 0
                    text_input.add_text(user_text)
                else:
                    user_text = user_text[:-1]
                    letters_deleted += 1
                    text_input.add_text(user_text)
    else:
        backspace_start_time = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                backspace_held = False
                letters_deleted = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_input.is_clicked():
                input_box_active = True
                if user_text == text_input.placeholder:
                    user_text = ""
                    text_input.add_text(user_text)
            if button.is_clicked():
                button_callback()
            elif not text_input.is_clicked() and input_box_active:
                input_box_active = False
                if user_text == "":
                    user_text = text_input.placeholder
                    text_input.add_text(user_text)

        if event.type == pygame.KEYDOWN and input_box_active:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE]) or (keys[pygame.K_RCTRL] and keys[pygame.K_BACKSPACE]):
                user_text = ""
                text_input.add_text(user_text)
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key != pygame.K_RETURN:
                if len(user_text) < 20:
                    user_text += event.unicode
                    start_length = len(user_text)
            elif event.key == pygame.K_RETURN:
                if user_text == "":
                    user_text = text_input.placeholder
                    text_input.add_text(user_text)
                else:
                    text_input_callback(user_text)
                    user_text = text_input.placeholder
            text_input.add_text(user_text)
    
    button.draw()
    text_input.draw()

    pygame.display.update()
    pygame.display.flip()

pygame.quit()