import math
import pygame
import random
from pygame.locals import *
from pygame import mixer

# Initializing pyGame:
pygame.init()

# Creating the screen (frame):
screen = pygame.display.set_mode((800, 600))  # defining the size of the screen

# Background sound defining:
sound = pygame.mixer.Sound("assets/sounds/background-music.wav")
sound.set_volume(0.1)
sound.play(-1)

# Caption and icon defining:
pygame.display.set_caption("Cupcake Invaders")
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

# Explosion image and its initial location:
explosionImg = pygame.image.load('assets/images/boom.png')
collisionX = 0
collisionY = 500

# Points images:
onePntImg = pygame.image.load('assets/images/one.png')
twoPntsImg = pygame.image.load('assets/images/two.png')
threePntsImg = pygame.image.load('assets/images/three.png')
fourPntsImg =pygame.image.load('assets/images/four.png')
fivePntsImg = pygame.image.load('assets/images/five.png')

# Player's image and its initial location:
playerImg = pygame.image.load('assets/images/baker.png')
playerX = 370
playerY = 471

# Lettuce's image and its initial location and state:
lettuceImg = pygame.image.load('assets/images/lettuce.png')
lettuceY = 20
lettuceX_change = 0
lettuceY_change = 1
lettuce_state = "hidden"
# "Hidden" - You can't currently see the lettuce on the screen
# "Falling" - The lettuce is currently moving
lettuceFlag = False # indicates if the death was caused by a lettuce

# Cupcakes images and movement parameters initialization:
cupcakeImg = []
cupcakeX = []
cupcakeY = []
cupcakeX_change = []
cupcakeY_change = []
num_of_cupcakes = 5
cupcakes = ['assets/images/cupcake.png', 'assets/images/cupcake2.png', 'assets/images/cupcake3.png',
            'assets/images/cupcake4.png', 'assets/images/cupcake5.png']
for i in range(num_of_cupcakes):
    cupcakeImg.append(pygame.image.load(cupcakes[i]))
    cupcakeX.append(random.randint(0, 736))
    cupcakeY.append(random.randint(50, 150))
    cupcakeX_change.append(1.1)
    cupcakeY_change.append(40)

