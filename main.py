import pygame
import sys
import random
from pygame.locals import *
import os
pygame.init()
vec = pygame.math.Vector2

height = 600
width = 800
acc = 0.5
platacc=0.5
fric = -0.12
fps = 60

walkright=[pygame.image.load(r"Images/Right/R%s.png" %frame) for frame in range(1,10)]
walkleft=[pygame.image.load(r"Images/Left/L%s.png" %frame) for frame in range(1,10)]
stnd=pygame.image.load(r"Images/Standing.png")

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Platformer")

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        
        self.pos = vec((10,200))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.walkcount=0
        self.left=False
        self.right=False
        self.standing=True
    def move(self):
        self.acc = vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.left=True
            self.right=False
            self.standing=False
            self.acc.x = -acc
        elif pressed_keys[K_d]:
            self.left=False
            self.right=True
            self.standing=False
            self.acc.x = acc
        else:
            self.standing=True
            self.walkcount=0
            
        self.acc.x += self.vel.x * fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(p1, platforms, False)
        if p1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -20
    def draw(self,surf):
        x=self.rect.x-17
        y=self.rect.y-30
        if self.walkcount+1>=60:
            self.walkcount=0
        if not(self.standing):
            if self.left:
                screen.blit(walkleft[self.walkcount//7],(x,y))
                self.walkcount+=1
            elif self.right:
                screen.blit(walkright[self.walkcount//7],(x,y))
                self.walkcount+=1
        else:
            if self.right:
                screen.blit(walkright[0],(x,y))
            else:
                screen.blit(walkleft[0],(x,y))
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(100,200), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, width-10), random.randint(50, height -50)))
        self.pos=vec((self.rect.x,self.rect.y))
        self.vel=vec((0,0))
        self.acc=vec((0,0))
    def move(self):
        pass
class mover(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, width-10), random.randint(40, height-30)))
        self.pos=vec((self.rect.x,self.rect.y))
        self.vel=vec((0,0))
        self.acc=vec((0,0))
    def move(self):
        self.acc=vec((0.5,0))
        if self.rect.x > width:
            self.acc.x=-platacc
        if self.rect.x < 0:
            self.acc.x=platacc
        self.acc.x += self.vel.x * fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
def platgen():
    while len(platforms)<7:
        w=random.randrange(50,100)
        p=platform()
        p.rect.center=(random.randrange(0,width-w),random.randrange(-100,-50))
        platforms.add(p)
        all_sprites.add(p)
def reset():
    for p in platforms:
        p.kill()
    pt1 = platform()
    pt1.surf = pygame.Surface((width, 20))
    pt1.surf.fill((255,0,0))
    pt1.rect = pt1.surf.get_rect(center = (int(width/2), height - 10))
    platforms.add(pt1)
    all_sprites.add(pt1)
    for x in range(random.randint(5,6)):
        plat = platform()
        platforms.add(plat)
        all_sprites.add(plat)
    p1.pos=(100,300)
    

pt1 = platform()
pt1.surf = pygame.Surface((width, 20))
pt1.surf.fill((255,0,0))
pt1.rect = pt1.surf.get_rect(center = (int(width/2), height - 10))
m1=mover()
p1 = player()

all_sprites = pygame.sprite.Group()
all_sprites.add(pt1)
all_sprites.add(p1)

platforms = pygame.sprite.Group()
platforms.add(pt1)

# Code to generate the levels
for x in range(random.randint(5,6)):
    plat = platform()
    platforms.add(plat)
    all_sprites.add(plat)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                p1.jump()

    if p1.rect.top <= height / 3:
        p1.pos.y += abs(p1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(p1.vel.y)
            if plat.rect.top>=height:
                plat.kill()
    if p1.rect.top>height:
        reset()

    platgen()
    screen.fill((0,0,0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        entity.move()

        
    p1.update()
    p1.draw(screen)
    pygame.display.update()
    clock.tick(fps)

