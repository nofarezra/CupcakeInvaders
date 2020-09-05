import math
import pygame
import random
from pygame.locals import *
from pygame import mixer

# Initializing pyGame:
pygame.init()

# Creating the screen (frame):
screen = pygame.display.set_mode((800, 600))  # defining the size of the screen

# Background image:
background = pygame.image.load('background.png')

# Background sound defining:
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and icon defining:
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player:
playerImg = pygame.image.load('arcade.png')
# Initial location of the player:
playerX = 370
playerY = 500

# Enemies:
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5  # moves as fast as our spaceship
enemies = ['enemy.png', 'enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(enemies[i]))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Bullet:
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 20  # moves fast
bullet_state = "ready"
# "Ready" - You can't see the bullet on the screen
# "Fire" - The bullet is currently moving

# Score
score_value = 0
font = pygame.font.Font('font.ttf', 32)

# Defining the location of the score on the screen:
textX = 10
textY = 10

# Game Over font:
over_font = pygame.font.Font('Pixelmania.ttf', 38)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (175, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


running = True

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
        # if event.type == pygame.KEYUP:  # key was released
        #     if keys[K_LEFT] or keys[K_RIGHT]:
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        #         playerX_change = 0

    # Handle keystroke pressing:
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:  # move left
        playerX -= 5
    if keys[K_RIGHT]:  # move right
        playerX += 5
    if keys[K_SPACE]:  # shoot
        if bullet_state is "ready":
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.play()
            # Get the current x coordinate of the spaceship
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    # Handle boundaries of spaceship:
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement:
    for i in range(num_of_enemies):
        # Game Over handling:
        if enemyY[i] > 450:  # the enemy reached our spaceship
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # this way they will all disappear
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Handle collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
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

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
