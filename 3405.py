import pygame
import random
import sys

WIDTH = 640  # 增加总宽度来容纳分数板
HEIGHT = 600
GAME_WIDTH = 480  # 游戏内容的宽度
SCOREBOARD_WIDTH = WIDTH - GAME_WIDTH  # 分数板的宽度
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

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
explosion_sound = pygame.mixer.Sound('death.mp3')

# Load explosion image
explosion_image = pygame.image.load('explosion.png').convert_alpha()
explosion_image = pygame.transform.scale(explosion_image, (30, 40))

# Load red and green star images
red_star_image = pygame.image.load('red_star.png').convert_alpha()
red_star_image = pygame.transform.scale(red_star_image, (20, 20))
green_star_image = pygame.image.load('green_star.png').convert_alpha()
green_star_image = pygame.transform.scale(green_star_image, (20, 20))

# Load and scale frame images
frame_files = [
    'frame_1.png', 'frame_2.png', 'frame_3.png', 'frame_4.png',
    'frame_5.png', 'frame_6.png', 'frame_7.png', 'frame_8.png',
    'frame_9.png', 'frame_10.png', 'frame_11.png', 'frame_12.png',
    'frame_13.png', 'frame_14.png'
]

frames = []
for file in frame_files:
    img = pygame.image.load(file).convert_alpha()
    if 'frame_8' in file or 'frame_9' in file or 'frame_10' in file or 'frame_11' in file or 'frame_12' in file or 'frame_13' in file or 'frame_14' in file:
        img = pygame.transform.scale(img, (50, 50))  # Scale walking character to smaller size
    else:
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))  # Scale background images to fit the screen width and height
    frames.append(img)

# Load and scale knight image
knight_image = pygame.image.load('knight2.png').convert_alpha()
knight_image = pygame.transform.scale(knight_image, (SCOREBOARD_WIDTH, SCOREBOARD_WIDTH))

# Font for drawing text
font_name = pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_scoreboard(surface, score, health, enemies_killed, bombs):
    surface.fill(BLACK)
    x = SCOREBOARD_WIDTH / 2
    y = 50
    draw_text(surface, f'HiScore: {score}', 18, x, y, WHITE)
    draw_text(surface, f'Score: {score}', 18, x, y + 30, WHITE)
    draw_text(surface, f'Player:', 18, x - 20, y + 60, RED)
    for i in range(health):
        surface.blit(red_star_image, (x + i * 25, y + 60))
    draw_text(surface, f'Bomb:', 18, x - 20, y + 90, GREEN)
    for i in range(bombs):
        surface.blit(green_star_image, (x + i * 25, y + 90))
    draw_text(surface, f'Enemies Killed: {enemies_killed}', 18, x, y + 120, GREEN)

def main_menu(screen, frames):
    frame_count = len(frames)
    current_frame = 0
    last_update = pygame.time.get_ticks()
    frame_rate = 150  # 控制动画速度

    while True:
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:
            last_update = now
            current_frame = (current_frame + 1) % frame_count

        screen.blit(frames[current_frame], (0, 0))
        draw_text(screen, "Knight's Adventure", 48, WIDTH / 2, HEIGHT / 4, YELLOW)
        draw_text(screen, "Single Player", 28, WIDTH / 2, HEIGHT / 2, YELLOW)
        draw_text(screen, "Multiplayer", 28, WIDTH / 2, HEIGHT / 2 + 50, YELLOW)
        draw_text(screen, "Settings", 28, WIDTH / 2, HEIGHT / 2 + 100, YELLOW)
        draw_text(screen, "Quit", 28, WIDTH / 2, HEIGHT / 2 + 150, YELLOW)

        if current_frame >= 7:  # Display walking character frames
            screen.blit(frames[current_frame], (WIDTH / 2 + 100, HEIGHT / 2 + 150))  # Adjust position to be next to "Quit"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if WIDTH / 2 - 100 < x < WIDTH / 2 + 100:
                    if HEIGHT / 2 - 20 < y < HEIGHT / 2 + 20:
                        return SINGLE_PLAYER
                    elif HEIGHT / 2 + 30 < y < HEIGHT / 2 + 70:
                        return MULTI_PLAYER
                    elif HEIGHT / 2 + 80 < y < HEIGHT / 2 + 120:
                        return SETTINGS
                    elif HEIGHT / 2 + 130 < y < HEIGHT / 2 + 170:
                        pygame.quit()
                        sys.exit()

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
    background = pygame.transform.scale(background, (GAME_WIDTH, HEIGHT))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("knight1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 50))
            self.rect = self.image.get_rect()
            self.rect.centerx = GAME_WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0
            self.speedy = 0
            self.health = 3
            self.bombs = 3
            self.enemies_killed = 0

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

            if self.rect.right > GAME_WIDTH:
                self.rect.right = GAME_WIDTH
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

        def use_bomb(self, enemies, enemy_bullets):
            if self.bombs > 0:
                self.bombs -= 1
                for enemy in enemies:
                    explosion = Explosion(enemy.rect.center)
                    all_sprites.add(explosion)
                    explosion_sound.play()
                    enemy.kill()
                    global score
                    score += 10
                    self.enemies_killed += 1
                    new_enemy = Enemy()
                    all_sprites.add(new_enemy)
                    enemies.add(new_enemy)
                for bullet in enemy_bullets:
                    bullet.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("Monster.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 40))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(GAME_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > GAME_WIDTH + 20:
                self.rect.x = random.randrange(GAME_WIDTH - self.rect.width)
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

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center):
            pygame.sprite.Sprite.__init__(self)
            self.image = explosion_image
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50  # 控制动画速度

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == 9:
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = explosion_image
                    self.rect = self.image.get_rect()
                    self.rect.center = center

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

    global score
    score = 0
    enemies_killed = 0

    scoreboard_surface = pygame.Surface((SCOREBOARD_WIDTH, HEIGHT))

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key in (pygame.K_q, pygame.K_q):
                    player.use_bomb(enemies, enemy_bullets)

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        for hit in hits:
            score += 10
            enemies_killed += 1
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosion_sound.play()
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            player.enemies_killed += 1
            if player.enemies_killed % 10 == 0:
                player.bombs += 1

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
        draw_scoreboard(scoreboard_surface, score, player.health, enemies_killed, player.bombs)
        screen.blit(scoreboard_surface, (GAME_WIDTH, 0))
        screen.blit(knight_image, (GAME_WIDTH, HEIGHT - SCOREBOARD_WIDTH))
        pygame.display.flip()

    game_over_screen(screen)

game_state = MAIN_MENU

while True:
    if game_state == MAIN_MENU:
        game_state = main_menu(screen, frames)
    elif game_state == SINGLE_PLAYER:
        single_player_game(screen)
    elif game_state == MULTI_PLAYER:
        print("Multiplayer settings")
    elif game_state == SETTINGS:
        print("Game settings")

    pygame.display.update()
    clock.tick(FPS)
