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
def Enemy(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((30, 40))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            # 设置敌人出现的随机位置
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            # 设置敌人的随机速度
            self.speedy = random.randrange(1, 8)
            self.speed
            self.speedx = random.randrange(-3, 3)  # 如果需要水平移动的话

        def update(self):
            # 更新敌人的位置
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            # 边界检查，如果敌人超出屏幕底部，重新放置到屏幕顶部
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)

    all_sprites = pygame.sprite.Group()