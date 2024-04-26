import pygame

from utils import TextInput

class Keyboard:
    def __init__(
            self,
            text_input: TextInput = None,
    ):
        # Backspace variables

        self.backspace_start_time = None
        self.backspace_held = False
        self.start_length = 0
        self.letters_deleted = 0
        self.text_input = text_input


        # Mouse variables
        self.input_box_active = False


    def handle_backspace(self, keys, user_text: str):
        self.start_length = len(user_text)
        if keys[pygame.K_BACKSPACE]:
            if self.backspace_start_time is None:
                self.backspace_start_time = pygame.time.get_ticks()
                
            elif pygame.time.get_ticks() - self.backspace_start_time >= 600:
                self.backspace_held = True

            if self.backspace_held and pygame.time.get_ticks() - self.backspace_start_time >= 50:
                if self.letters_deleted >= (self.start_length * 0.6):
                    user_text = ""
                    self.letters_deleted = 0
                    self.start_length = 0
                    self.text_input.add_text(user_text)

                else:
                    user_text = user_text[:-1]
                    self.letters_deleted += 1
                    self.text_input.add_text(user_text)
        else:
            self.backspace_start_time = None
            self.backspace_held = False

        return user_text
    
    def handle_mousedown(self, user_text: str, text_input, button, button_callback):
        if self.text_input.is_clicked():
            pygame.mouse.set_visible(False)
            self.input_box_active = True
            self.text_input.activated = True
            if user_text == self.text_input.placeholder:
                user_text = ""
                text_input.add_text(user_text)

        if button.is_clicked():
            button_callback()

        elif not self.text_input.is_clicked() and self.input_box_active:
            self.input_box_active = False
            self.text_input.activated = False
            if user_text == "":
                user_text = text_input.placeholder
                self.text_input.add_text(user_text)

        return user_text, self.input_box_active
    
    def handle_keydown(self, event, user_text: str, text_input, text_input_callback):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL] and keys[pygame.K_BACKSPACE] and text_input.activated) or (keys[pygame.K_RCTRL] and keys[pygame.K_BACKSPACE] and text_input.activated):
            words = user_text.split(" ")
            if len(words) > 1:
                words = words[:-1]
                user_text = " ".join(words)
            else:
                user_text = ""
            text_input.add_text(user_text)

        elif event.key == pygame.K_BACKSPACE:
            if user_text != text_input.placeholder:
                user_text = user_text[:-1]

        elif event.key != pygame.K_RETURN:
            if len(user_text) < text_input.max_length and self.text_input.activated:
                user_text += event.unicode
                self.start_length = len(user_text)

        elif event.key == pygame.K_RETURN:
            text_input.activated = False
            if user_text == "":
                user_text = text_input.placeholder
                text_input.add_text(user_text)
            elif user_text != text_input.placeholder:
                text_input.add_json(
                        filename="test.json",
                        keys=["test", "test1"],
                        value=user_text
                    )
                text_input_callback(user_text)
                user_text = text_input.placeholder

        text_input.add_text(user_text)
        return user_text