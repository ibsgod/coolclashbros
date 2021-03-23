import math

import pygame

import Info


class Projectile:
    def __init__(self, x, y, angle, hero):
        self.x = x
        self.y = y
        self.angle = angle % 360
        self.hero = hero
        self.start = pygame.time.get_ticks()
        if hero.name == "Swordy":
            self.speed = 10
            self.img = pygame.image.load("slice.png")
            self.duration = 2000
        self.hit = []
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)


    def tick(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if pygame.time.get_ticks() > self.start + self.duration:
            self.hero.projectiles.remove(self)
        for i in Info.heroes:
            if i.hitbox.colliderect(self.hitbox) and i != self.hero and i not in self.hit:
                self.hit.append(i)
                i.takeHit(0, -10, 0.2)
                self.hero.atksnd.play()

    def draw(self):
        self.hero.screen.blit(pygame.transform.flip(self.img, self.angle > 90 and self.angle < 270, self.angle > 180), (self.x, self.y))
