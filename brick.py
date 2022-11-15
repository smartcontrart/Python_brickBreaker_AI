import pygame
import os

class Brick:

    def __init__(self, x, y, life_points, length, width, imgs):
        self.x = x
        self.y = y
        self.life_points = life_points
        self.length = length
        self.width = width
        self.imgs = imgs
        self.img = imgs[self.life_points -1]
    
    def updateImage(self):
        self.img = self.imgs[self.life_points -1]

    def hit(self):
        self.life_points -= 1
        self.updateImage()

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)