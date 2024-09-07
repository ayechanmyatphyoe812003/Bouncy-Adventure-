from os.path import join
import pygame
import sqlite3
from pygame.locals import *
import sys
from main import Game
import re  # Import regular expressions module for email validation
import bcrypt  # Import bcrypt for password hashing

from menu import menu

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Registration')

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

# Create users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Function to display text on screen
def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y) if center else (x, y))
    surface.blit(textobj, textrect)



def is_valid_email(email):
    pattern = r'^[\w\.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
    return re.match(pattern, email)


# Function to handle registration and insert into SQLite database
def register():
    username_input = ""
    email_input = ""
    password_input = ""
    active_input = None
    error_message = ""

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
                    # Perform registration when Enter key is pressed
                    if username_input and email_input and password_input:
                        if is_valid_email(email_input):
                            try:
                                # Hash the password before storing
                                hashed_password = bcrypt.hashpw(password_input.encode('utf-8'), bcrypt.gensalt())

                                cursor.execute('''
                                    INSERT INTO users (username, email, password)
                                    VALUES (?, ?, ?)
                                ''', (username_input, email_input, hashed_password))
                                conn.commit()

                                # Fetch the user_id for the newly registered user
                                cursor.execute('SELECT id FROM users WHERE username = ?', (username_input,))
                                player_id = cursor.fetchone()[0]

                                # Transition to main menu with player_id
                                menu(player_id)

                                # Optionally, provide feedback to user that registration is successful
                                username_input = ""
                                email_input = ""
                                password_input = ""
                            except sqlite3.IntegrityError:
                                error_message = "Username or email already exists. Please choose another."
                        else:
                            error_message = "Invalid email format. Please enter a valid email."
                    else:
                        error_message = "Please fill in all fields."

                elif event.key == K_BACKSPACE:
                    # Handle backspace to delete characters from inputs
                    if active_input == 'username' and len(username_input) > 0:
                        username_input = username_input[:-1]
                    elif active_input == 'email' and len(email_input) > 0:
                        email_input = email_input[:-1]
                    elif active_input == 'password' and len(password_input) > 0:
                        password_input = password_input[:-1]
                else:
                    # Add characters to inputs
                    if active_input == 'username' and len(username_input) < 20 and event.unicode.isalnum():
                        username_input += event.unicode
                    elif active_input == 'email' and len(email_input) < 50 and (event.unicode.isalnum() or event.unicode in "@._-"):
                        email_input += event.unicode
                    elif active_input == 'password' and len(password_input) < 20:
                        password_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is within the bounds of text input fields
                x, y = pygame.mouse.get_pos()
                if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and screen_height // 2 - 25 <= y <= screen_height // 2 + 5:
                    active_input = 'username'
                elif screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and screen_height // 2 + 50 <= y <= screen_height // 2 + 80:
                    active_input = 'email'
                elif screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and screen_height // 2 + 125 <= y <= screen_height // 2 + 155:
                    active_input = 'password'
                else:
                    active_input = None

        # Display registration form
        draw_text('Sign Up', font, BLACK, screen, screen_width // 2, screen_height // 2 - 100, center=True)
        draw_text('Username', small_font, BLACK, screen, screen_width // 2, screen_height // 2 - 40)
        draw_text('Email', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 30)
        draw_text('Password', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 100)

        pygame.draw.rect(screen, BLACK if active_input == 'username' else GRAY, (screen_width // 2 - 100, screen_height // 2 - 25, 200, 30), 2)
        pygame.draw.rect(screen, BLACK if active_input == 'email' else GRAY, (screen_width // 2 - 100, screen_height // 2 + 50 , 200, 30), 2)
        pygame.draw.rect(screen, BLACK if active_input == 'password' else GRAY, (screen_width // 2 - 100, screen_height // 2 + 125, 200, 30), 2)

        draw_text(username_input, small_font, BLACK, screen, screen_width // 2, screen_height // 2 - 10)
        draw_text(email_input, small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 65)
        draw_text("*" * len(password_input), small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 140)

        if error_message:
            draw_text(error_message, small_font, RED, screen, screen_width // 2, screen_height // 2 + 190, center=True)

        pygame.display.flip()

# Close database connection
def close_connection():
    conn.close()

# Call this to run the register form
if __name__ == "__main__":
    register()
    close_connection()
