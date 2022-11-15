import pygame

class Pad:

    def __init__(self, x, y, length, width, img):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.img = img
        self.speed = 15

    def move_left(self):
        if self.x <= 0:
            pass
        else:
            self.x -= self.speed

    def move_right(self):
        if self.x >= 800 - self.length:
            pass
        else:
            self.x += self.speed

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)