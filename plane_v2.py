# versão sem layout e sons, porém com classes/sprites.
import pygame
import random 
from pygame import mixer

width = 800
height = 400
FPS = 60

#cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/warplane.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = height / 2
        self.rect.left = 10
        self.speedx = 0
        self.speedy = 0

    def update(self) :
        self.speedx = 0
        self.speedy = 0

        keys = pygame.key.get_pressed()

        #setas direita e esquerda
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5

        #teclado 'a' e 'd'
        if keys[pygame.K_a]:
            self.speedx = -5
        if keys[pygame.K_d]:
            self.speedx = 5       
        
        self.rect.x += self.speedx

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0 :
            self.rect.left = 0

        #setas cima e baixo
        if keys[pygame.K_UP]:
            self.speedy = -5
        if keys[pygame.K_DOWN]:
            self.speedy = 5

        #teclado 'w' e 's'    
        if keys[pygame.K_w]:
            self.speedy = -5
        if keys[pygame.K_s]:
            self.speedy = 5
       
        self.rect.y += self.speedy

        #não permitindo sair da tela
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > height :
            self.rect.bottom = height

    def shoot(self):
        bullet = Bullet(self.rect.x + self.rect.width, self.rect.y + (self.rect.height/2) + 13)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/plane32_l.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(850, 1000)
        self.rect.y = random.randrange(height - self.rect.height)
        self.speedy = 0
        self.speedx = random.randrange(-6, -2)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0  :
            self.rect.x = random.randrange(850, 1000)
            self.rect.y = random.randrange(height - self.rect.height)
            self.speedy = 0
            self.speedx = random.randrange(-6, -2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # deleta a bala caso saia da tela
        if self.rect.left > width:
            self.kill()


#iniciando pygame e criando a janela do jogo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('data/background1.jpg')
background_rect = background.get_rect()
pygame.display.set_caption('Avião!')
icon_img = pygame.image.load('data/airplane.png')
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()

#Sprites
all_sprites = pygame.sprite.Group()
enemys = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemys.add(enemy)

#Game loop
running = True
while running :

    #Controle de atualização da tela
    clock.tick(FPS)

    # puxando todos os eventos
    event = pygame.event.poll()

    # caso o evento QUIT seja requisitado
    if event.type == pygame.QUIT :
        break
    
    # atirar se a tecla espaço seja pressionada
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            player.shoot()

    #atualização
    all_sprites.update()

    #checando colisão de bullets com os enemys
    hits = pygame.sprite.groupcollide(enemys, bullets, True, True)

    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemys.add(enemy)


    #checando colisão de player com os enemys
    hits = pygame.sprite.spritecollide(player, enemys, False)
    if hits:
        running = False


    #desenhar / renderizar
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen) 

    pygame.display.flip()

pygame.quit()
