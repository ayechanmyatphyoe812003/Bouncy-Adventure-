from os.path import join

import pygame
import sqlite3
from pygame.locals import *
import sys
from main import Game
from menu import menu

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Sign In')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fonts
FONT_PATH = join('..', 'graphics', 'ui', 'runescape_uf.ttf')
font = pygame.font.Font(FONT_PATH, 45)
small_font = pygame.font.Font(FONT_PATH, 24)

# SQLite database connection and cursor
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Function to display text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Function to validate login credentials and show login form
def login():
    username_input = ""
    password_input = ""
    active_input = None  # Track which input field is currently active
    error_message = ""  # Variable to store error messages

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    # Perform login when Enter key is pressed
                    if username_input:
                        cursor.execute('''
                            SELECT * FROM users
                            WHERE username = ?;
                        ''', (username_input,))
                        user = cursor.fetchone()
                        # print(user)
                        if user:
                            # Transition to main menu here
                            player_id = user[0]  # Assuming player_id is in the first column
                            start_level = user[4]
                            menu(player_id)
                        else:
                            error_message = "Invalid username or password."
                    else:
                        error_message = "Please fill in both fields."

                elif event.key == K_BACKSPACE:
                    # Handle backspace to delete characters from inputs
                    if active_input == 'username' and len(username_input) > 0:
                        username_input = username_input[:-1]
                    elif active_input == 'password' and len(password_input) > 0:
                        password_input = password_input[:-1]
                else:
                    # Add characters to inputs
                    if active_input == 'username' and len(username_input) < 20 and event.unicode.isalnum():
                        username_input += event.unicode
                    elif active_input == 'password' and len(password_input) < 20:
                        password_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is within the bounds of text input fields
                x, y = pygame.mouse.get_pos()
                if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and screen_height // 2 - 25 <= y <= screen_height // 2 + 5:
                    active_input = 'username'
                elif screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and screen_height // 2 + 50 <= y <= screen_height // 2 + 80:
                    active_input = 'password'
                else:
                    active_input = None

        # Display sign in form
        draw_text('Log In', font, BLACK, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text('Username', small_font, BLACK, screen, screen_width // 2, screen_height // 2 - 50)
        draw_text('Password', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 30)

        pygame.draw.rect(screen, BLACK if active_input == 'username' else GRAY, (screen_width // 2 - 100, screen_height // 2 - 25, 200, 30), 2)
        pygame.draw.rect(screen, BLACK if active_input == 'password' else GRAY, (screen_width // 2 - 100, screen_height // 2 + 50, 200, 30), 2)

        draw_text(username_input, small_font, BLACK, screen, screen_width // 2, screen_height // 2 - 10)
        draw_text("*" * len(password_input), small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 65)

        # Display error message if any
        if error_message:
            draw_text(error_message, small_font, RED, screen, screen_width // 2, screen_height // 2 + 120)

        pygame.display.flip()

# Close database connection
def close_connection():
    conn.close()

# Call this to run the login form
if __name__ == "__main__":
    login()
    close_connection()