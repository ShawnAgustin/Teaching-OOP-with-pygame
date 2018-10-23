import pygame
import random
import math


white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((600, 600))
w, h = gameDisplay.get_size()
pygame.display.set_caption("Snake")
gameExit = False
scl = 20


class Snake:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xspeed = 1
        self.yspeed = 0
        self.total = 0
        self.tail = []
        self.snake_rect = pygame.Rect(self.x, self.y, 20, 20)

    def show(self):
        for t in self.tail:
            pygame.draw.rect(gameDisplay, green, (t.x, t.y, 20, 20))

        self.snake_rect = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(gameDisplay, green, self.snake_rect)

    def dir(self, x, y):
        self.xspeed = x
        self.yspeed = y

    def update(self):
        for c in range(len(self.tail) - 1):
            self.tail[c] = self.tail[c + 1]

        if len(self.tail) >= 1:
            self.tail[self.total - 1] = pygame.Rect(self.x, self.y, 20, 20)

        self.x = self.x + self.xspeed * 20
        self.y = self.y + self.yspeed * 20

    def eat(self, food):
        if self.snake_rect.colliderect(food.food_rect):
            self.tail.append(self.snake_rect)
            self.total += 1
            return True
        return False

    def restart(self):
        print("Starting Over")
        self.x = 0
        self.y = 0
        self.total = 0
        self.tail = []
        self.dir(1, 0)

    def die(self):
        print(self.snake_rect[0])
        if self.snake_rect[0] > 600 or self.snake_rect[1] > 600 or self.snake_rect[0] < 0 or self.snake_rect[1] < 0:
            self.restart()
        else:
            for t in self.tail:
                if self.snake_rect.colliderect(t):
                    self.restart()


class Food:
    def __init__(self):
        cols = math.floor(w / scl)
        rows = math.floor(h / scl)

        randx = math.floor(random.randint(0, cols-1)) * 20
        randy = math.floor(random.randint(0, rows-1)) * 20

        self.food_rect = pygame.Rect(randx, randy, 20, 20)

    def show(self):
        pygame.draw.rect(gameDisplay, red, self.food_rect)


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



s = Snake()
f = Food()

while not gameExit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                s.dir(0, -1)
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                s.dir(0, 1)
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                s.dir(1, 0)
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                s.dir(-1, 0)


    gameDisplay.fill(black)

    if s.eat(f):
        f = Food()
    s.update()
    s.show()
    s.die()
    f.show()

    draw_text(gameDisplay, str("Score: {}".format(s.total)), 50, 400, 550)
    clock.tick(20)
    pygame.display.update()