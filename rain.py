import pygame as pg
import random

screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
done = False

class Ball:
    def __init__(self, x, y, gravity):
        self.x = x
        self.y = y
        self.gravity = gravity
        self.velocity = 0
        self.radius = 5
        self.ball_rect = pg.Rect(self.x, self.y, self.radius, self.radius)

    def show(self):
        #pg.draw.rect(screen, (255,0,0), self.rect, 2)
        pg.draw.ellipse(screen, (0,0,255), self.ball_rect)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        self.ball_rect = pg.Rect(self.x, self.y, self.radius, self.radius)

    def off_screen(self):
        if self.ball_rect[1] > 480:
            return True

balls = []
for i in range(1000):
    balls.append(Ball(i*random.uniform(2, 5), 0, random.uniform(0.1, 0.2)))

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    screen.fill((0,0,0))

    for enum, ball in enumerate(balls):
        ball.show()
        ball.update()

        if ball.off_screen():
            balls.insert(enum, Ball(enum * random.uniform(2, 5), 0, random.uniform(0.1, 0.2)))
            balls.remove(ball)





    clock.tick(100)
    pg.display.update()