import pygame

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((800, 600))
w, h = gameDisplay.get_size()
pygame.display.set_caption("GAME")
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
gameExit = False

score = 0
new_score = 0
bullets = 13


class Target:
    def __init__(self, speed, x, lwr):
        self.image = pygame.image.load('targ.jpeg')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.targetPos = self.image.get_rect()
        self.targetPos[0] = x
        self.lower = lwr
        self.hit = 0
        if lwr:
            self.targetPos[1] = 100
        gameDisplay.blit(self.image, self.targetPos)
        if lwr:
            self.speed = [speed, 0]
        else:
            self.speed = [-speed, 0]

    def move(self):
        gameDisplay.blit(self.image, self.targetPos)

        if self.targetPos[0] >= gameDisplay.get_size()[0] and self.lower == 1:
            self.targetPos[0] = 0

        elif self.targetPos[0] < -75:
            self.targetPos[0] = 800

        self.targetPos.move_ip(self.speed)

    def is_hit(self, pos):
        if self.hit == 0 and self.targetPos.collidepoint(pos):
            self.hit = 1
            self.image.fill(white)
            return 1
        return 0


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


targets = []
for i in range(12):
    lower = i % 2
    spd = 4
    if lower:
        spd = 6
    targ = Target(spd, i * 75, lower)
    targets.append(targ)


while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            scores = 0
            if bullets > 0:
                for targ in targets:
                    scores += targ.is_hit(pygame.mouse.get_pos())
                bullets -= 1
            new_score += scores

    gameDisplay.fill(white)

    for targ in targets:
        targ.move()

    if new_score > score:
        score = new_score

    draw_text(gameDisplay, str("Score: {}".format(score)), 50, 400, 550)
    draw_text(gameDisplay, str("Bullets: {}".format(bullets)), 25, 45, 600-25)
    clock.tick(60)
    pygame.display.update()

