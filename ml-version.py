import pygame
import os
import random
import sys
import brain
import numpy as np
import copy

pygame.font.init()

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

font1 = "Courier"
arial = "Arial"

SCORE_FONT = pygame.font.SysFont(font1, 30, bold=True)
GEN_FONT = pygame.font.SysFont(arial, 70, bold=True)
FPS_FONT = pygame.font.SysFont(font1, 40, bold=False)

PINK = '#F38181'
YELLOW = '#FFFF00'
GREEN = '#EAFFD0'
BLUE = '#95E1D3'
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

FPS = 60

BIRD_W = 60
BIRD_H = BIRD_W / (17 / 12)

PIPE_W = 100
PIPE_H = PIPE_W / (16 / 60) + 20

BIRD_PNG = pygame.image.load(
    os.path.join('Assets', 'bird.png'))
PIPE_PNG = pygame.image.load(
    os.path.join('Assets', 'pipe_long.png'))

BIRD = pygame.transform.scale(BIRD_PNG, (BIRD_W, BIRD_H))
PIPE = pygame.transform.scale(PIPE_PNG, (PIPE_W, PIPE_H))
GRAVITY = 0.5

BIRD_SPEED = 3

BIG_NUM = 6_000

BIRD_X = WIDTH / 2 - 50

MR = 20
MUTATION_VARIATION = 0.5

PREV_BEST = 0

GEN_NUM = 1


class Bird:

    def __init__(self):
        self.dead = 0
        self.rect = pygame.Rect(BIRD_X, 200, BIRD_W, BIRD_H)
        self.acc = 0
        self.time = 0

    def fall(self):
        if self.dead:
            img = BIRD
            img.set_alpha(100)
            self.rect.x -= BIRD_SPEED
        else:
            self.acc += GRAVITY
            self.rect.y += self.acc
            angle = -self.acc * 1.5
            img = pygame.transform.rotate(
                pygame.transform.scale(BIRD_PNG, (BIRD_W, BIRD_H)), angle)

        WIN.blit(img, (self.rect.x, self.rect.y))

    def collide(self, *args):
        for elem in args:
            if self.rect.colliderect(elem):
                return 1


class Obstacle:

    def __init__(self, x):
        r = random.randint(-350, -50)
        h_ext = BIG_NUM + PIPE_H
        self.rect_top = pygame.Rect(x, r-BIG_NUM, PIPE_W, h_ext)
        self.rect_bottom = pygame.Rect(
            x, r + 200 + PIPE_H, PIPE_W, h_ext)

    def move(self):
        # pu = pygame.Surface((self.rect_top.width, self.rect_top.height))
        # pd = pygame.Surface((self.rect_bottom.width, self.rect_bottom.height))
        # WIN.blit(pu, (self.rect_top.x, self.rect_top.y))
        # WIN.blit(pd, (self.rect_bottom.x, self.rect_bottom.y))

        self.rect_top.x -= BIRD_SPEED
        self.rect_bottom.x -= BIRD_SPEED
        upside_pipe = pygame.transform.rotate(PIPE, 180)
        WIN.blit(upside_pipe, (self.rect_top.x, self.rect_top.y + BIG_NUM))
        WIN.blit(PIPE, (self.rect_bottom.x, self.rect_bottom.y))


class Score:
    def __init__(self):
        self.score = 0

    def draw_score(self):
        score_text = SCORE_FONT.render(f'Score: {self.score}', True, BLACK)
        WIN.blit(score_text, (0, 0))

    def add_score(self):
        self.score += 1


class Generation:
    def __init__(self):
        self.surf = GEN_FONT.render(f"Gen: {GEN_NUM}", True, WHITE)
        self.surf.set_alpha(150)

    def draw(self):
        WIN.blit(self.surf, (WIDTH/2 - 100, HEIGHT/2 - 100))

