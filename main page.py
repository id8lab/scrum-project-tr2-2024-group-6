import pygame

# Define screen dimensions
WIDTH = 480
HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight adventure")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

# Game statistics
game_data = {
    "high_score": 0,
    "games_played": 0,
    "enemies_killed": 0
}

def draw_text(surf, text, size, x, y, align="midtop"):
    """Draw text on the screen."""
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    setattr(text_rect, align, (x, y))
    surf.blit(text_surface, text_rect)

class Button:
    """Class for creating interactive buttons."""
    def __init__(self, text, x, y, width, height, color, hover_color, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.callback = callback

    def draw(self, screen):
        """Draw the button on the screen."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)
        draw_text(screen, self.text, 20, self.rect.centerx, self.rect.centery, align="center")

    def handle_event(self, event):
        """Handle button click events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

def start_game():
    """Callback function to start the game."""
    global main_menu
    main_menu = False

def show_main_menu():
    """Function to display the main menu."""
    start_button = Button("Start", WIDTH // 2 - 50, HEIGHT // 2, 100, 50, GREEN, YELLOW, start_game)
    global main_menu
    main_menu = True
    while main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            start_button.handle_event(event)

        screen.fill(BLACK)
        draw_text(screen, "Knight adventure", 64, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, f"High Score: {game_data['high_score']}", 22, WIDTH - 10, 10, align="topright")  # Top right corner
        draw_text(screen, f"Games Played: {game_data['games_played']}", 22, WIDTH // 2, 10, align="midtop")  # Top center
        draw_text(screen, f"Enemies Killed: {game_data['enemies_killed']}", 22, 10, 10, align="topleft")  # Top left corner
        start_button.draw(screen)
        pygame.display.flip()

# Show main menu
show_main_menu()


