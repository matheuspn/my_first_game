import pygame
import random 
from pygame import mixer

width = 1200
height = 400 
FPS = 60

#cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


#iniciando pygame e criando a janela do jogo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
background_image = pygame.image.load('data/background.jpg').convert_alpha()
background = pygame.transform.scale(background_image, (width, height))
background_rect = background.get_rect()
pygame.display.set_caption('Avião!')
icon_img = pygame.image.load('data/airplane.png')
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()

# imagens do jogo
player_img = pygame.image.load('data/warplane.png').convert_alpha()
enemy_img = pygame.image.load('data/enemy_32.png').convert_alpha()
bullet_img = pygame.image.load('data/laser.png').convert_alpha()
life_img = pygame.image.load('data/vida.png').convert_alpha()

# Pontuação
score = 0
score_x_y = (10 ,10)

# Vidas
lifes = 5
life_x_y = (10, height - 25)

# Fonte
font = pygame.font.Font('data/techno_hideo.ttf', 25)

def draw_text(text, color, x_y):
    text_screen = font.render(text, True, color)
    screen.blit(text_screen, x_y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 22
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)        
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
        bullet = Bullet(self.rect.x + self.rect.width, self.rect.y + (self.rect.height/2) + 5)
        mixer.music.load('data/laser.wav')
        mixer.music.set_volume(0.2)
        mixer.music.play()
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.radius = 13 
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius) 
        self.rect.x = random.randrange(width + 10, width + 100)
        self.rect.y = random.randrange(height - self.rect.height)
        self.speedy = 0
        self.speedx = random.randrange(-8, -3)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0  :
            self.rect.x = random.randrange(width + 10, width + 100)
            self.rect.y = random.randrange(height - self.rect.height)
            self.speedy = 0
            self.speedx = random.randrange(-8, -3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        # deleta a bala caso saia da tela
        if self.rect.left > width:
            self.kill()


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
        score += 1
        enemy = Enemy()
        all_sprites.add(enemy)
        enemys.add(enemy)


    #checando colisão de player com os enemys
    hits = pygame.sprite.spritecollide(player, enemys, True, pygame.sprite.collide_circle)
    
    if hits:
        lifes -= 1
        if lifes == 0 :
            running = False


    #desenhar / renderizar
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen) 

    draw_text(f'Pontos : {score}', white, score_x_y)
    draw_text(f'Vidas : ', white, life_x_y)
    
    for i in range(lifes) :
        screen.blit(life_img, (110 + (i * 40), height - 32))

    pygame.display.flip()

pygame.quit()
