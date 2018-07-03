#!/usr/bin/env python3

# CPSC 481-01 AI
# Game: Zombie Hoard v3

# Ryan hodgson
# Tyler McConnell
# Albin Vinoy

import sys
import pygame
import time
from MyPRNG import MyPRNG
from bullet import Bullet

# import Zombie class
from zombieClass import Zombie
# import Player class
from playerClass import Player
# import Base class
from baseClass import Base

# initialize pygame
pygame.init()

##################### CONSTANTS #####################

# set title
title = "Zombie Hoard"

FPS = 60

# colors
tan = 181, 136, 76
menuColor = 0, 77, 0 # zombieGreen
white = 255, 255, 255
lightGreen = 0, 255, 0
lightRed = 255, 0, 0
green = 0, 200, 0
red = 200, 0, 0
brown = 179, 89, 0

###################### GlOBALS ######################

# set width/height
size = width, height = 800, 600

# create the screen
screen = pygame.display.set_mode(size)
# create screen rectangle for setting borders around screen
screenRect = screen.get_rect()

# set window title
pygame.display.set_caption(title)

# create clock object
clock = pygame.time.Clock()

# create a Player object
player = Player("player_soldier.png", width * 0.45, height * 0.5)

# create a Base object
base = Base("base3.png", 0, height * 0.4)

# list that will hold 4 different possible start spots for the zombies
zombieStartSpot = [(500,10), (775,100), (775, 500), (500,550)]

# this will be used to keep track of ticks
tickCount = 0

# container for the zombies
zombieGroup = pygame.sprite.Group()

# container for the bullets
bulletGroup = pygame.sprite.Group()

#create instance of PRNG for generating random numbers
myGen = MyPRNG()

# score for keeping track of zombie kills
score = 0

# used for finding change in player's x, y coordinates
deltaX = 0
deltaY = 0

# tree defining waypoint association
tree = {
	'a': ['A', 'B'],
	'b': ['F'],
	'c': ['I'],
	'd': ['L', 'I'],
	'A': ['a'],
	'B': ['a', 'C'],
	'C': ['B', 'D'],
	'D': ['C', 'E'],
	'E': ['D', 'G', 'J'],
	'F': ['b', 'G'],
	'G': ['E', 'F', 'H'],
	'H': ['G', 'I'],
	'I': ['c', 's4', 'H'],
	'J': ['E', 'K'],
	'K': ['Z'],
	'L': ['d'],
	'Z': []
    }

def button(msg, xPos, yPos, width, height, activeColor, inactiveColor, action):
    # object for getting mouse position
    mouse = pygame.mouse.get_pos()

    # object for getting mouse click
    click = pygame.mouse.get_pressed()

    # if you hover over first button, turn active color, else turn inactive color
    if xPos + width > mouse[0] > xPos and yPos + height > mouse[1] > yPos:
        pygame.draw.rect(screen, activeColor, (xPos, yPos, width, height))
        if click[0] == 1:
            if action == "play":
                return True
            elif action == "continue":
                return True
            else:
                sys.exit()
    else:
        pygame.draw.rect(screen, inactiveColor, (xPos, yPos, width, height))

    # font object for buttons
    buttonFont = pygame.font.Font(pygame.font.get_default_font(), 20)

    # button text
    buttonTextSurface = buttonFont.render(msg, True, white)
    buttonTextRect = buttonTextSurface.get_rect()
    buttonTextRect.center = ((xPos+(width/2)), (yPos+(height/2)))
    screen.blit(buttonTextSurface, buttonTextRect)

def menu():
    print("In menu")
	### maybe make menu return value to main() ###
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # background color of menu
        screen.fill(menuColor)

        # object for text and textsize
        menuText = pygame.font.Font(pygame.font.get_default_font(), 64)

        # render the text on the screen
        menuTextSurface = menuText.render("Zombie Hoard", True, white)

        # create text utility object
        menuTextRect = menuTextSurface.get_rect()

        #center the text
        menuTextRect.center = ((width/2),(height/2))

        # draw images onto screen
        screen.blit(menuTextSurface, menuTextRect)

        # draw play and quit buttons, change colors when hovering
        action = button("Play", 350, 450, 100, 50, lightGreen, green, "play")
        button("Quit", 350, 515, 100, 50, lightRed, red, "quit")

        # if True, return to main()
        if action == True:
            return True

        # update screen
        pygame.display.update()
        clock.tick(FPS)

def pauseScreen():
	#debug step
	print("Pausing game..")

	# fill screen with backColor
	screen.fill(menuColor)

	#set the font as the same font on title screen
	font = pygame.font.Font(pygame.font.get_default_font(), 64)

	# render the text on the screen
	pauseTextSurface = font.render("PAUSED", True, white)

	# create text utility object
	pauseTextRect = pauseTextSurface.get_rect()

	#center the text
	pauseTextRect.center = ((width/2),(height/2))

	#draw text onto screen
	screen.blit(pauseTextSurface, pauseTextRect)

	while(1):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		# when continue is pressed, action set to True
		action = button("Continue", 350,375,100,50, lightGreen, green, "continue")
		button("Quit", 350,450,100,50, lightRed, red, "quit")

		# if true, return to gameLoop()
		if action == True:
			return

		pygame.display.update()
		clock.tick(FPS)

