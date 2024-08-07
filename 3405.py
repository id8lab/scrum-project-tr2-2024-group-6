import pygame
import random
import sys

WIDTH = 640
HEIGHT = 600
GAME_WIDTH = 480
SCOREBOARD_WIDTH = WIDTH - GAME_WIDTH
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

MAIN_MENU = 0
SINGLE_PLAYER = 1
MULTI_PLAYER = 2
SETTINGS = 3
GAME_OVER = 4
HIGH_SCORES = 5

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Adventure")
clock = pygame.time.Clock()

pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound('shoot.mp3')
player_hit_sound = pygame.mixer.Sound('death.mp3')
player_death_sound = pygame.mixer.Sound('death.mp3')
explosion_sound = pygame.mixer.Sound('death.mp3')

explosion_image = pygame.image.load('explosion.png').convert_alpha()
explosion_image = pygame.transform.scale(explosion_image, (30, 40))

red_star_image = pygame.image.load('red_star.png').convert_alpha()
red_star_image = pygame.transform.scale(red_star_image, (20, 20))
green_star_image = pygame.image.load('green_star.png').convert_alpha()
green_star_image = pygame.transform.scale(green_star_image, (20, 20))

frame_files = [
    'frame_1.png', 'frame_2.png', 'frame_3.png', 'frame_4.png',
    'frame_5.png', 'frame_6.png', 'frame_7.png', 'frame_8.png',
    'frame_9.png', 'frame_10.png', 'frame_11.png', 'frame_12.png',
    'frame_13.png', 'frame_14.png'
]

difficulty_settings = {
    "Easy": {"enemy_count": 5, "game_speed": 1},
    "Medium": {"enemy_count": 10, "game_speed": 1.5},
    "Hard": {"enemy_count": 15, "game_speed": 2}
}
selected_difficulty = "Medium"

frames = []
for file in frame_files:
    img = pygame.image.load(file).convert_alpha()
    if 'frame_8' in file or 'frame_9' in file or 'frame_10' in file or 'frame_11' in file or 'frame_12' in file or 'frame_13' in file or 'frame_14' in file:
        img = pygame.transform.scale(img, (50, 50))
    else:
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    frames.append(img)

knight_image = pygame.image.load('knight2.png').convert_alpha()
knight_image = pygame.transform.scale(knight_image, (SCOREBOARD_WIDTH, SCOREBOARD_WIDTH))

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

    # 读取最高分
    high_scores = get_high_scores()
    hiscore = high_scores[0] if high_scores else 0

    draw_text(surface, f'Highest score: {hiscore}', 18, x, y, WHITE)
    draw_text(surface, f'Score: {score}', 18, x, y + 30, WHITE)
    draw_text(surface, f'Player:', 18, x - 20, y + 60, RED)
    for i in range(health):
        surface.blit(red_star_image, (x + i * 25, y + 60))
    draw_text(surface, f'Bomb:', 18, x - 20, y + 90, GREEN)
    for i in range(bombs):
        surface.blit(green_star_image, (x + i * 25, y + 90))
    draw_text(surface, f'Enemies Killed: {enemies_killed}', 18, x, y + 120, GREEN)


def get_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            scores = file.readlines()
        return [int(score.strip()) for score in scores]
    except FileNotFoundError:
        return [0] * 5

def update_high_scores(new_score):
    scores = get_high_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:5]
    with open('high_scores.txt', 'w') as file:
        for score in scores:
            file.write(f"{score}\n")

def show_high_scores(screen):
    screen.fill(BLACK)
    draw_text(screen, "High Scores", 48, WIDTH / 2, HEIGHT / 4, YELLOW)
    high_scores = get_high_scores()
    y = HEIGHT / 2 - 100
    for i, score in enumerate(high_scores):
        draw_text(screen, f"{i + 1}. {score}", 28, WIDTH / 2, y, WHITE)
        y += 40
    draw_text(screen, "Press ESC to return to main menu", 22, WIDTH / 2, y + 50, YELLOW)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

