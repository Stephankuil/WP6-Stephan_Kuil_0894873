import pygame
import sys


class LobbyScreen:
    """
    This class creates and controls the lobby screen.

    The purpose of this screen is:
    1. Let the player type a player name
    2. Let the player type a room code
    3. Let the player choose whether to host or join a room
    4. Let the player go back to the home screen

    This screen keeps running until the player:
    - clicks "Host Room"
    - clicks "Join Room"
    - clicks "Back"
    - or closes the window
    """

    def __init__(self, window, width, height):
        """
        The constructor prepares everything the lobby screen needs.

        Parameters:
        - window: the pygame window/surface where everything will be drawn
        - width: width of the game window
        - height: height of the game window
        """

        # Save the pygame window so we can draw on it later
        self.window = window

        # Save the window size
        self.width = width
        self.height = height

        # ---------------------------------------------------------
        # FONTS
        # ---------------------------------------------------------
        # We create different fonts for different UI elements.
        # Bigger font for the title, smaller font for labels and buttons.
        self.title_font = pygame.font.SysFont(None, 70)
        self.label_font = pygame.font.SysFont(None, 40)
        self.input_font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 36)

        # ---------------------------------------------------------
        # TEXT VALUES
        # ---------------------------------------------------------
        # These variables store what the player types.
        # At first, both are empty strings.
        self.player_name = ""
        self.room_code = ""

        # ---------------------------------------------------------
        # ACTIVE INPUT
        # ---------------------------------------------------------
        # This tells the program which text box is currently selected.
        # If active_input == "name", typing goes into player_name
        # If active_input == "room", typing goes into room_code
        self.active_input = "name"

        # ---------------------------------------------------------
        # BUTTON RECTANGLES
        # ---------------------------------------------------------
        # A pygame.Rect is a rectangle object.
        # We use rectangles for clickable areas such as buttons.
        #
        # Format:
        # pygame.Rect(x_position, y_position, width, height)
        #
        # These buttons are centered horizontally.
        self.host_button = pygame.Rect(width // 2 - 120, 320, 240, 50)
        self.join_button = pygame.Rect(width // 2 - 120, 390, 240, 50)
        self.back_button = pygame.Rect(width // 2 - 120, 460, 240, 50)

        # ---------------------------------------------------------
        # INPUT BOX RECTANGLES
        # ---------------------------------------------------------
        # These rectangles are the clickable boxes where the player types text.
        self.name_box = pygame.Rect(width // 2 - 150, 140, 300, 45)
        self.room_box = pygame.Rect(width // 2 - 150, 230, 300, 45)

    def draw(self):
        """
        This method draws the full lobby screen.

        It redraws everything every frame:
        - background
        - title
        - labels
        - input boxes
        - typed text
        - buttons
        - instruction text
        """

        # Fill the whole screen with black
        self.window.fill((0, 0, 0))

        # ---------------------------------------------------------
        # DRAW TITLE
        # ---------------------------------------------------------
        # Create a yellow text surface that says "GAME LOBBY"
        title_surface = self.title_font.render("GAME LOBBY", True, (255, 255, 0))

        # Center the title near the top of the window
        title_rect = title_surface.get_rect(center=(self.width // 2, 60))

        # Draw the title on the window
        self.window.blit(title_surface, title_rect)

        # ---------------------------------------------------------
        # DRAW LABELS
        # ---------------------------------------------------------
        # Labels explain what the player should type in each box
        name_label = self.label_font.render("Player Name:", True, (255, 255, 255))
        room_label = self.label_font.render("Room Code:", True, (255, 255, 255))

        self.window.blit(name_label, (self.width // 2 - 150, 105))
        self.window.blit(room_label, (self.width // 2 - 150, 195))

        # ---------------------------------------------------------
        # HIGHLIGHT THE ACTIVE INPUT BOX
        # ---------------------------------------------------------
        # If the "name" box is active, it gets a cyan border.
        # Otherwise, it gets a white border.
        #
        # Same logic for the room box.
        name_color = (0, 255, 255) if self.active_input == "name" else (255, 255, 255)
        room_color = (0, 255, 255) if self.active_input == "room" else (255, 255, 255)

        # Draw only the border of the rectangles (thickness = 2)
        pygame.draw.rect(self.window, name_color, self.name_box, 2)
        pygame.draw.rect(self.window, room_color, self.room_box, 2)

        # ---------------------------------------------------------
        # DRAW THE TYPED TEXT INSIDE THE INPUT BOXES
        # ---------------------------------------------------------
        name_text = self.input_font.render(self.player_name, True, (255, 255, 255))
        room_text = self.input_font.render(self.room_code, True, (255, 255, 255))

        # Draw the typed text with a small margin inside each box
        self.window.blit(name_text, (self.name_box.x + 10, self.name_box.y + 8))
        self.window.blit(room_text, (self.room_box.x + 10, self.room_box.y + 8))

        # ---------------------------------------------------------
        # DRAW BUTTONS
        # ---------------------------------------------------------
        # Host button = green
        # Join button = blue
        # Back button = red
        pygame.draw.rect(self.window, (0, 180, 0), self.host_button)
        pygame.draw.rect(self.window, (0, 120, 220), self.join_button)
        pygame.draw.rect(self.window, (180, 0, 0), self.back_button)

        # Create the button text
        host_text = self.button_font.render("Host Room", True, (255, 255, 255))
        join_text = self.button_font.render("Join Room", True, (255, 255, 255))
        back_text = self.button_font.render("Back", True, (255, 255, 255))

        # Center the text inside each button rectangle
        self.window.blit(host_text, host_text.get_rect(center=self.host_button.center))
        self.window.blit(join_text, join_text.get_rect(center=self.join_button.center))
        self.window.blit(back_text, back_text.get_rect(center=self.back_button.center))

        # ---------------------------------------------------------
        # DRAW INSTRUCTION TEXT
        # ---------------------------------------------------------
        instruction_text = self.input_font.render(
            "Click a box to type. Enter name and room first.",
            True,
            (180, 180, 180)
        )
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, 540))
        self.window.blit(instruction_text, instruction_rect)

        # ---------------------------------------------------------
        # UPDATE THE SCREEN
        # ---------------------------------------------------------
        # Without this, the new drawing would not appear
        pygame.display.update()

    def handle_text_input(self, event):
        """
        This method handles keyboard input.

        It checks:
        - if the player pressed backspace
        - otherwise, if the pressed key is a printable character

        The typed text is added to the currently active input field.
        """

        # ---------------------------------------------------------
        # HANDLE BACKSPACE
        # ---------------------------------------------------------
        # Backspace removes the last character from the active input string
        if event.key == pygame.K_BACKSPACE:
            if self.active_input == "name":
                self.player_name = self.player_name[:-1]
            elif self.active_input == "room":
                self.room_code = self.room_code[:-1]

        else:
            # -----------------------------------------------------
            # HANDLE NORMAL TYPING
            # -----------------------------------------------------
            # event.unicode contains the typed character
            # isprintable() makes sure it is a visible character
            if event.unicode.isprintable():
                if self.active_input == "name":
                    self.player_name += event.unicode
                elif self.active_input == "room":
                    self.room_code += event.unicode

    def run(self):
        """
        This method runs the lobby screen loop.

        The loop keeps going forever until one of these happens:
        - the player closes the window
        - the player clicks Host Room
        - the player clicks Join Room
        - the player clicks Back

        Return values:
        - ("host", player_name, room_code)
        - ("join", player_name, room_code)
        - "back"
        """

        while True:
            # Draw the screen again every loop iteration
            self.draw()

            # Read all pygame events (mouse, keyboard, quit, etc.)
            for event in pygame.event.get():

                # -------------------------------------------------
                # WINDOW CLOSE EVENT
                # -------------------------------------------------
                # If the player clicks the X button of the window,
                # close pygame and stop the whole program.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # -------------------------------------------------
                # HANDLE MOUSE CLICKS
                # -------------------------------------------------
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If the player clicked on the name input box,
                    # activate the name input
                    if self.name_box.collidepoint(event.pos):
                        self.active_input = "name"

                    # If the player clicked on the room input box,
                    # activate the room input
                    elif self.room_box.collidepoint(event.pos):
                        self.active_input = "room"

                    # If the player clicked the host button,
                    # only continue if both fields contain text
                    elif self.host_button.collidepoint(event.pos):
                        if self.player_name.strip() and self.room_code.strip():
                            return ("host", self.player_name.strip(), self.room_code.strip())

                    # If the player clicked the join button,
                    # only continue if both fields contain text
                    elif self.join_button.collidepoint(event.pos):
                        if self.player_name.strip() and self.room_code.strip():
                            return ("join", self.player_name.strip(), self.room_code.strip())

                    # If the player clicked the back button,
                    # return to the previous screen
                    elif self.back_button.collidepoint(event.pos):
                        return "back"

                # -------------------------------------------------
                # HANDLE KEYBOARD INPUT
                # -------------------------------------------------
                if event.type == pygame.KEYDOWN:
                    self.handle_text_input(event)