# Bullet's image and its initial location and state:
bulletImg = pygame.image.load('assets/images/open-mouth.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"
# "Ready" - You can't see the bullet on the screen
# "Fire" - The bullet is currently moving

# Bonus items images and initial location and state:
bonusY = 20
bonusX_change = 0
bonusY_change = 2
mixerImg = pygame.image.load('assets/images/mixer.png')
spatulaImg = pygame.image.load('assets/images/spatula.png')
ovenImg = pygame.image.load('assets/images/oven.png')
pinImg = pygame.image.load('assets/images/rolling_pin.png')
bonus_types_and_imgs = {0: [mixerImg, 4, fourPntsImg], 1: [spatulaImg, 2, twoPntsImg], 2: [ovenImg, 5, fivePntsImg], 3: [pinImg, 3, threePntsImg]}
bonus_state = "hidden"
# "Hidden" - no bonus is currently on the screen
# "Falling" - bonus is currently falling

# Score's font and location:
score_value = 0
font = pygame.font.Font('assets/fonts/font.ttf', 32)
textX = 10
textY = 10

# Game Over font:
over_font = pygame.font.Font('assets/fonts/Pixelmania.ttf', 38)


# Initializing different variables:
game_over = False
running = True
time_to_die = None
time_for_cupcake = None
time_for_bonus = None
bonus_type = None
counter=0

# Custom events:
BONUSEVENT = pygame.USEREVENT
LETTUCEEVENT = pygame.USEREVENT
# insert bonus custom event into the event queue, will be called every 4000 milliseconds
pygame.time.set_timer(BONUSEVENT, 4000)
# insert lettuce custom event into the event queue, will be called every 3000 milliseconds
pygame.time.set_timer(LETTUCEEVENT, 3000)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (175, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def cupcake(x, y, i):
    screen.blit(cupcakeImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 57, y + 15))


def fire_lettuce(x, y):
    global lettuce_state
    lettuce_state = "falling"
    screen.blit(lettuceImg, (x, y))


def is_collision(cupcakeX, cupcakeY, x, y, minimum_distance):
    distance = math.sqrt(math.pow(cupcakeX - x, 2) + (math.pow(cupcakeY - y, 2)))
    if distance < minimum_distance:
        return True
    return False


def give_bonus(x, y, bonus_type):
    global bonus_state
    bonus_state = "falling"
    screen.blit(bonus_types_and_imgs[bonus_type][0], (x, y))


# The game loop:
while running:
    # RGB = Red, Green, Blue (in order to implement colors on screen)
    screen.fill((177, 216, 255)) # RGB of azure color

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
        playerX -= 3
    if keys[K_RIGHT]:  # move right
        playerX += 3
    if keys[K_SPACE]:  # shoot
        if bullet_state is "ready":
            # Get the current x coordinate of the baker in order to prevent
            # the bullet from moving along with her as she moves:
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    # Handle boundaries of baker:
    if playerX <= 0:
        playerX = 0
    elif playerX >= 680:
        playerX = 680

    if not game_over:
        # Handle cupcakes movement:
        for i in range(num_of_cupcakes):
            # Handling collision of baker with cupcake:
            collision = is_collision(cupcakeX[i], cupcakeY[i], playerX, playerY, 30)
            if collision: # the cupcake reached our baker
                # save the collision location before changing it:
                collisionX = cupcakeX[i]
                collisionY = cupcakeY[i]
                # save the death time:
                time_to_die = pygame.time.get_ticks() + 2000  # 2 second delay
                noooSound = mixer.Sound("assets/sounds/nooo.wav")
                noooSound.play()
                game_over = True
                for j in range(num_of_cupcakes):
                    cupcakeY[j] = 2000  # this way all the cupcakes will disappear
                break

            # Handle cupcakes movement in case there wasn't collision:
            cupcakeX[i] += cupcakeX_change[i]
            if cupcakeX[i] <= 0:
                cupcakeX_change[i] = 1.1
                cupcakeY[i] += cupcakeY_change[i]
            elif cupcakeX[i] >= 736:
                cupcakeX_change[i] = -1.1
                cupcakeY[i] += cupcakeY_change[i]

            # Handle collision of bullet and cupcake:
            collision = is_collision(cupcakeX[i], cupcakeY[i], bulletX, bulletY, 55)
            if collision and bullet_state is "fire":
                # save the time the baker hit the cupcake:
                time_for_cupcake = pygame.time.get_ticks() + 300
                biteSound = mixer.Sound("assets/sounds/bite.wav")
                biteSound.play()
                score_value += 1
                # save the collision location:
                collisionX = bulletX
                collisionY = bulletY
                # set up bullet state for the next shooting:
                bulletY = 500 # this way it won't be seen
                bullet_state = "ready"
                # Getting a location for a new cupcake:
                cupcakeX[i] = random.randint(0, 736)
                cupcakeY[i] = random.randint(50, 150)
            cupcake(cupcakeX[i], cupcakeY[i], i)

        # Handle lettuce movement:
        if lettuceY >= 600:
            lettuceY = 0
            lettuce_state = "hidden"
        if lettuce_state is "falling":
            fire_lettuce(lettuceX, lettuceY)
            lettuceY += lettuceY_change
            # Handling collision of the baker with lettuce:
            collision = is_collision(lettuceX, lettuceY, playerX, playerY, 58)
            if collision:
                # save the death time:
                time_to_die = pygame.time.get_ticks() + 2000  # 2 seconds delay
                noooSound = mixer.Sound("assets/sounds/nooo.wav")
                noooSound.play()
                lettuceFlag = True
                lettuceY = 2000  # this way the lettuce will disappear
                game_over = True

        # Handle bonuses movement:
        if bonusY >= 600:
            bonusY = 0
            bonus_state = "hidden"
        if bonus_state is "falling":
            give_bonus(bonusX, bonusY, bonus_type)
            bonusY += bonusY_change
            # Picking bonus handling:
            collision = is_collision(bonusX, bonusY, playerX, playerY, 70)
            if collision:  # the baker picked a bonus
                # save the picking time:
                time_for_bonus = pygame.time.get_ticks() + 500
                yaySound = mixer.Sound("assets/sounds/yay.wav")
                yaySound.play()
                score_value += bonus_types_and_imgs[bonus_type][1]
                bonus_state = "hidden"

    # Handle bullet movement and shooting:
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    if time_to_die:
        if lettuceFlag:
            screen.blit(explosionImg, (playerX + 30, playerY - 30))
        else:
            screen.blit(explosionImg, (collisionX + 20, collisionY - 20))
        if pygame.time.get_ticks() >= time_to_die:
            time_to_die = None

    if time_for_cupcake:
        screen.blit(onePntImg, (collisionX + 30, collisionY - 30))
        if pygame.time.get_ticks() >= time_for_cupcake:
            time_for_cupcake = None

    if time_for_bonus and bonus_type is not None:
        screen.blit(bonus_types_and_imgs[bonus_type][2], (playerX + 40, playerY - 20))
        if pygame.time.get_ticks() >= time_for_bonus:
            time_for_bonus = None

    if game_over:
        game_over_text()

    show_score(textX, textY)
    pygame.display.update()
