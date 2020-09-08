import math
import pygame
import random
from pygame.locals import *
from pygame import mixer

# Initializing pyGame:
pygame.init()

# Creating the screen (frame):
screen = pygame.display.set_mode((806, 600))  # defining the size of the screen

# Background image:
background = pygame.image.load('background.png')

# Background sound defining:
mixer.music.load("music.mp3")
mixer.music.play(-1)

# Caption and icon defining:
pygame.display.set_caption("Cupcake Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player:
playerImg = pygame.image.load('baker.png')
# Initial location of the player:
playerX = 370
playerY = 471

# Lettuce:
lettuceImg = pygame.image.load('lettuce.png')
lettuceY = 20
lettuceX_change = 0
lettuceY_change = 3
lettuce_state = "hidden"
# "Hidden" - You can't currently see the lettuce on the screen
# "Falling" - The lettuce is currently moving

# Enemies:
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5  # moves as fast as our baker
enemies = ['cupcake.png', 'cupcake2.png', 'cupcake3.png', 'cupcake4.png', 'cupcake5.png']
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(enemies[i]))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Bullet:
bulletImg = pygame.image.load('open-mouth.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 20  # moves fast
bullet_state = "ready"
# "Ready" - You can't see the bullet on the screen
# "Fire" - The bullet is currently moving

# Bonus items:
bonusY = 20
bonusX_change = 0
bonusY_change = 5
bonus_types_and_imgs = {0: ['mixer.png', 4], 1: ['spatula.png', 2], 2: ['oven.png', 5], 3: ['rolling_pin.png', 3]}
bonus_state = "hidden"
# "Hidden" - no bonus is currently on the screen
# "Falling" - bonus is currently falling

# Score
score_value = 0
font = pygame.font.Font('font.ttf', 32)

# Defining the location of the score on the screen:
textX = 10
textY = 10

# Game Over font:
over_font = pygame.font.Font('Pixelmania.ttf', 38)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (175, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 57, y + 15))


def fire_lettuce(x, y):
    global lettuce_state
    lettuce_state = "falling"
    screen.blit(lettuceImg, (x, y))


def is_collision(enemyX, enemyY, x, y, minimum_distance):
    distance = math.sqrt(math.pow(enemyX - x, 2) + (math.pow(enemyY - y, 2)))
    if distance < minimum_distance:
        return True
    return False


def give_bonus(x, y, bonus_type):
    global bonus_state
    bonus_state = "falling"
    screen.blit(pygame.image.load(bonus_types_and_imgs[bonus_type][0]), (x, y))


game_over = False
running = True

BONUSEVENT = pygame.USEREVENT
LETTUCEEVENT = pygame.USEREVENT

# insert bonus custom event into the event queue, will be called every 4000 milliseconds
pygame.time.set_timer(BONUSEVENT, 4000)
# insert lettuce custom event into the event queue, will be called every 3000 milliseconds
pygame.time.set_timer(LETTUCEEVENT, 3000)


# The game loop:
while running:
    # RGB = Red, Green, Blue (in order to implement colors on screen)
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # Handle quitting key:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == BONUSEVENT and not game_over:
            bonusX = random.randint(0, 736)
            bonusY = 0
            bonus_type = random.randint(0, 3)
            give_bonus(bonusX, bonusY, bonus_type)
        if event.type == LETTUCEEVENT and not game_over:
            lettuceX = random.randint(0, 736)
            fire_lettuce(lettuceX, lettuceY)

    # Handle keystroke pressing:
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:  # move left
        playerX -= 5
    if keys[K_RIGHT]:  # move right
        playerX += 5
    if keys[K_SPACE]:  # shoot
        if bullet_state is "ready":
            # Get the current x coordinate of the spaceship
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    # Handle boundaries of baker:
    if playerX <= 0:
        playerX = 0
    elif playerX >= 680:
        playerX = 680

    if not game_over:
        # Enemy movement:
        for i in range(num_of_enemies):
            # Game Over handling:
            if is_collision(enemyX[i], enemyY[i], playerX, playerY, 30): # the enemy reached our baker
                for j in range(num_of_enemies):
                    enemyY[j] = 2000  # this way they will all disappear
                game_over = True
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            # Handle collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY, 45)
            if collision:
                # biteSound = mixer.Sound("bite.wav")
                # biteSound.play()
                bulletY = 500
                bullet_state = "ready"
                score_value += 1
                # Getting a location for a new enemy:
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

    # Bullet movement:
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Lettuce movement:
    if not game_over:
        if lettuceY >= 600:
            lettuceY = 0
            lettuce_state = "hidden"

        if lettuce_state is "falling":
            fire_lettuce(lettuceX, lettuceY)
            lettuceY += lettuceY_change
            # Game Over handling:
            if is_collision(lettuceX, lettuceY, playerX, playerY, 58):  # the lettuce reached our baker
                # noooSound = mixer.Sound("nooo.wav")
                # noooSound.play()
                lettuceY = 2000  # this way the lettuce will disappear
                game_over = True

    # Bonus movement:
    if not game_over:
        if bonusY >= 600:
            bonusY = 0
            bonus_state = "hidden"

        if bonus_state is "falling":
            give_bonus(bonusX, bonusY, bonus_type)
            bonusY += bonusY_change
            # Picking bonus handling:
            if is_collision(bonusX, bonusY, playerX, playerY, 40):  # the baker picked the bonus
                # yaySound = mixer.Sound("yay.wav")
                # yaySound.play()
                bonus_state = "hidden"
                score_value += bonus_types_and_imgs[bonus_type][1]

    if game_over:
        game_over_text()

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
