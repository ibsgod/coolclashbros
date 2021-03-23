import pygame
import random
import Info


class Hero:
    def __init__(self, x, y, name, speed, jump, screen, player):
        self.x = x
        self.y = y
        self.name = name
        self.player = player
        self.screen = screen
        self.disp = None
        self.projectiles = []
        try:
            self.img = pygame.image.load(name.lower().replace(" ", "") + ".png")
        except:
            pass
        try:
            self.stunimg = pygame.image.load(name.lower().replace(" ", "") + "stun.png")
        except:
            pass
        try:
            self.blockimg = pygame.image.load(name.lower().replace(" ", "") + "block.png")
        except:
            pass
        try:
            self.atksnd = pygame.mixer.Sound(name.lower().replace(" ", "") + "atk.wav")
        except:
            pass
        try:
            self.atksnd2 = pygame.mixer.Sound(name.lower().replace(" ", "") + "atk2.wav")
        except:
            pass
        try:
            self.atkwoosh = pygame.mixer.Sound("fisty" + "atkwoosh.wav")
        except:
            pass
        try:
            self.runatkwoosh = pygame.mixer.Sound("fisty" + "runatkwoosh.wav")
        except:
            pass
        try:
            self.countersnd = pygame.mixer.Sound(name.lower().replace(" ", "") + "counter.wav")
        except:
            pass
        self.confuse = pygame.mixer.Sound("confuse.wav")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cx = self.x + self.width/2
        self.cy = self.y + self.height/2
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.xspd = 0
        self.yspd = 0
        self.accel = 1 if player == 0 else 2
        self.jumping = False
        self.flip = False
        self.walkStart = 0
        self.attackStart = -9999
        self.runattackStart = -9999
        self.jumpattackStart = -9999
        self.blockattackStart = -9999
        self.speed = speed
        self.jump = jump
        self.walkAnim = []
        self.attackAnim = []
        self.runattackAnim = []
        self.jumpattackAnim = []
        self.blockattackAnim = []
        self.hitx = 0
        self.hity = 0
        self.dmg = 0
        self.touchGround = None
        self.blocking = False
        self.blockinginp = False
        self.blockopp = None
        self.blockStart = 0
        self.blockTime = 0
        self.blockRegen = 0
        self.stunStart = -9999
        self.stun = False
        i = 1
        while True:
            fail = 0
            try:
                self.walkAnim.append(pygame.image.load(name.lower().replace(" ", "") + "walk" + format(i, "04") + ".png"))
            except:
                fail += 1
            try:
                self.attackAnim.append(pygame.image.load(name.lower().replace(" ", "") + "atk" + format(i, "04") + ".png"))
            except:
                fail += 1
            try:
                self.runattackAnim.append(pygame.image.load(name.lower().replace(" ", "") + "runatk" + format(i, "04") + ".png"))
            except:
                fail += 1
            try:
                self.jumpattackAnim.append(pygame.image.load(name.lower().replace(" ", "") + "jumpatk" + format(i, "04") + ".png"))
            except:
                fail += 1
            try:
                self.blockattackAnim.append(pygame.image.load(name.lower().replace(" ", "") + "blockatk" + format(i, "04") + ".png"))
            except:
                fail += 1
            if fail == 5:
                break
            i += 1

    def register(self, events):
        self.jumping = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_a:
                    self.left = True
                elif key == pygame.K_d:
                    self.right = True
                if key == pygame.K_w:
                    self.jumping = True
                if key == pygame.K_j:
                    self.blockinginp = True
                if key == pygame.K_k and pygame.time.get_ticks() - self.attackStart > 400 \
                        and pygame.time.get_ticks() - self.runattackStart > 600\
                        and pygame.time.get_ticks() - self.jumpattackStart > 400\
                        and pygame.time.get_ticks() - self.blockattackStart > 400:
                    if self.blocking:
                        self.blockattackStart = pygame.time.get_ticks()
                        self.runatkwoosh.play()
                    elif abs(self.xspd) < 5 and self.touchGround is not None:
                        self.attackStart = pygame.time.get_ticks()
                        self.atkwoosh.play()
                    elif abs(self.xspd) >= 5:
                        self.runattackStart = pygame.time.get_ticks()
                        self.runatkwoosh.play()
                    else:
                        self.yspd -= 5
                        self.jumpattackStart = pygame.time.get_ticks()
                        self.runatkwoosh.play()
                    self.stopBlocking()
            if event.type == pygame.KEYUP:
                key = event.key
                if key == pygame.K_a:
                    self.left = False
                elif key == pygame.K_d:
                    self.right = False
                if key == pygame.K_j:
                    self.stopBlocking()
                    self.blockinginp = False
                    self.blockopp = None

    def compute(self, rand):
        self.jumping = False
        self.left = False
        self.right = False
        if rand:
            max = 4
            r = random.randint(1, max)
            if r <= (max/2 if self.xspd < 0 else 1) and self.x - self.speed*3 - self.width> 200:
                self.left = True
            elif r > max/2 and r <= (max if self.xspd > 0 else max/2+1) and self.x + self.width + self.speed*3< 1000:
                self.right = True
            if random.randint(1, 100) == 1:
                self.jumping = True
            r = random.randint(1, 100)
            if r <= 2 and pygame.time.get_ticks() - self.attackStart > 400 \
                    and pygame.time.get_ticks() - self.runattackStart > 600\
                    and pygame.time.get_ticks() - self.jumpattackStart > 400:
                if r == 1:
                    self.blocking = True
                    self.blockStart = pygame.time.get_ticks()
                    pass
                if abs(self.xspd) < 5 and self.touchGround is not None:
                    self.attackStart = pygame.time.get_ticks()
                elif abs(self.xspd) >= 5:
                    self.runattackStart = pygame.time.get_ticks()
                else:
                    self.yspd -= 5
                    self.jumpattackStart = pygame.time.get_ticks()

        else:
            p = None
            for i in Info.heroes:
                if i is not self and (p == None or (self.cx - i.cx)**2 + (self.cy - i.cy)**2 < (self.cx - p.cx)**2 + (self.cy - p.cy)**2):
                    p = i
            if self.cx - 1 > p.cx and self.x - self.speed*3 - self.width> 300:
                self.left = True
            elif self.cx + 1 < p.cx and self.x + self.width < 1000:
                self.right = True
            if random.randint(1, 100) == 1:
                self.jumping = True
            if self.hitbox.colliderect(p.hitbox) and pygame.time.get_ticks() - self.attackStart > 400 \
                    and pygame.time.get_ticks() - self.runattackStart > 600\
                    and pygame.time.get_ticks() - self.jumpattackStart > 400:
                if abs(self.xspd) < 5 and self.touchGround is not None:
                    self.attackStart = pygame.time.get_ticks()
                    self.atkwoosh.play()
                elif abs(self.xspd) >= 5:
                    self.runattackStart = pygame.time.get_ticks()
                    self.runatkwoosh.play()
                else:
                    self.yspd -= 5
                    self.jumpattackStart = pygame.time.get_ticks()
                    self.runatkwoosh.play()

    def tick(self, events):
        if self.player == 0 and pygame.time.get_ticks() - self.stunStart > 3000:
            self.register(events)
        elif self.player == 2:
            self.compute(True)
        elif self.player == 3:
            self.compute(False)
            pass
        if pygame.time.get_ticks() - self.stunStart > 3000 and self.stun:
            self.stun = False
            Info.hpText[self] = pygame.font.SysFont("Microsoft Yahei UI Light", 35) \
                .render('{0:.3g}'.format(self.dmg) + "%", True,
                        (0 if pygame.time.get_ticks() - self.stunStart > 3000 else 255, 0, 0))
        if self.left:
            self.xspd = max(self.xspd-self.accel, -self.speed)
        if self.right:
            self.xspd = min(self.xspd+self.accel, self.speed)
        if self.left or self.right:
            self.stopBlocking()
            self.blockopp = None
        elif self.blockinginp and pygame.time.get_ticks() - self.attackStart > 400 \
                        and pygame.time.get_ticks() - self.runattackStart > 600 \
                        and pygame.time.get_ticks() - self.jumpattackStart > 400:
            if not self.blocking:
                self.blocking = True
                self.blockStart = pygame.time.get_ticks()
        self.touchGround = None
        for i in Info.grounds:
            if self.hitbox.colliderect(i.hitbox) and (self.touchGround is None or i.hitbox.y >= self.touchGround.hitbox.y):
                self.touchGround = i
        if self.touchGround is None:
            self.yspd += Info.gravity
        else:
            self.yspd = 0
            self.y = self.touchGround.hitbox.y - self.height + 1
        if self.jumping and self.touchGround:
            self.yspd = -self.jump
        self.checkAttacks()
        self.x += self.xspd + self.hitx
        self.y += self.yspd + self.hity
        if self.xspd != 0:
            self.xspd = self.xspd - self.xspd/abs(self.xspd)/2
        if self.hitx != 0:
            self.hitx = self.hitx - self.hitx/abs(self.hitx)/2
        if self.hity != 0:
            self.hity = self.hity - self.hity/abs(self.hity)/2
        self.cx = self.x
        self.cy = self.y + self.height / 2
        self.hitbox = pygame.Rect(self.cx - self.width / 2, self.cy - self.height / 2, self.width, self.height)
        if self.blockopp is not None and not self.hitbox.colliderect(self.blockopp.hitbox):
            self.blockopp = None
        if self.blocking and pygame.time.get_ticks() - self.blockStart + self.blockTime > 5000:
            self.stunStart = pygame.time.get_ticks()
            Info.hpText[self] = pygame.font.SysFont("Microsoft Yahei UI Light", 35).render(
                '{0:.3g}'.format(self.dmg) + "%", True, (0 if pygame.time.get_ticks() - self.stunStart > 3000 else 255, 0, 0))
            self.confuse.play()
            self.stun = True
            self.blockTime = 0
            self.left = False
            self.right = False
            self.blocking = False
            self.blockinginp = False
            self.attackStart = -9999
            self.jumpattackStart = -9999
            self.runattackStart = -9999
            self.blockattackStart = -9999
        if pygame.time.get_ticks() - self.stunStart > 3000 and not self.blocking and pygame.time.get_ticks() - self.blockRegen > 100:
            self.blockTime = max(self.blockTime - 50, 0)
            self.blockRegen = pygame.time.get_ticks()
        if self.touchGround is not None:
            self.y = self.touchGround.y - self.height

    def checkAttacks(self):
        pass

    def draw(self):
        p = pygame.time.get_ticks()
        if self.right:
            if self.flip:
                self.walkStart = p
            if p - self.attackStart > 400 and p - self.runattackStart > 600\
                    and p - self.jumpattackStart > 400 \
                    and p - self.blockattackStart > 400:
                self.flip = False
        elif self.left:
            if not self.flip:
                self.walkStart = p
            if p - self.attackStart > 400 and p - self.runattackStart > 600\
                    and p - self.jumpattackStart > 400\
                    and p - self.blockattackStart > 400:
                self.flip = True
        if self.stun:
            self.disp = (pygame.transform.flip(self.stunimg, self.flip, False))
        elif p - self.attackStart < 400:
            self.disp = (pygame.transform.flip(self.attackAnim[int(
                (p - self.attackStart) / 400 * len(self.attackAnim))], self.flip, False))
        elif p - self.runattackStart < 600:
            self.disp = (pygame.transform.flip(self.runattackAnim[int(
                (p - self.runattackStart) / 600 * len(self.runattackAnim))], self.flip, False))
        elif p - self.jumpattackStart < 400:
            self.disp = (pygame.transform.flip(self.jumpattackAnim[int(
                (p - self.jumpattackStart) / 400 * len(self.jumpattackAnim))], self.flip, False))
        elif p - self.blockattackStart < 400:
            self.disp = (pygame.transform.flip(self.blockattackAnim[int(
                (p - self.blockattackStart) / 400 * len(self.blockattackAnim))], self.flip, False))
        elif self.blocking:
            self.disp = (pygame.transform.flip(self.blockimg, self.flip, False))
        elif self.xspd != 0 or self.left or self.right:
            self.disp = (pygame.transform.flip(self.walkAnim[int(
                (p - self.walkStart) / 400 * len(self.walkAnim)) % len(self.walkAnim)],
                                                   self.flip, False))
        else:
            self.disp = (pygame.transform.flip(self.img, self.flip, False))
        self.height = self.disp.get_height()
        self.width = self.disp.get_width()
        self.screen.blit(self.disp, (self.x - self.width/2, self.y))
        if self.player == 0:
            pygame.draw.circle(self.screen, (255, 0, 0), (self.cx, self.y - 50), 20)

    def takeHit(self, x, y, dmg, opp=None):
        if dmg == None:
            self.hity = y
            self.hitx = x
            return
        if y != 0:
            self.hity = int((y + self.dmg * y / abs(y) / (5 if self.blocking else 1)))
        if x != 0:
            self.hitx = int((x + self.dmg * x / abs(x) / (5 if self.blocking else 1)))
        self.xspd = 0
        self.yspd = 0
        self.dmg += dmg / (5 if self.blocking else 1)
        if self.blocking and opp is not None:
            self.blockopp = opp
        Info.hpText[self] = pygame.font.SysFont("Microsoft Yahei UI Light", 35)\
            .render('{0:.3g}'.format(self.dmg) + "%", True, (0 if pygame.time.get_ticks() - self.stunStart > 3000 else 255, 0, 0))

    def stopBlocking(self):
        if self.blocking:
            self.blocking = False
            self.blockTime += pygame.time.get_ticks() - self.blockStart
            self.blockStart = pygame.time.get_ticks()






