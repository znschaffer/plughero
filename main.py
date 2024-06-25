from pygame.sprite import Group
from typing_extensions import Tuple
import pygame
import random

WIDTH = 300
HEIGHT = 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((0, 255, 255))
pygame.init()
vec = pygame.math.Vector2
gamestate = 0

enemies = ["jack", "xlr"]


class Jack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.target = False
        self.jack_type = random.choice(enemies)
        if self.jack_type == "jack":
            self.target = True
        self.image = pygame.image.load(
            f"data/assets/{self.jack_type}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(random.randint(64, WIDTH - 64), 0)
        self.acc = random.randint(300, 700)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.pos.y += self.acc * dt
        if self.pos.y > HEIGHT:
            if self.jack_type == "xlr":
                plug_group.remove(self)
            else:
                global gamestate
                gamestate = -1

        self.rect.center = (int(self.pos.x), int(self.pos.y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/assets/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(WIDTH // 2, HEIGHT - 64)
        self.dir = 0
        self.speed = 500

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.acc = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dir = -1
        elif keys[pygame.K_RIGHT]:
            self.dir = 1
        else:
            self.dir = 0

        self.pos.x += self.dir * self.speed * dt
        if self.pos.x < 8:
            self.pos.x = 8
        elif self.pos.x > WIDTH:
            self.pos.x = WIDTH
        self.rect.center = (int(self.pos.x), int(self.pos.y))


P1 = Player()

plug_group = pygame.sprite.Group()


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data/assets/background.png")
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH // 2, HEIGHT // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, dt):
        self.scrollY(300 * dt)

    def scrollY(self, offsetY):
        width, height = self.image.get_size()
        copySurf = self.image.copy()
        self.image.blit(copySurf, (0, offsetY))
        if offsetY < 0:
            self.image.blit(copySurf, (0, height + offsetY), (0, 0, width, -offsetY))
        else:
            self.image.blit(copySurf, (0, 0), (0, height - offsetY, width, offsetY))


def background():
    SCREEN.fill("white")


bg = Background()

clock = pygame.time.Clock()

score = 0
font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 40)
pygame.time.set_timer(pygame.USEREVENT, 750)
scoreSFX = pygame.mixer.Sound("data/audio/pickupCoin.wav")
scoreSFX.set_volume(0.1)


def scoreboard():
    show_score = font.render(str(score), True, (0, 0, 0))
    score_rect = show_score.get_rect(center=(WIDTH // 2, 30))
    SCREEN.blit(show_score, score_rect)


def main():
    running = True

    pygame.display.set_caption("Plug Hero")
    pygame.mixer.music.load("data/audio/sleigh_ride.ogg")
    pygame.mixer.music.play()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                plug_group.add(Jack())

        dt = clock.tick(120) / 1000
        bg.update(dt)
        bg.draw(SCREEN)
        P1.update(dt)

        global gamestate
        plug_group.update(dt)
        plug_group.draw(SCREEN)
        collisions = pygame.sprite.spritecollide(
            P1, plug_group, True, pygame.sprite.collide_mask
        )
        if collisions:
            for c in collisions:
                if c.jack_type == "xlr":
                    gamestate = -1
            global score
            score += 1
            pygame.mixer.Sound.play(scoreSFX)

        P1.draw(SCREEN)
        scoreboard()
        pygame.display.update()
        if gamestate == -1:
            plug_group.empty()
            score = 0
            gamestate = 0

    pygame.quit()


main()