def settings_menu(screen):
    global selected_difficulty
    slider_rect = pygame.Rect(100, HEIGHT // 2, WIDTH - 200, 10)
    slider_knob_rect = pygame.Rect(slider_rect.x, slider_rect.y - 10, 20, 30)
    dragging = False
    volume = pygame.mixer.music.get_volume()

    difficulty_buttons = {
        "Easy": pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 130, 60),
        "Medium": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 100, 130, 60),
        "Hard": pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 100, 130, 60)
    }

    return_button_rect = pygame.Rect(10, HEIGHT - 100, 85, 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_knob_rect.collidepoint(event.pos):
                    dragging = True
                elif return_button_rect.collidepoint(event.pos):
                    return
                for difficulty, rect in difficulty_buttons.items():
                    if rect.collidepoint(event.pos):
                        selected_difficulty = difficulty
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    slider_knob_rect.x = max(slider_rect.x, min(event.pos[0],
                                                                slider_rect.x + slider_rect.width - slider_knob_rect.width))
                    volume = (slider_knob_rect.x - slider_rect.x) / (slider_rect.width - slider_knob_rect.width)
                    pygame.mixer.music.set_volume(volume)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return

        screen.fill(WHITE)
        draw_text(screen, "Settings", 48, WIDTH // 2, HEIGHT // 4 - 50, BLACK)
        draw_text(screen, "Adjust Volume", 28, WIDTH // 2, HEIGHT // 2 - 60, BLACK)
        pygame.draw.rect(screen, BLACK, slider_rect)
        pygame.draw.ellipse(screen, BLACK, slider_knob_rect)

        draw_text(screen, "Current Difficulty: " + selected_difficulty, 28, WIDTH // 2, HEIGHT // 2 + 50, BLACK)

        for difficulty, rect in difficulty_buttons.items():
            pygame.draw.rect(screen, BLACK, rect)
            draw_text(screen, difficulty, 28, rect.centerx, rect.centery, WHITE)

        pygame.draw.rect(screen, BLACK, return_button_rect)
        draw_text(screen, "Return", 20, return_button_rect.centerx, return_button_rect.centery, WHITE)

        pygame.display.flip()
        clock.tick(FPS)

def main_menu(screen, frames):
    frame_count = len(frames)
    current_frame = 0
    last_update = pygame.time.get_ticks()
    frame_rate = 60

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
        draw_text(screen, "High Scores", 28, WIDTH / 2, HEIGHT / 2 + 150, YELLOW)
        draw_text(screen, "Quit", 28, WIDTH / 2, HEIGHT / 2 + 200, YELLOW)

        if current_frame >= 7:
            screen.blit(frames[current_frame], (WIDTH / 2 + 100, HEIGHT / 2 + 150))

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
                        return HIGH_SCORES
                    elif HEIGHT / 2 + 180 < y < HEIGHT / 2 + 220:
                        pygame.quit()
                        sys.exit()


def game_over_screen(screen, score):
    # 更新最高分
    update_high_scores(score)

    # 填充屏幕黑色背景
    screen.fill(BLACK)

    # 绘制 GAME OVER 文本
    draw_text(screen, "GAME OVER", 80, WIDTH / 2, HEIGHT / 8, RED)

    # 绘制分数文本
    draw_text(screen, f"Your Score: {score}", 22, WIDTH / 2, HEIGHT / 3, WHITE)

    # 绘制“查看最高分”框
    box_width, box_height = 200, 50
    box_x = WIDTH / 2 - box_width / 2
    box_y = HEIGHT / 2 + 20
    pygame.draw.rect(screen, YELLOW, (box_x, box_y, box_width, box_height))
    draw_text(screen, "View High Scores", 22, WIDTH / 2, box_y + box_height / 2, BLACK)

    # 绘制“按任意键重新开始”文本
    draw_text(screen, "Press any key to Restart the game", 22, WIDTH / 2, HEIGHT * 5 / 6, WHITE)

    pygame.display.flip()

    # 等待玩家输入
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key != pygame.K_c:  # 任何键除 'C' 外
                    waiting = False
                    return SINGLE_PLAYER
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if box_x < x < box_x + box_width and box_y < y < box_y + box_height:
                    return HIGH_SCORES



def single_player_game(screen):
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, (GAME_WIDTH, 1000))

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
            self.invincible = False
            self.invincible_timer = 0

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

            if self.invincible:
                now = pygame.time.get_ticks()
                if now - self.invincible_timer > 2000:
                    self.invincible = False
                    self.image.set_alpha(255)  # 重置透明度
                else:
                    if (now - self.invincible_timer) % 500 < 250:
                        self.image.set_alpha(128)
                    else:
                        self.image.set_alpha(255)
                print("Invincible:", self.invincible, "Time left:", 2000 - (now - self.invincible_timer))

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

        def hit(self):
            if not self.invincible:
                self.health -= 1
                if self.health <= 0:
                    self.kill()
                else:
                    self.invincible = True
                    self.invincible_timer = pygame.time.get_ticks()
                player_hit_sound.play()

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

    difficulty = difficulty_settings[selected_difficulty]
    for i in range(difficulty["enemy_count"]):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    global score
    score = 0
    enemies_killed = 0

    scoreboard_surface = pygame.Surface((SCOREBOARD_WIDTH, HEIGHT))

    background_y = 0
    background_speed = 2

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
            player.hit()
            if player.health <= 0:
                player_death_sound.play()
                pygame.time.wait(1000)  # Wait for a second to allow death sound to play
                running = False

        background_y += background_speed
        if background_y >= HEIGHT:
            background_y = 0

        screen.blit(background, (0, background_y - HEIGHT))
        screen.blit(background, (0, background_y))

        all_sprites.draw(screen)
        draw_scoreboard(scoreboard_surface, score, player.health, enemies_killed, player.bombs)
        screen.blit(scoreboard_surface, (GAME_WIDTH, 0))
        screen.blit(knight_image, (GAME_WIDTH, HEIGHT - SCOREBOARD_WIDTH))
        pygame.display.flip()

    return game_over_screen(screen, score)



game_state = MAIN_MENU

while True:
    if game_state == MAIN_MENU:
        game_state = main_menu(screen, frames)
    elif game_state == SINGLE_PLAYER:
        game_state = single_player_game(screen)
    elif game_state == MULTI_PLAYER:
        print("Multiplayer settings")
    elif game_state == SETTINGS:
        settings_menu(screen)
        game_state = MAIN_MENU
    elif game_state == HIGH_SCORES:
        show_high_scores(screen)
        game_state = MAIN_MENU

    pygame.display.update()
    clock.tick(FPS)
