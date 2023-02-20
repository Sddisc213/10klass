# Игра Shmup - 1 часть
# Cпрайт игрока и управление
import pygame
import random
from pygame import *

WIDTH = 1250
HEIGHT = 700
FPS = 60

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game!")
clock = pygame.time.Clock()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'),size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

    
#Создаем класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 40
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.speedx = -6
        if key[pygame.K_d]:
            self.speedx = 6
        if key[pygame.K_w]:
            self.speedy = -6
        if key[pygame.K_s]:
            self.speedy = 6
    
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

#Создаем класс врагов
class Mob (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = random.randrange(30,50)
        y = x
        self.image = pygame.Surface((x,y))
        self.image.fill((random.randrange(0,255),
                         random.randrange(0,255),
                         random.randrange(0,255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-8,8)
        self.speedy = random.randrange(1,8)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
        if self.rect.top > HEIGHT + 10:   
            self.rect.x = random.randrange(WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)
            self.speedx = random.randrange(-8,8)

#Создаем класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__ (self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill((random.randrange(125,255),
                         random.randrange(125,255),
                         random.randrange(125,255)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = -10

    def update (self):
        self.rect.y += self.speedy
        #убираем если долетела до верха
        if self.rect.bottom < 0:
            self.kill()
        
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
players = pygame.sprite.Group()

for i in range (0,20,1):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

player = Player()
players.add(player)
all_sprites.add(player)

score = 0
sh = 0

# Цикл игры
running = True
res = False

while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: running = False
            '''elif event.key == K_SPACE:
                player.shoot()'''
            
    sh += 1
    if sh == 15 and res == False :
        player.shoot()
        sh = 0
         

    # Обновление
    all_sprites.update()

    #Проверка на столкновение спрайтов игрока и моба
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        res = True

    #Проверка столкновения спрайта пули и моба
    rth = pygame.sprite.groupcollide(bullets, mobs, True, True)
    if rth:
        score += 1

    if len(players)<1:
        player = Player()
        players.add(player)
        all_sprites.add(player)

    if len(mobs)<20 and res == False:
        m = Mob()
        mobs.add(m)
        all_sprites.add(m)

    
    # Рендеринг
    if res == False:
        screen.fill((0,0,0))
        all_sprites.draw(screen)
        draw_text (screen, str(score), 100, WIDTH/2, 0)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        
    elif res == True:
        screen.fill((0,0,0))
        draw_text (screen, str(score), 100, WIDTH/2, 0)
        draw_text (screen, 'Вы погибли', 100, WIDTH/2, 100)
        pygame.display.flip()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_r:
                    res = False
        
pygame.quit()
