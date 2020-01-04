import pygame
import random
import os
import sys

size = WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
platforms = []
platform_sprites = pygame.sprite.Group()
mario_sprite = pygame.sprite.Group()

mario_coord = []
cameray = 1


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image
    return image


class Mario(pygame.sprite.Sprite):
    hero_image = load_image('mar.png')

    def __init__(self, x, y):
        super().__init__(mario_sprite)
        self.image = Mario.hero_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.isJump = False
        self.jump_count = 13
        # global mario_coord
        # mario_coord.append(x, y)

    def update(self, x=0):
        global WIDTH, HEIGHT, cameray
        if pygame.sprite.spritecollideany(self, platform_sprites) or self.isJump:
            self.isJump = True
        else:
            self.rect = self.rect.move(0, self.jump_count)

        if self.isJump:
            if self.jump_count >= 0:
                self.rect = self.rect.move(0, -self.jump_count)
                self.jump_count -= 1
            else:
                self.isJump = False
                self.jump_count = 13

        if x != 0:
            if 0 < x < WIDTH - 24:
                self.rect.x = x

        if self.rect.y > HEIGHT:
            terminate()


class Platform(pygame.sprite.Sprite):
    platform_image = load_image('platform1.png')
    broken_pl_image = load_image('platform1.png')

    def __init__(self, x=-80, y=-18):
        super().__init__(all_sprites, platform_sprites)
        self.image = Platform.platform_image
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, 80, 18)

    def update(self):
        global platforms, cameray
        self.rect = self.rect.move(0, cameray)
        check = platforms[1][1] + cameray
        platforms[1][1] += cameray
        global HEIGHT
        if check > HEIGHT:
            platforms.append([random.randint(0, 720), platforms[-1][1] - 20])
            Platform(platforms[-1][0], platforms[-1][1])
            platforms.pop(0)

    def cameray(self):
        global HEIGHT
        self.rect = self.rect.move(0, HEIGHT)


def generatePlatform():
    global HEIGHT, platforms
    on = HEIGHT
    while on > -300:
        x_coord = random.randint(0, 720)
        platforms.append([x_coord, on])
        Platform(x_coord, on)
        on -= 30


def run():
    FPS = 30
    clock = pygame.time.Clock()
    generatePlatform()
    Mario(platforms[1][0], platforms[1][-1] - 35)
    flag = False
    while True:
        for event in pygame.event.get():
            pygame.mouse.set_visible(False)
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
            if event.type == pygame.MOUSEMOTION and flag:
                mario_sprite.update(event.pos[0])
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        mario_sprite.draw(screen)
        if flag:
            mario_sprite.update()
            all_sprites.update()
            platform_sprites.update()
            clock.tick(FPS)
        pygame.display.flip()


run()
