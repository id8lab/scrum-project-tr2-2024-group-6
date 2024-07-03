def single_player_game():
    print("Starting Single Player Game...")
    # 初始化Pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Adventure")
    clock = pygame.time.Clock()

    # Load the background image
    background = pygame.image.load("grassland.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))