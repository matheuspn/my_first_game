import pygame
import random 
from pygame import mixer

width = 1200
height = 200
FPS = 60

#cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


#iniciando pygame e criando a janela do jogo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
background_image = pygame.image.load('data/background.jpg').convert_alpha()
background = pygame.transform.scale(background_image, (width, height))
background_rect = background.get_rect()
pygame.display.set_caption('Avião!')
icon_img = pygame.image.load('data/warplane.png')
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()

# imagens do jogo
player_img = pygame.image.load('data/warplane.png').convert_alpha()
enemy_img = pygame.image.load('data/enemy_32.png').convert_alpha()
bullet_img = pygame.image.load('data/laser.png').convert_alpha()
life_img = pygame.image.load('data/vida.png').convert_alpha()

# Pontuação
score = 0
score_x = 10
score_y = 10

# Fontes
fonte_a = pygame.font.match_font('arial')

def new_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemys.add(enemy)

def draw_text(text, color, size, x, y, font_name):
    font = pygame.font.Font(font_name, size)
    text_screen = font.render(text, True, color)
    screen.blit(text_screen, (x, y))

def draw_life_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if player.life > 50 :
        life_color = green
    elif player.life < 50 and player.life > 30 :
        life_color = yellow
    else :
        life_color = red
    pygame.draw.rect(surf, life_color, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text("Atira!", white, 64, width / 2 - 75, height / 4 - 30, fonte_a)
    draw_text("Setas para mover e space para atirar.",  white, 22, width / 2 - 180, height / 2 + 10 , fonte_a)
    draw_text("Pressione uma tecla para iniciar.", white, 18, width / 2 - 132 , height * 3 / 4, fonte_a)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYUP:
            waiting = False

explosion_anim = []
for i in range(9) :
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(f'explosion/{filename}').convert_alpha()
    explosion_img = pygame.transform.scale(img, (40, 30))
    explosion_anim.append(explosion_img)

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
        self.life = 100
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()

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

        # atirar se espaço pressionado
        if keys[pygame.K_SPACE]:
            player.shoot()

        #não permitindo sair da tela
        if self.rect.top < 0 :
            self.rect.top = 0
        if self.rect.bottom > height :
            self.rect.bottom = height

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay :  
            self.last_shot = now
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
            if score > 50 :
                self.speedx -= 5
            elif score > 100 :    
                self.speedx -= 10
            elif score > 150 :
                self.speedx -= 15
            elif score > 200 :
                self.speedx -= 20
            elif score > 250 :
                self.speedx -= 25
            elif score > 300 :
                self.speedx -= 30                

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

class Explosion(pygame.sprite.Sprite) :
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()

    def update(self) :
        now = pygame.time.get_ticks() 
        if now - self.last_update > self.frame_rate :
            self.last_upadte = now
            self.frame += 1
            if self.frame == len(explosion_anim) :
                self.kill()
            else :
                center = self.rect.center 
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#Sprites
all_sprites = pygame.sprite.Group()
enemys = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_enemy()

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_enemy()
        score = 0

    #Controle de atualização da tela
    clock.tick(FPS)

    # puxando todos os eventos
    event = pygame.event.poll()

    # caso o evento QUIT seja requisitado
    if event.type == pygame.QUIT :
        break

    #atualização
    all_sprites.update()

    #checando colisão de bullets com os enemys
    hits = pygame.sprite.groupcollide(enemys, bullets, True, True)
    
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)              
        new_enemy()

    #checando colisão de player com os enemys
    hits = pygame.sprite.spritecollide(player, enemys, True, pygame.sprite.collide_circle)
    
    for hit in hits:
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl) 
        mixer.music.load('player_explosion/rumble1.ogg')
        mixer.music.set_volume(0.2)
        mixer.music.play()         
        new_enemy()  
        if player.life <= 20 :
            player.life -= 19
        else :
            player.life -= 20   
        if player.life <= 0 :
            game_over = True


    #desenhar / renderizar
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen) 

    draw_text(f'Pontos : {score}', white, 20, score_x, score_y, fonte_a)
    draw_life_bar(screen, 2 , height - 12, player.life)

    pygame.display.flip()

pygame.quit()
