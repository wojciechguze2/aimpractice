import os
import sys
import random
import pygame
from pygame.locals import *

import const
import sprites
import translations

pygame.init()

# fonts
monospace_14 = pygame.font.SysFont(*const.monospace_14)
monospace_25 = pygame.font.SysFont(*const.monospace_25)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%s, %s' % (const.WINDOW_POSITION_X, const.WINDOW_POSITION_Y)

fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(const.WINDOW_SIZE)
pygame.display.set_caption('Pygame aim practice')

clock = pygame.time.Clock()
pygame.display.update()

points = 0
targets = pygame.sprite.Group()
lives = pygame.sprite.Group()
time = const.TIME_UNIT
lives_count = const.LIVES_COUNT_INIT
game_started = False
input_level = 1
input_level_str = ''


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

        if game_started and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            mouse_pos = pygame.mouse.get_pos()

            for target in targets:  # type: sprites.Target
                points += target.is_clicked(mouse_pos)
                lives_count -= 1 - target.is_clicked(mouse_pos)

        if not game_started and event.type == pygame.KEYDOWN and len(input_level_str) < 3:
            try:
                input_level_str += str(int(event.unicode))
                input_level = int(input_level_str)

                if input_level > 100:
                    input_level_str = input_level_str[:-1]
                    input_level = int(input_level_str)

                    raise ValueError
            except ValueError:
                pass

        if not game_started and event.type == pygame.KEYDOWN and len(input_level_str) > 0:
            if event.key == pygame.K_BACKSPACE:
                input_level_str = input_level_str[:-1]

                try:
                    input_level = int(input_level_str)
                except ValueError:
                    input_level = 0
            elif event.key == pygame.K_RETURN:  # enter
                game_started = True

    if game_started:
        difficulty = const.DIFFICULTY_SCALE - input_level + 1
        total_lives_count = difficulty

        time += const.TIME_UNIT

        if time % difficulty == 0:
            targets.add(
                sprites.Target(
                    random_x(),
                    random_y(),
                    difficulty * 2,
                    difficulty * 2
                )
            )

        points_text = monospace_14.render(
            ('%s %d' % (translations.translate('points'), points)),
            True,
            const.DARK_GREEN
        )
        screen.blit(points_text, (const.POINTS_TEXT_X, const.POINTS_TEXT_Y))

        total_lives = [
            sprites.Life(
                life_number * 19 if life_number > 0 else 19,
                const.LIFE_POSITION_Y,
                const.LIFE_WIDTH,
                const.LIFE_WIDTH,
                life_number < lives_count
            )
            for life_number in range(total_lives_count)
        ]

        lives.add(*total_lives)
        lives.update()
        lives.draw(screen)

        targets.update()
        targets.draw(screen)

        if lives_count <= 0:
            print('%s %d' % (translations.translate('points'), points))
            exit()
    else:
        input_level_label = monospace_25.render(translations.translate('enter_level'), True, const.BLACK)
        screen.blit(input_level_label, (const.INPUT_LEVEL_LABEL_X, const.INPUT_LEVEL_LABEL_Y))

        input_level_text = monospace_14.render(input_level_str, True, const.BLACK)
        screen.blit(input_level_text, (const.INPUT_LEVEL_TEXT_X, const.INPUT_LEVEL_TEXT_Y))

    pygame.display.flip()
    fpsClock.tick(fps)
