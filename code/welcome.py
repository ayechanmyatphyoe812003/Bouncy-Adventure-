from os.path import join
import pygame
import sys

from register import register
from sign_in import login

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

class Button:
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BUTTON_COLOR
        self.text = text
        self.font = font
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


def register_action():
    register()


def login_action():
    login()


# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create buttons
buttons = [
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "Log In", FONT, login_action),
    Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 370, BUTTON_WIDTH, BUTTON_HEIGHT, "Register", FONT, register_action),

]

def draw_title(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        for button in buttons:
            button.handle_event(event)

    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw title
    draw_title(screen, "BOUNCY ADVENTURE", TITLE_FONT, BUTTON_TEXT_COLOR, SCREEN_WIDTH // 2, 200)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Update display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
