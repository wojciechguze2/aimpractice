import pygame

import const


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(const.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.kill()

            return 1

        return 0


class Life(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colored):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(const.WHITE)
        self.image.set_colorkey(const.WHITE)

        pygame.draw.rect(self.image, const.WHITE, [0, 0, width, height])

        self.image = pygame.image.load(const.LIFE_FULL_IMAGE_PATH) if colored \
            else pygame.image.load(const.LIFE_EMPTY_IMAGE_PATH)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