def gameOver():
	#debug step
	print("Game Over!")

	# fill screen with backColor
	screen.fill(menuColor)

	#set the font as the same font on title screen
	font = pygame.font.Font(pygame.font.get_default_font(), 64)

	# render the text on the screen
	gameOverTextSurface = font.render("Game Over", True, white)

	# create text utility object
	gameOverTextRect = gameOverTextSurface.get_rect()

	#center the text
	gameOverTextRect.center = ((width/2),(height/2))

	#draw text onto screen
	screen.blit(gameOverTextSurface, gameOverTextRect)

	while(1):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		clock.tick(FPS)

def generateZombies():
    #print("In generateZombies")
    global myGen
    global tree

    # coordinates for start spots
    start1 = (500, 30)
    start2 = (775,100)
    start3 = (775, 500)
    start4 = (500,550)

    # waypoints
    A = (650, 40)
    B = (330, 30)
    C = (330, 120)
    D = (410, 120)
    E = (410, 265)
    F = (620, 170)
    G = (590, 290)
    H = (610, 400)
    I = (610, 500)
    J = (300, 330)
    K = (300, 250)
    L = (300, 500)

    # goal coordinate
    GOAL = (1, 250)

    # use current time as seed
    seed = int(time.time() % 60) + 1

    # seed the PRNG instance
    myGen.setSeed(seed)

    # generate the pseudo random number in range 1 to 100
    prn = (myGen.next_prn() % 100) + 1

    if prn <= 25:
        path = breadthFirstSearch(tree, 'a', 'Z')
        #print("Zombie's path: ", path)
        coordinatesPath = []
        for item in path:
            if item == 'a':
                coordinatesPath.append(start1)
            elif item == 'b':
                coordinatesPath.append(start2)
            elif item == 'c':
                coordinatesPath.append(start3)
            elif item == 'd':
                coordinatesPath.append(start4)
            elif item == 'A':
                coordinatesPath.append(A)
            elif item == 'B':
                coordinatesPath.append(B)
            elif item == 'C':
                coordinatesPath.append(C)
            elif item == 'D':
                coordinatesPath.append(D)
            elif item == 'E':
                coordinatesPath.append(E)
            elif item == 'F':
                coordinatesPath.append(F)
            elif item == 'G':
                coordinatesPath.append(G)
            elif item == 'H':
                coordinatesPath.append(H)
            elif item == 'I':
                coordinatesPath.append(I)
            elif item == 'J':
                coordinatesPath.append(J)
            elif item == 'K':
                coordinatesPath.append(K)
            elif item == 'L':
                coordinatesPath.append(L)
            else:
                coordinatesPath.append(GOAL)
        # create new zombie at appropriate spawnpoint
        z = Zombie("zombieWithAxe.png", zombieStartSpot[0], GOAL ,coordinatesPath)
    elif prn > 25 and prn <= 50:
        path = breadthFirstSearch(tree, 'b', 'Z')
        #print("Zombie's path: ", path)
        coordinatesPath = []
        for item in path:
            if item == 'a':
                coordinatesPath.append(start1)
            elif item == 'b':
                coordinatesPath.append(start2)
            elif item == 'c':
                coordinatesPath.append(start3)
            elif item == 'd':
                coordinatesPath.append(start4)
            elif item == 'A':
                coordinatesPath.append(A)
            elif item == 'B':
                coordinatesPath.append(B)
            elif item == 'C':
                coordinatesPath.append(C)
            elif item == 'D':
                coordinatesPath.append(D)
            elif item == 'E':
                coordinatesPath.append(E)
            elif item == 'F':
                coordinatesPath.append(F)
            elif item == 'G':
                coordinatesPath.append(G)
            elif item == 'H':
                coordinatesPath.append(H)
            elif item == 'I':
                coordinatesPath.append(I)
            elif item == 'J':
                coordinatesPath.append(J)
            elif item == 'K':
                coordinatesPath.append(K)
            elif item == 'L':
                coordinatesPath.append(L)
            else:
                coordinatesPath.append(GOAL)
        z = Zombie("zombieWithAxe.png", zombieStartSpot[1], GOAL ,coordinatesPath)
    elif prn > 50 and prn <= 75:
        path = breadthFirstSearch(tree, 'c', 'Z')
        #print("Zombie's path: ", path)
        coordinatesPath = []
        for item in path:
            if item == 'a':
                coordinatesPath.append(start1)
            elif item == 'b':
                coordinatesPath.append(start2)
            elif item == 'c':
                coordinatesPath.append(start3)
            elif item == 'd':
                coordinatesPath.append(start4)
            elif item == 'A':
                coordinatesPath.append(A)
            elif item == 'B':
                coordinatesPath.append(B)
            elif item == 'C':
                coordinatesPath.append(C)
            elif item == 'D':
                coordinatesPath.append(D)
            elif item == 'E':
                coordinatesPath.append(E)
            elif item == 'F':
                coordinatesPath.append(F)
            elif item == 'G':
                coordinatesPath.append(G)
            elif item == 'H':
                coordinatesPath.append(H)
            elif item == 'I':
                coordinatesPath.append(I)
            elif item == 'J':
                coordinatesPath.append(J)
            elif item == 'K':
                coordinatesPath.append(K)
            elif item == 'L':
                coordinatesPath.append(L)
            else:
                coordinatesPath.append(GOAL)
        z = Zombie("zombieWithAxe.png", zombieStartSpot[2], GOAL ,coordinatesPath)
    else:
        path = breadthFirstSearch(tree, 'd', 'Z')
        #print("Zombie's path: ", path)
        coordinatesPath = []
        for item in path:
            if item == 'a':
                coordinatesPath.append(start1)
            elif item == 'b':
                coordinatesPath.append(start2)
            elif item == 'c':
                coordinatesPath.append(start3)
            elif item == 'd':
                coordinatesPath.append(start4)
            elif item == 'A':
                coordinatesPath.append(A)
            elif item == 'B':
                coordinatesPath.append(B)
            elif item == 'C':
                coordinatesPath.append(C)
            elif item == 'D':
                coordinatesPath.append(D)
            elif item == 'E':
                coordinatesPath.append(E)
            elif item == 'F':
                coordinatesPath.append(F)
            elif item == 'G':
                coordinatesPath.append(G)
            elif item == 'H':
                coordinatesPath.append(H)
            elif item == 'I':
                coordinatesPath.append(I)
            elif item == 'J':
                coordinatesPath.append(J)
            elif item == 'K':
                coordinatesPath.append(K)
            elif item == 'L':
                coordinatesPath.append(L)
            else:
                coordinatesPath.append(GOAL)
        z = Zombie("zombieWithAxe.png", zombieStartSpot[3], GOAL ,coordinatesPath)

    #print("coordinatesPath", coordinatesPath)
    # add zombie to zombieGroup
    zombieGroup.add(z)


