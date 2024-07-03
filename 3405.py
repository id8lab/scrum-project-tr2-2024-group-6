import pygame
import random
import sys

WIDTH = 480
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define game states
MAIN_MENU = 0
SINGLE_PLAYER = 1
MULTI_PLAYER = 2
SETTINGS = 3
GAME_OVER = 4

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Adventure")
clock = pygame.time.Clock()

# Load background music and sound effects
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # Loop background music indefinitely
shoot_sound = pygame.mixer.Sound('shoot.mp3')
player_hit_sound = pygame.mixer.Sound('death.mp3')
player_death_sound = pygame.mixer.Sound('death.mp3')

# Font for drawing text
font_name = pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main_menu(screen):
    screen.fill(WHITE)
    draw_text(screen, "Knight's Adventure", 48, WIDTH / 2, HEIGHT / 4, BLACK)
    draw_text(screen, "Single Player", 22, WIDTH / 2, HEIGHT / 2, BLACK)
    draw_text(screen, "Multiplayer", 22, WIDTH / 2, HEIGHT / 2 + 50, BLACK)
    draw_text(screen, "Settings", 22, WIDTH / 2, HEIGHT / 2 + 100, BLACK)
    draw_text(screen, "Quit", 22, WIDTH / 2, HEIGHT / 2 + 150, BLACK)
    pygame.display.flip()

def game_over_screen(screen):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4, RED)
    draw_text(screen, "Press any key to restart", 22, WIDTH / 2, HEIGHT / 2, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def single_player_game(screen):
    background = pygame.image.load("grassland.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("knight.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 50))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0
            self.speedy = 0
            self.health = 3

        def update(self):
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()

            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            if keystate[pygame.K_UP]:
                self.speedy = -8
            if keystate[pygame.K_DOWN]:
                self.speedy = 8

            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top, -10, "player")
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            shoot_sound.play()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("Monster.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 40))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)
            if random.random() > 0.98:
                self.shoot()

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 10, "enemy")
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            shoot_sound.play()



    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, speed, bullet_type):
            pygame.sprite.Sprite.__init__(self)
            if bullet_type == "player":
                self.image = pygame.image.load('player bullets.png').convert_alpha()
            else:  # bullet_type == "enemy"
                self.image = pygame.image.load('enemy bullets.png').convert_alpha()
                self.image = pygame.transform.rotate(self.image, 180)
            self.image = pygame.transform.scale(self.image, (20, 40))  # 调整图片大小以适应子弹
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = speed
            self.bullet_type = bullet_type

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()

    all_sprites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    enemies_killed = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        for hit in hits:
            score += 10
            enemies_killed += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            player.health -= 1
            player_hit_sound.play()
            if player.health <= 0:
                player_death_sound.play()
                pygame.time.wait(1000)  # Wait for a second to allow death sound to play
                running = False

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, f'Health: {player.health}', 18, WIDTH / 2, 10, BLACK)
        draw_text(screen, f'Score: {score}', 18, WIDTH - 70, 10, BLACK)
        draw_text(screen, f'Enemies Killed: {enemies_killed}', 18, 70, 10, BLACK)
        pygame.display.flip()

    game_over_screen(screen)

game_state = MAIN_MENU

while True:
    if game_state == MAIN_MENU:
        main_menu(screen)
    elif game_state == SINGLE_PLAYER:
        single_player_game(screen)
    elif game_state == MULTI_PLAYER:
        print("Multiplayer settings")
    elif game_state == SETTINGS:
        print("Game settings")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MAIN_MENU:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if WIDTH / 2 - 100 < x < WIDTH / 2 + 100:
                    if HEIGHT / 2 - 20 < y < HEIGHT / 2 + 20:
                        game_state = SINGLE_PLAYER
                    elif HEIGHT / 2 + 30 < y < HEIGHT / 2 + 70:
                        game_state = MULTI_PLAYER
                    elif HEIGHT / 2 + 80 < y < HEIGHT / 2 + 120:
                        game_state = SETTINGS
                    elif HEIGHT / 2 + 130 < y < HEIGHT / 2 + 170:
                        pygame.quit()
                        sys.exit()

    pygame.display.update()
    clock.tick(FPS)



