class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, bullet_type):
        pygame.sprite.Sprite.__init__(self)
        if bullet_type == "player":
            self.image = pygame.image.load('player bullets.png').convert_alpha()
        else:  # bullet_type == "enemy"
            self.image = pygame.image.load('enemy bullets.png').convert_alpha()
            # self.image = pygame.transform.rotate(self.image, 180)  # 移除旋转操作
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