def breadthFirstSearch(tree, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in tree.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def gameLoop():
    print("In game loop")
    global deltaX
    global deltaY
    global score
    global base
    global player
    global zombieStartSpot
    global waypointList
    global tickCount
    global zombieGroup
    global bulletGroup

    # load background song 'Farcry 3: Heat'
    pygame.mixer.music.load('Heat.mp3')
    # set volume of music
    pygame.mixer.music.set_volume(0.2)
    # play song repeatedly
    pygame.mixer.music.play(-1)

    # load background image
    background = pygame.image.load("background.png")
    # create the utility rectangle for background
    backgroundRect = background.get_rect()

    # create a font object
    scoreFont = pygame.font.SysFont("monospace", 16)

    while 1:
        # if exit button is pressed, close program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if direction keys pressed, change deltas so we can move!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    deltaX = -3
                if event.key == pygame.K_d:
                    deltaX = 3
                if event.key == pygame.K_w:
                    deltaY = -3
                if event.key == pygame.K_s:
                    deltaY = 3

            # if keyup for direction keys, reset deltas to 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    deltaX = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    deltaY = 0


            #check for pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pauseScreen()
                if event.key == pygame.K_RETURN:
                    player.shoot(bulletGroup)

        # use deltas to update where player rectangle should be drawn
        player.rect.x += deltaX
        player.rect.y += deltaY

        # create impassable border around the screen
        player.rect.clamp_ip(screenRect)

        # draw background
        screen.blit(background, backgroundRect)

        # draw base
        screen.blit(base.image, base.rect)

        # draw all bullets on screen
        for bullet in bulletGroup:
            screen.blit(bullet.image, bullet.rect)

        # draw player on screen
        screen.blit(player.image, player.rect)

        # draw all zombies onto screen
        for zombie in zombieGroup:
            screen.blit(zombie.image, zombie.rect)

        # render text on screen
        scoretext = scoreFont.render("Score: {0}".format(score),1,(0,0,0))

        # draw text onto screen
        screen.blit(scoretext, (5,10))

        # detect if collision occurs between player and a zombie
        playerCollision = pygame.sprite.spritecollide(player, zombieGroup, False)

        # detect if collision occurs between base and a zombie
        baseCollision = pygame.sprite.spritecollide(base, zombieGroup, False)

        # list for if bullet hits zombie; kill zombie
        hits = pygame.sprite.groupcollide(zombieGroup, bulletGroup, True, True)

        # if hit occurred, increment score
        if hits:
            score += 5

        # this is for firing directionally
        #for bullets in bulletGroup:
            #bullets.update()

        # if collision occurs, end game
        if playerCollision or baseCollision:
            gameOver()

        # move the zombies through path toward base
        for zombie in zombieGroup:
            zombie.move()

        # spawn new zombies
        if tickCount % 100 == 1:
            generateZombies()

        #print("tickCount", tickCount)
        tickCount += 1
        # update the screen
        pygame.display.update()
        clock.tick(FPS)

def main():
    print("In main")
    action = menu()

    # if True, proceed to gameLoop()
    if action == True:
        gameLoop()

if __name__ == "__main__":
	main()
