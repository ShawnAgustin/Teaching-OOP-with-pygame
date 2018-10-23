import pygame
import random
import math


white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((600, 600))
w, h = gameDisplay.get_size()
pygame.display.set_caption("Flappy")
gameExit = False


class Bird:

    def __init__(self):
        self.x = 200
        self.y = 100
        self.gravity = 0.6
        self.lift = -10
        self.velocity = 0

        self.bird_rect = pygame.Rect(self.x, self.y, 20, 20)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y >= 600:
            self.y = h-20;
            self.velocity = 0

        self.bird_rect = pygame.Rect(self.x, self.y, 20, 20)

    def bounce(self):
        self.velocity = self.lift

    def show(self):
        pygame.draw.ellipse(gameDisplay, red, self.bird_rect)


class Obstacle:

    def __init__(self):
        self.top = random.randint(0,h/2)
        self.bottom = random.randint(0,h/2)
        self.x = w
        self.w = 50
        self.speed = 3
        self.passed = False
        self.highlight = False

        self.obs_rect_up = pygame.Rect(self.x, 0, self.w, self.top)
        self.obs_rect_down = pygame.Rect(self.x, h-self.bottom, self.w, self.bottom)

    def show(self):
        colour = green
        if self.highlight:
            colour = blue
        pygame.draw.rect(gameDisplay, colour, self.obs_rect_up)
        pygame.draw.rect(gameDisplay, colour, self.obs_rect_down)

    def update(self):
        self.x -= self.speed
        self.obs_rect_up = pygame.Rect(self.x, 0, self.w, self.top)
        self.obs_rect_down = pygame.Rect(self.x, h - self.bottom, self.w, self.bottom)

    def off_screen(self):
        if self.x < -self.w:
            return True
        return False

    def hits_bird(self, bird):
        if self.obs_rect_up.colliderect(bird.bird_rect):
            self.highlight = True
            return True
        if self.obs_rect_down.colliderect(bird.bird_rect):
            self.highlight = True
            return True

        return False


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


b = Bird()
obs = [Obstacle()]

frameCount = 0
while not gameExit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                b.bounce()

    if frameCount % 100 == 0:
        obs.append(Obstacle())

    gameDisplay.fill(white)
    b.show()
    b.update()

    for o in obs:
        if o.off_screen():
            obs.remove(o)
        o.show()
        o.update()

        if o.hits_bird(b):
            print("hit")


    draw_text(gameDisplay, str("Score: {}".format(0)), 50, 400, 550)

    clock.tick(60)
    frameCount += 1
    pygame.display.update()