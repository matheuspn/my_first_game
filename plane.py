import pygame , random, math
from pygame import mixer
from data import cores 
from pygame.locals import *

def show_score (x, y) :
    score = font.render(f'Pontos : {score_value}', True, (cores.Preto))
    screen.blit(score, (x, y))

def show_life (x, y) :
    life = font.render(f'Vidas : ', True, (cores.Preto))
    screen.blit(life, (x, y))

def player(x, y) :
    screen.blit(image_player,(x, y))

def enemy(x, y, i) :
    screen.blit(image_enemy[i],(x, y))

def bullet(x, y, i) :
    global bullet_status
    bullet_status[i] = fire
    screen.blit(image_bullet[i] ,(x, y))

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y) :
    distance = math.sqrt((math.pow(enemy_x - bullet_x,2)) + (math.pow(enemy_y - bullet_y,2)))
    if distance < 10 :
        return True
    else :
        return False

def show_bullets(j) :
    screen.blit(image_bullet[j], (106 + (j * 30), screen_h - 25))

def show_image_life(i) : 
    screen.blit(image_life[i], (150 + (i * 50), life_text_y -5))

def show_game_over (x, y) :
    game_over = game_over_font.render('GAME\n OVER', True, (cores.Vermelho))
    screen.blit(game_over, (x, y))

def bullet_text():
    bullet_status_text = bullet_font.render('Balas : ', True, (cores.Preto)) 
    screen.blit(bullet_status_text, (5, screen_h - 20)) 

#iniciando o pygames
pygame.init()

# parâmetros da tela
screen_w = 800
screen_h = 400

# background
background = pygame.image.load('data/background1.jpg')
background = pygame.transform.scale(background, (screen_w, screen_h))

# background sound
mixer.music.load('data/background.wav')
mixer.music.play(-1)

# Player
image_player = pygame.image.load('data/warplane.png')
player_x = 0
player_y = (screen_h / 2) 
player_vel = 1.6
player_size = 50

# enemy
image_enemy = []
enemy_size = 32
enemy_x = []
enemy_y = []
num_of_enemies = 3 
enemy_vel = 1.3

for i in range(num_of_enemies):
    image_enemy.append(pygame.image.load('data/plane32_l.png'))
    enemy_x.append(random.randrange(screen_w, screen_w + 200))
    enemy_y.append(random.randrange(0, screen_h - enemy_size))


# bullet   
bullet_vel = 2
bullet_size = 24
num_of_bullets = 3
image_bullet = []
bullet_x = []
bullet_y = []
bullet_status = []
bullet_font = pygame.font.Font('data/techno_hideo.ttf', 24)
ready = 0
fire = 1

for i in range(num_of_bullets) :
    image_bullet.append(pygame.image.load('data/bullet.png')) 
    bullet_x.append(player_x + player_size)
    bullet_y.append(player_y + 20.5) 
    bullet_status.append(ready)  

# pontuação
score_value = 0
font = pygame.font.Font('data/techno_hideo.ttf', 32)
text_x = 10
text_y = 10

# vidas
image_life = []
life_value = 5
life_text_x = 10
life_text_y = 45

for i in range (life_value) :
    image_life.append(pygame.image.load('data/like.png'))

# Game over 
    game_over_font = pygame.font.Font('data/techno_hideo.ttf', 100)
    game_over_text_x = 70
    game_over_text_y = 100

# setando a tela
screen = pygame.display.set_mode((screen_w, screen_h))

# Titúlo e icon do programa 
pygame.display.set_caption('Avião!')
airplane = pygame.image.load('data/airplane.png')
pygame.display.set_icon(airplane)

clock = pygame.time.Clock()

# Game loop

while True :
    
    clock.tick(144)

    # background com imagem
    screen.blit(background, (0, 0))

    # puxando todos os eventos
    event = pygame.event.poll()

    # caso o evento QUIT seja requisitado
    if event.type == pygame.QUIT :
        break

    # puxando as keys
    keys = pygame.key.get_pressed()

    # movimentos do player
    if keys[pygame.K_RIGHT] and player_x < (screen_w - player_size) :
        player_x += player_vel 
    if keys[pygame.K_LEFT] and player_x > 0 :
        player_x -= player_vel 
    if keys[pygame.K_DOWN] and player_y < (screen_h - player_size) :
        player_y += player_vel 
    if keys[pygame.K_UP] and player_y > 0 :
        player_y -= player_vel 


    # inimigo
    for i in range(num_of_enemies): 

        if enemy_x[i] > 0 :
            enemy_x[i] -= enemy_vel

        if enemy_x[i] < 0 : 
            enemy_x[i] = screen_w
            enemy_y[i] = random.randrange(0, screen_h - enemy_size)
            life_value -= 1 

        if life_value == 0 :
            enemy_x[i] = screen_w * 2
            enemy_y[i] = screen_h * 2
            enemy_x[i] += enemy_vel
        
        enemy(enemy_x[i], enemy_y[i], i)

    # balas  
    bullet_text()

    for j in range(num_of_bullets) :

        if bullet_status[j] == ready :
            show_bullets(j)
           
        if bullet_x[j] > screen_w and not life_value == 0 :
            bullet_status[j] = ready

        if keys[pygame.K_SPACE] and bullet_status[j] == ready:
            bullet_sound = mixer.Sound('data/laser.wav')
            bullet_sound.play()
            bullet_x[j] = player_x + player_size
            bullet_y[j] = player_y + 20.5
            bullet(bullet_x[j], bullet_y[j], j)
                    
        if bullet_status[j] == fire :
            bullet(bullet_x[j], bullet_y[j], j)
            bullet_x[j] += bullet_vel 

        if life_value == 0 :
            bullet_status[j] = fire


    # colisão
    for i in range(num_of_enemies):
        for j in range(num_of_bullets): 
            
            colision = isCollision(enemy_x[i], enemy_y[i], bullet_x[j], bullet_y[j])

            if colision :
                colision_sound = mixer.Sound('data/explosion.wav')
                colision_sound.play()
                bullet_x[j] = player_x + player_size
                bullet_y[j] = player_y + 20.5
                bullet_status[j] = ready
                enemy_x[i] = screen_w
                enemy_y[i] = random.randrange(0, screen_h - enemy_size)
                score_value += 1

    for i in range(life_value) :
        show_image_life(i)

    if life_value == 0 :
        show_game_over(game_over_text_x, game_over_text_y)

    player(player_x, player_y)
    show_score(text_x, text_y)
    show_life(life_text_x, life_text_y)

    # atualizando a tela
    pygame.display.update()
