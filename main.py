import os
import sys
import random
import pygame
from pygame.locals import *

import const
import sprites

pygame.init()

# fonts
monospace_14 = pygame.font.SysFont(*const.monospace_14)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%s, %s' % (const.WINDOW_POSITION_X, const.WINDOW_POSITION_Y)

fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(const.WINDOW_SIZE)
pygame.display.set_caption('Pygame aim practice')

clock = pygame.time.Clock()
pygame.display.update()

points = 0
difficulty_input = 1

targets = pygame.sprite.Group()
lifes = pygame.sprite.Group()

time = const.TIME_UNIT
difficulty = const.DIFFICULTY_SCALE - difficulty_input
total_lifes_count = int(difficulty // 1.5)

lifes_count = total_lifes_count


def random_x():
    return random.randint(0, const.WINDOW_WIDTH)


def random_y():
    return random.randint(0, const.WINDOW_HEIGHT)


while True:
    screen.fill(const.WHITE)
    key_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            mouse_pos = pygame.mouse.get_pos()

            for target in targets:  # type: sprites.Target
                points += target.is_clicked(mouse_pos)
                lifes_count -= 1 - target.is_clicked(mouse_pos)

    time += const.TIME_UNIT

    if not time % difficulty:
        targets.add(
            sprites.Target(
                random_x(),
                random_y(),
                difficulty // 2,
                difficulty // 2
            )
        )

    points_text = monospace_14.render('Points: %d' % points, True, const.DARK_GREEN)
    screen.blit(points_text, (const.POINTS_TEXT_X, const.POINTS_TEXT_Y))

    total_lifes = [
        sprites.Life(life_number * 19, 0, 20, 20, life_number < lifes_count)
        for life_number in range(1, total_lifes_count)
    ]

    lifes.add(*total_lifes)
    lifes.update()
    lifes.draw(screen)

    targets.update()
    targets.draw(screen)

    pygame.display.flip()
    fpsClock.tick(fps)
