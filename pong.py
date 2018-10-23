import pygame as pg
import random


white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
pg.init()
clock = pg.time.Clock()
gameDisplay = pg.display.set_mode((600, 600))
width, height = gameDisplay.get_size()
pg.display.set_caption("Pong")
gameExit = False


class Paddle:
    def __init__(self, x, y, h, w=10):
        self.x = x
        self.y = y
        self.w = w
        self.score = 0
        self.y_speed = 0
        self.h = h
        self.multiplier = 1.2
        self.paddle_rect = pg.Rect(self.x, self.y, self.w, self.h)

    def show(self):
        pg.draw.rect(gameDisplay, white, self.paddle_rect)

    def update(self):
        if self.y + self.y_speed * self.multiplier <= 480 and self.y + self.y_speed * self.multiplier >= 20:
            self.y = self.y + self.y_speed * self.multiplier
        self.paddle_rect = pg.Rect(self.x, self.y, self.w, self.h)

    def dir(self, y):
        self.y_speed = y


class Ball:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.radius = rad
        self.x_speed = 0
        self.y_speed = 0
        self.multiplier = 1
        self.ball_rect = pg.Rect(self.x, self.y, self.radius, self.radius)

    def show(self):
        pg.draw.ellipse(gameDisplay, white, self.ball_rect)

    def start(self):
        self.x_speed = random.choice([-10, 10])
        self.y_speed = random.choice([-5, 5])

    def update(self):
        self.x = self.x + self.x_speed * self.multiplier
        self.y = self.y + self.y_speed * self.multiplier
        self.ball_rect = pg.Rect(self.x, self.y, self.radius, self.radius)

    def check_winner(self):
        if self.x < 0:
            return "Right Wins"
        elif self.x > 600:
            return "Left Wins"
        else:
            return ""

    def hit(self, user_paddles):
        top, right, bottom, left = user_paddles
        if self.ball_rect.colliderect(left.paddle_rect):
            self.x_speed = abs(self.x_speed)
            self.y_speed = self.y_speed
            self.multiplier += 0.1
            left.multiplier += 0.1
            left.score += 1

        elif self.ball_rect.colliderect(right.paddle_rect):
            self.x_speed = self.x_speed * -1
            self.y_speed = self.y_speed
            self.multiplier += 0.1
            right.multiplier += 0.1
            right.score += 1

        elif self.ball_rect.colliderect(top.paddle_rect):
            self.x_speed = self.x_speed
            self.y_speed = abs(self.y_speed)

        elif self.ball_rect.colliderect(bottom.paddle_rect):
            self.x_speed = self.x_speed
            self.y_speed = self.y_speed * -1


def draw_text(surf, text, size, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


paddles = [Paddle(0, 0, 10, 600),  # TOP
           Paddle(width - 10, height/2-50, 100),  # RIGHT
           Paddle(0, 590, 10, 600),  # DOWN
           Paddle(10, height/2-50, 100)]  # LEFT
myBall = Ball(width/2, height/2, 20)

frameCount = 0
while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True

        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                paddles[1].dir(-10)
            elif event.key == ord('w'):
                paddles[3].dir(-10)
            elif event.key == pg.K_DOWN:
                paddles[1].dir(10)
            elif event.key == ord('s'):
                paddles[3].dir(10)
            elif event.key == pg.K_SPACE:
                myBall.start()

        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                paddles[1].dir(0)
            elif event.key == ord('s') or event.key == ord('w'):
                paddles[3].dir(0)

    gameDisplay.fill(black)

    myBall.show()
    myBall.update()
    winner = myBall.check_winner()
    myBall.hit(paddles)

    for paddle in paddles:
        paddle.show()
        paddle.update()

    draw_text(gameDisplay, str("{}".format(paddles[3].score)), 50, 20, 520)
    draw_text(gameDisplay, str("{}".format(paddles[1].score)), 50, 580, 520)
    draw_text(gameDisplay, str("{}".format(winner)), 100, 300, 100)

    clock.tick(30)
    pg.display.update()