def main(next_flappy_w_b=None):
    global FPS

    def nextgen():
        global GEN_NUM

        def find_best():
            global PREV_BEST
            times = [flappies[i].time for i in range(num_flappies)]
            max_time = [max(times) for i in range(num_flappies)]

            if max_time[0] <= PREV_BEST:

                return num_flappies+1

            PREV_BEST = max_time[0]
            diff = [max_time[i] - times[i] for i in range(num_flappies)]

            max_diff = max(diff)

            if not max_diff < 50:
                return diff.index(0)

            else:
                ys = [flappies[i].rect.y - WIDTH /
                    2 for i in range(num_flappies)]
                miny = min(ys)

                return ys.index(miny)

        def change_w_b():

            w = wb_tuple[0].copy()
            b = wb_tuple[1].copy()

            for layer_idx in range(len(w)):
                for b_idx in range(len(b[layer_idx])):
                    if MR > np.random.randint(1, 101):
                        b[layer_idx][b_idx] += np.random.uniform(
                            -MUTATION_VARIATION, MUTATION_VARIATION)
                for neuron_idx in range(len(w[layer_idx])):
                    for weight_idx in range(len(w[layer_idx][neuron_idx])):
                        if MR > np.random.randint(1, 101):
                            w[layer_idx][neuron_idx][weight_idx] += np.random.uniform(
                                -MUTATION_VARIATION, MUTATION_VARIATION)

            return w, b

        start = 0
        max_idx = find_best()
        if max_idx > num_flappies:
            start = 1
            new_w_b = [copy.deepcopy(flappy_w_b[0])]
            max_idx = 0

        else:
            start = 0
            new_w_b = []

        wb_tuple = flappy_w_b[max_idx]
        for i in range(start, num_flappies):
            myw, myb = change_w_b()
            new_w_b.append(copy.deepcopy((myw, myb)))

        GEN_NUM += 1
        main(new_w_b)

    score = Score()
    pipes = [Obstacle(WIDTH + i*300) for i in range(3)]
    clock = pygame.time.Clock()


    c_idx = 0
    cp = pipes[c_idx]

    num_flappies = 150
    flappies = [Bird() for i in range(num_flappies)]

    inputs = [None for i in range(num_flappies)]

    if next_flappy_w_b is None:
        flappy_w_b = []
        for i in range(num_flappies):
            iw, ib = brain.init_params()
            flappy_w_b.append((iw, ib))
    else:
        flappy_w_b = next_flappy_w_b
    numdead = 0
    ref = 0

    genText = Generation()
    while 1:

        if numdead >= num_flappies:
            nextgen()

        for idx in range(num_flappies):
            # 1. dist from pipe
            # 2. pipe height
            # 3. flappy y coord

            dist2pipe = cp.rect_bottom.x + PIPE_W - flappies[idx].rect.x
            inputs[idx] = [dist2pipe, cp.rect_bottom.y, flappies[idx].rect.y]

        if cp.rect_top.x + PIPE_W <= flappies[ref].rect.x:
            score.add_score()
            c_idx += 1
            cp = pipes[c_idx]

        WIN.fill(BLUE)

        for idx in range(num_flappies):

            if not flappies[idx].dead:
                flappies[idx].time += 0.1
                a = brain.for_prop(
                    inputs[idx], flappy_w_b[idx][0], flappy_w_b[idx][1])

                choice = np.argmax(a[-1], 0)

                if choice:
                    flappies[idx].acc = -10

                if flappies[idx].collide(cp.rect_top, cp.rect_bottom):

                    flappies[idx].dead = 1
                    numdead += 1
                    if ref == idx:
                        for idk in range(num_flappies):
                            if not flappies[idk].dead:
                                ref = idk

            flappies[idx].fall()

        for elem in pipes:
            elem.move()

        if pipes[0].rect_top.x < -100:
            pipes.pop(0)
            pipes.append(Obstacle(WIDTH))
            c_idx -= 1
            cp = pipes[c_idx]

        score.draw_score()
        genText.draw()


        pygame.display.update()

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for elem in flappies:
                        elem.acc = -10

                if event.key == pygame.K_UP:
                    FPS *= 2
                if event.key == pygame.K_DOWN:
                    FPS /= 2


if __name__ == '__main__':
    main()
