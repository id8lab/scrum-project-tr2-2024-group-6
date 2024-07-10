import pygame
import random
import sys

WIDTH = 480
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define game states
MAIN_MENU = 0
SINGLE_PLAYER = 1
MULTI_PLAYER = 2
SETTINGS = 3


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
    all_sprites = pygame.sprite.Group()
