import pygame
import os
import random

pygame.font.init()


WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

font1 = "Courier"

LOSER_FONT = pygame.font.SysFont(font1, 40, bold=True)
LOSER_FONT2 = pygame.font.SysFont(font1, 25, bold=True)
SCORE_FONT = pygame.font.SysFont(font1, 30, bold=True)

PINK = '#F38181'
YELLOW = '#FCE38A'
GREEN = '#EAFFD0'
BLUE = '#95E1D3'
BLACK = (0, 0, 0)

FPS = 60

BIRD_W = 60
BIRD_H = BIRD_W / (17 / 12)

PIPE_W = 100
PIPE_H = PIPE_W / (16 / 60) + 20

CLOUD_W = 50
CLOUD_H = CLOUD_W / (30 / 28)

BCLOUD_W = 100
BCLOUD_H = BCLOUD_W

BIRD_PNG = pygame.image.load(
    os.path.join('Assets', 'bird.png'))
PIPE_PNG = pygame.image.load(
    os.path.join('Assets', 'pipe_long.png'))
CLOUD_PNG = pygame.image.load(
    os.path.join('Assets', 'cloud.png'))
CLOUD_BACK_PNG = pygame.image.load(
    os.path.join('Assets', 'cloud2.png'))

BIRD = pygame.transform.scale(BIRD_PNG, (BIRD_W, BIRD_H))
PIPE = pygame.transform.scale(PIPE_PNG, (PIPE_W, PIPE_H))
CLOUD = pygame.transform.scale(CLOUD_PNG, (CLOUD_W, CLOUD_H))
CLOUD_BACK = pygame.transform.scale(CLOUD_BACK_PNG, (BCLOUD_W, BCLOUD_H))
GRAVITY = 0.5

BIRD_SPEED = 3
BCLOUD_SPEED = 1


class Bird:

    def __init__(self):
        self.rect = pygame.Rect(WIDTH / 2 - 50, 200, BIRD_W, BIRD_H)
        self.acc = 0
        self.angle = 0

    def fall(self):
        global BIRD
        BIRD = pygame.transform.rotate(
            pygame.transform.scale(BIRD_PNG, (BIRD_W, BIRD_H)), self.angle)
        self.rect.y += self.acc * 1
        WIN.blit(BIRD, (self.rect.x, self.rect.y))
        self.angle = -self.acc * 1.5

    def jump(self):
        self.acc = -10

    def collide(self, *args):
        for elem in args:
            if self.rect.colliderect(elem):
                return 1


class Obstacle:

    def __init__(self, space):
        r = random.randint(-350, -50)
        self.rect_top = pygame.Rect(WIDTH, r, PIPE_W, PIPE_H)
        self.rect_bottom = pygame.Rect(
            WIDTH, self.rect_top.y + PIPE_H + space, PIPE_W, PIPE_H)

    def move(self, speed):
        self.rect_top.x -= speed
        self.rect_bottom.x -= speed
        upside_pipe = pygame.transform.rotate(PIPE, 180)
        WIN.blit(upside_pipe, (self.rect_top.x, self.rect_top.y))
        WIN.blit(PIPE, (self.rect_bottom.x, self.rect_bottom.y))

    def check(self):
        if self.rect_top.x < -390:
            return 1


class Score:
    def __init__(self):
        self.score = 0

    def draw_score(self):
        score_text = SCORE_FONT.render(f'Score: {self.score}', True, PINK)
        WIN.blit(score_text, (0, 0))

    def add_score(self, rect_bird, rect_pipe):
        birdx = rect_bird.rect.x
        pipex = rect_pipe.rect_top.x

        if birdx == pipex:
            self.score += 1
            return 1


class Cloud:
    def __init__(self, x, y):
        r_angle = random.randint(0, 360)

        self.exists = 25
        self.x = x
        self.y = y
        self.alpha = 255

        self.img = pygame.transform.rotate(
            pygame.transform.scale(CLOUD_PNG, (CLOUD_W, CLOUD_H)), r_angle)

    def draw(self):

        self.img.set_alpha(self.alpha)
        if self.exists > 0:
            WIN.blit(self.img, (self.x-30, self.y))
        else:
            return 1
        self.exists -= 1
        self.alpha -= 10


class BackCloud:
    def __init__(self):

        rh = random.randint(0, HEIGHT * 3 / 4)
        self.rect = pygame.Rect(WIDTH + 50, rh, BCLOUD_W, BCLOUD_H)

    def move(self):

        if self.rect.x < - BCLOUD_W:
            return 1

        self.rect.x -= BCLOUD_SPEED
        WIN.blit(CLOUD_BACK, (self.rect.x, self.rect.y))


def main():

    def draw_lose():
        nonlocal lost
        with open(os.path.join('Assets', 'high_score.txt'), mode='r') as tf:
            high_score = int(tf.readline())

        if high_score < score.score:
            high_score = score.score
            with open(os.path.join('Assets', 'high_score.txt'), mode='w') as tf:
                tf.write(f'{high_score}')

        first_line_h = HEIGHT/2 - 100
        first_line_w = WIDTH / 2 - 100
        colour = BLACK
        lose_text = LOSER_FONT.render('LOSER', True, colour)
        WIN.blit(lose_text, (first_line_w, first_line_h))

        lose_text = LOSER_FONT.render(f'You got {score.score}', True, colour)
        WIN.blit(lose_text, (first_line_w - 50, first_line_h + 50))

        lose_text = LOSER_FONT.render(
            f'The high score is {high_score}', True, colour)
        WIN.blit(lose_text, (first_line_w - 150, first_line_h + 100))

        lose_text = LOSER_FONT2.render(
            f'[Mouse 1] to Exit', True, colour)
        WIN.blit(lose_text, (20, HEIGHT-50))

        lose_text = LOSER_FONT2.render(
                    f'[R] to Restart', True, colour)
        WIN.blit(lose_text, (WIDTH - 230, HEIGHT-50))

        lost = 1

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_r:
                    main()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()

    score = Score()
    flappy = Bird()
    pipes = []
    lost = 0
    run = 1
    clock = pygame.time.Clock()
    counter = 0
    clouds = []
    back_clouds = []
    space = 250
    speed = BIRD_SPEED
    while run:


        if not lost:

            if not 0 < flappy.rect.y < HEIGHT:
                in_bounds = 0
            else:
                in_bounds = 1

            r = random.randint(0, 100)
            if r < 50:
                
                if counter % 300 == 0:
                    back_clouds.append(BackCloud())

            flappy.acc += GRAVITY
            if counter % 150 == 0:
                
                pipes.append(Obstacle(space))
                if space > 150:
                    space -= 5

            WIN.fill(BLUE)

            for elem in back_clouds:
                if elem.move():
                    back_clouds.remove(elem)

            for elem in clouds:
                if elem.draw():
                    clouds.remove(elem)

            for elem in pipes:
                elem.move(speed)
                if elem.check():
                    pipes.remove(elem)

            flappy.fall()
            score.draw_score()
            for elem in pipes:
                if score.add_score(flappy, elem) and not in_bounds:
                    score.score -= 1
                    draw_lose()

            pygame.display.update()

            for elem in pipes:
                if flappy.collide(elem.rect_top, elem.rect_bottom):
                    draw_lose()

            counter += round(0.5*BIRD_SPEED, 1)
            
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and lost):
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not lost:
                    clouds.append(Cloud(flappy.rect.x, flappy.rect.y))
                    flappy.jump()

                if event.key == pygame.K_r and lost:
                    main()
        
    draw_lose()


if __name__ == '__main__':
    main()
