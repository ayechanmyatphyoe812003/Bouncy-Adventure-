from os.path import join
import pygame
import sys
import sqlite3
from main import Game  # Ensure this imports the correct Game class

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BG_COLOR = (255, 255, 255)
BUTTON_COLOR = (89, 245, 165)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_GAP = 20
FONT_PATH = join('..', 'graphics', 'ui', 'runescape_uf.ttf')
FONT = pygame.font.Font(FONT_PATH, 36)
TITLE_FONT = pygame.font.Font(FONT_PATH, 72)
TITLE_FONT = pygame.font.Font(FONT_PATH, 72)
TABLE_FONT = pygame.font.Font(FONT_PATH, 24)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = FONT.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

def start_game(player_id):
    try:
        game = Game(player_id, menu)  # Pass menu function to Game
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")

def settings_action():
    print("Settings button clicked")

def exit_game():
    pygame.quit()
    sys.exit()

def get_top_players():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, current_level FROM users ORDER BY current_level DESC LIMIT 5")
    top_players = cursor.fetchall()
    conn.close()
    return top_players

def leaderboard_action(player_id):
    top_players = get_top_players()
    display_leaderboard(top_players, player_id)

def draw_title(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def display_leaderboard(top_players, player_id):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Leaderboard")

    def go_back():
        menu(player_id)

    back_button = Button(50, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", go_back)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            back_button.handle_event(event)

        screen.fill(BG_COLOR)

        draw_title(screen, "Leaderboard", TITLE_FONT, BUTTON_TEXT_COLOR, SCREEN_WIDTH // 2, 100)

        # Display table headers
        headers = ["Rank", "Username", "Level"]
        header_x_positions = [SCREEN_WIDTH // 4, SCREEN_WIDTH // 2, SCREEN_WIDTH * 3 // 4]
        for i, header in enumerate(headers):
            header_surface = TABLE_FONT.render(header, True, BUTTON_TEXT_COLOR)
            header_rect = header_surface.get_rect(center=(header_x_positions[i], 200))
            screen.blit(header_surface, header_rect)

        # Display the top 5 players in a table format
        y_offset = 250
        for idx, player in enumerate(top_players):
            rank_surface = TABLE_FONT.render(str(idx + 1), True, BUTTON_TEXT_COLOR)
            username_surface = TABLE_FONT.render(player[0], True, BUTTON_TEXT_COLOR)
            level_surface = TABLE_FONT.render(str(player[1]), True, BUTTON_TEXT_COLOR)

            rank_rect = rank_surface.get_rect(center=(header_x_positions[0], y_offset))
            username_rect = username_surface.get_rect(center=(header_x_positions[1], y_offset))
            level_rect = level_surface.get_rect(center=(header_x_positions[2], y_offset))

            screen.blit(rank_surface, rank_rect)
            screen.blit(username_surface, username_rect)
            screen.blit(level_surface, level_rect)

            y_offset += 50

        back_button.draw(screen)

        pygame.display.flip()

    pygame.quit()

def menu(player_id):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    button_y_start = SCREEN_HEIGHT // 2 - (BUTTON_HEIGHT * 2 + BUTTON_GAP * 3) // 2
    buttons = [
        Button(button_x, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT, "Start", lambda: start_game(player_id)),
        Button(button_x, button_y_start + BUTTON_HEIGHT + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", settings_action),
        Button(button_x, button_y_start + 2 * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH, BUTTON_HEIGHT, "Leaderboard", lambda: leaderboard_action(player_id)),
        Button(button_x, button_y_start + 3 * (BUTTON_HEIGHT + BUTTON_GAP), BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", exit_game)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        screen.fill(BG_COLOR)
        draw_title(screen, "Let's bounce", TITLE_FONT, BUTTON_TEXT_COLOR, SCREEN_WIDTH // 2, 150)
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    player_id = input("Enter player ID: ")
    try:
        player_id = int(player_id)
    except ValueError:
        print("Invalid player ID. Must be an integer.")
        sys.exit()
    menu(player_id)
