from random import randint
import pygame as pg
import time
from pygame import *

running = True
W = 400
H = 400
FPS = 30
Check = True    #переменная для движения противников
count = 0       #глобальный счетчик

UP = False  #состояние клавиш движения
DOWN = False
RIGHT = False
LEFT = False

clock = pg.time.Clock()

class Sprite(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

sc = pg.display.set_mode((W, H))    #установка разрешения игрового экрана

Player = Sprite(W/2,(H - H/3),(255,255,255))    #создание кораблика игрока

Enemy1 = Sprite(35, 35, (255,0,0))
Enemy2 = Sprite(145, 35, (255,0,0))
Enemy3 = Sprite(255, 35, (255,0,0))
Enemy4 = Sprite(365, 35, (255,0,0))
Enemy5 = Sprite(475, 35, (255,0,0))
Enemy6 = Sprite(585, 35, (255,0,0))

def Eny (Ey, count):
    if count % 100 == 0:
        Enemy1.rect.y = Ey
        Enemy2.rect.y = Ey
        Enemy3.rect.y = Ey
        Enemy4.rect.y = Ey
        Enemy5.rect.y = Ey
        Ey += 10
while running:
#время на один экран
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == KEYDOWN:           #Обработка нажатия кнопок
            if event.key == K_w: UP = True     #Клавиши движения
            if event.key == K_s: DOWN = True
            if event.key == K_a: LEFT = True
            if event.key == K_d: RIGHT = True

            if event.key == K_ESCAPE: running = False   #Клавиша ESC

        if event.type == KEYUP:             #Обработка отпускания клавиш
            if event.key == K_w: UP = False    #Клавиши движения
            if event.key == K_s: DOWN = False
            if event.key == K_a: LEFT = False
            if event.key == K_d: RIGHT = False
    

    sc.fill((0,0,0))
    sc.blit(Player.image, Player.rect) #поместить на экран объект
    sc.blit(Enemy1.image, Enemy1.rect)
    sc.blit(Enemy2.image, Enemy2.rect)
    sc.blit(Enemy3.image, Enemy3.rect)
    sc.blit(Enemy4.image, Enemy4.rect)
    sc.blit(Enemy5.image, Enemy5.rect)

    pg.display.update()
    pg.display.flip()

    if UP and Player.rect.y > H-H/3 : Player.rect.y -= 2   #Движение корабля игрока
    if DOWN and Player.rect.y < H - 55 : Player.rect.y += 2
    if LEFT and Player.rect.x > 0 : Player.rect.x -= 2
    if RIGHT and Player.rect.x < W - 50 : Player.rect.x += 2

    count+=1
    if count % 30 == 0:
        Check = not Check
    Eny(Enemy1.rect.y, count)
    if Check:
        Enemy1.rect.x -= 2
        Enemy2.rect.x -= 2
        Enemy3.rect.x -= 2
        Enemy4.rect.x -= 2
        Enemy5.rect.x -= 2
        
        #count += 1
    elif not Check:
        Enemy1.rect.x += 2
        Enemy2.rect.x += 2
        Enemy3.rect.x += 2
        Enemy4.rect.x += 2
        Enemy5.rect.x += 2
        #count += 1
    
    
    

pg.quit()
