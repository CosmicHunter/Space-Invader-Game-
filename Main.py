import pygame
import  random
import math
from pygame.locals import *

x = pygame.init()
print(x)
screen_width = 800
screen_height = 600
game_window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Invaders")
game_icon = pygame.image.load("ufo.png")
pygame.display.set_icon(game_icon)
fps = 30
game_clock = pygame.time.Clock()

#Score
game_score = 0
font = pygame.font.Font("freesansbold.ttf",32)
fx = 10
fy = 10

def displayGameScore(fx,fy):
    score_obj = font.render("Score :"+str(game_score),True,(255,255,255))
    game_window.blit(score_obj,(fx,fy))

# Game Over
gameOverfont    = pygame.font.Font("freesansbold.ttf",64)
def displayGameOver():
    obj = gameOverfont.render("Game Over ! ", True, (0, 255, 255))
    game_window.blit(obj, (200,250))


# Background
bckImg = pygame.image.load("bck3.jpg")


# Jupiter Details              # Reference from Lost in Space
jupiterImg = pygame.image.load("si2.png")
jupiter_x = 370
jupiter_y = 480
jupiter_dx = 0
jupiter_dy = 0
is_game_over = False

# Bots
botImg = []
botX = []
botY = []
botdx = []
botdy = []
no_of_bots = 5
for i in range(no_of_bots):
    botImg.append(pygame.image.load("monster.png"))
    botX.append(random.randint(0,736))
    botY.append(random.randint(0,180))
    botdx.append(4)
    botdy.append(30)

# Ballistics
bulletImg = pygame.image.load("bullet.png")
bulletY = 480
bulletX = 0
bulletdy = 16
is_bullet_fired = False
sounds_for_Game ={}
sounds_for_Game['exp'] = pygame.mixer.Sound("explosion.wav")
sounds_for_Game['laser'] = pygame.mixer.Sound("laser.wav")
sounds_for_Game['bck'] = pygame.mixer.Sound("background.wav")
sounds_for_Game['bck'].play(-1)   # -1 is for playing  the music on loop
# Explosion
eimg = pygame.image.load("explosion.png")

def initiate_space_bullet_protocol(x,y):
    global is_bullet_fired
    is_bullet_fired = True
    game_window.blit(bulletImg,(x+16,y+10))

def spaceship(x,y):
    game_window.blit(jupiterImg,(x,y))

def invaders(x,y,i):
    game_window.blit(botImg[i],(x,y))

def chkCollision(botX,botY,bulletX,bulletY):
     separation = math.sqrt(math.pow(botY-bulletY,2) + math.pow(botX - bulletX,2))
     if separation < 27:
         return True
     return False

while not is_game_over:
    game_window.fill((0,0,0))
    game_window.blit(bckImg, (0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_game_over = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT:
                    jupiter_dx = 10
                    print("Right key pressed")
            elif e.key == pygame.K_LEFT:
                    jupiter_dx = -10
                    print("Left key pressed")
            elif e.key == pygame.K_SPACE:
                if not is_bullet_fired :
                    bulletX = jupiter_x
                    initiate_space_bullet_protocol(bulletX,bulletY)
                    sounds_for_Game['laser'].play()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_RIGHT or e.key == pygame.K_LEFT:
                print("Key Released")
                jupiter_dx = 0
    jupiter_x += jupiter_dx
    if jupiter_x <=0:
        jupiter_x = 0
    elif jupiter_x > 800 - jupiterImg.get_width():
        jupiter_x = 800 - jupiterImg.get_width()

    for i in range(no_of_bots):

        if botY[i]>440:
            for j in range(no_of_bots):
                botY[j] = 1000
            displayGameOver()
            is_game_over = True
            break
        botX[i] += botdx[i]
        if botX[i] <= 0:
            botdx[i] = 4
            botY[i] += botdy[i]
        elif botX[i] > 800 - botImg[i].get_width():
            botdx[i] = -4
            botY[i] += botdy[i]

        is_enemy_hit = chkCollision(botX[i], botY[i], bulletX, bulletY)
        if is_enemy_hit:
            bulletY = 480
            is_bullet_fired = False
            sounds_for_Game['exp'].play()
            game_score += 10
            print(game_score)
            game_window.blit(eimg, (botX[i], botY[i]))
            botX[i] = random.randint(0, 736)
            botY[i] = random.randint(0, 180)

        invaders(botX[i], botY[i],i)

    # Reset the Ballistics
    if bulletY <=0 :
        is_bullet_fired = False
        bulletY = 480
    # Launch the bullet
    if is_bullet_fired:
        initiate_space_bullet_protocol(bulletX, bulletY)
        bulletY -= bulletdy

    spaceship(jupiter_x,jupiter_y)
    displayGameScore(fx,fy)
    pygame.display.update()
    game_clock.tick(fps)