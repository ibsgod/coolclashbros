import pygame

import Info
from Hero import Hero
from Projectile import Projectile


class Swordy(Hero):
    def __init__(self, x, y, screen, player):
        super().__init__(x, y, "Swordy", 15, 20, screen, player)
        self.hit = []
        self.moved = False
        self.leftatkmove = False
        self.fired = True

    def checkAttacks(self):
        if pygame.time.get_ticks() - self.attackStart > 0 and pygame.time.get_ticks() - self.attackStart < 200 :
            self.takeHit(1.5 * (-1 if self.flip else 1), 0, None)
        if pygame.time.get_ticks() - self.runattackStart > 500 and not self.fired:
            self.fired = True
            self.projectiles.append(Projectile(self.x, self.y, 0 + 180 if self.flip else 0, self))
        elif pygame.time.get_ticks() - self.runattackStart < 500:
            self.fired = False
        if pygame.time.get_ticks() - self.attackStart < 400 and pygame.time.get_ticks() - self.attackStart > 200:
            for i in Info.heroes:
                if i is not self:
                    if i.hitbox.colliderect(self.hitbox):
                        if i not in self.hit:
                            if self.cx < i.x + i.width and not self.flip:
                                self.hit.append(i)
                                i.takeHit(4, 0, 0.3, self)
                                self.atksnd.play()
                            if self.cx >= i.x and self.flip and i not in self.hit:
                                self.hit.append(i)
                                i.takeHit(-4, 0, 0.3, self)
                                self.atksnd.play()
                    else:
                        if i in self.hit:
                            self.hit.remove(i)
        elif pygame.time.get_ticks() - self.runattackStart < 500 and pygame.time.get_ticks() - self.runattackStart > 150:
            for i in Info.heroes:
                if i is not self:
                    if i.hitbox.colliderect(self.hitbox):
                        if i not in self.hit:
                            if self.cx < i.cx and not self.flip:
                                self.hit.append(i)
                                i.takeHit(10, -5, 0.3, self)
                                self.atksnd2.play()
                            if self.cx >= i.cx and self.flip and i not in self.hit:
                                self.hit.append(i)
                                i.takeHit(-10, -5, 0.3, self)
                                self.atksnd2.play()
                    else:
                        if i in self.hit:
                            self.hit.remove(i)
        elif pygame.time.get_ticks() - self.jumpattackStart < 300 and pygame.time.get_ticks() - self.jumpattackStart > 100:
            for i in Info.heroes:
                if i is not self:
                    if i.hitbox.colliderect(self.hitbox):
                        if i not in self.hit:
                            i.takeHit(0, -10, 0.3, self)
                            self.hit.append(i)
                            self.atksnd2.play()
                    elif i in self.hit:
                        self.hit.remove(i)
        elif pygame.time.get_ticks() - self.blockattackStart < 400 and pygame.time.get_ticks() - self.jumpattackStart > 200:
            for i in Info.heroes:
                if i is not self:
                    if i.hitbox.colliderect(self.hitbox):
                        if i not in self.hit:
                            if self.blockopp == i:
                                i.takeHit(15 * (-1 if self.cx > i.cx else 1), 0, 1.5, self)
                                self.countersnd.play()
                            else:
                                i.takeHit(3 * (-1 if self.cx > i.cx else 1), 0, 0.2, self)
                                self.atksnd.play()
                            self.blockopp = None
                            self.hit.append(i)
                    elif i in self.hit:
                        self.hit.remove(i)
        else:
            self.hit.clear()


