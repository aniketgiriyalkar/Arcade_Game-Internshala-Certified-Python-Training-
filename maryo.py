"""
File:  maryo.py, bricks.png, cactus.png, cactus_bricks.png, dragon.png, end.png,
       fire.png, fire_bricks.png, fireball.png, mario_dies.wav, mario_theme.wav,
       maryo.png, start.png
Language: python3
Author: Aniket Giriyalkar

Description: The game Maryo has two characters, Mario and Dragon.
            1. Maryo will be controlled by the user and can only move in two
             directions,upwards and downwards.
            2. The game should also have the function of gravity i.e if no key
             is pressed,the player should move downwards automatically.
            3. The Dragon should emit flames at a fixed rate depending upon the
            level, and the user has to dodge the flames emitted.
            4. There should be 4 levels in the game. The level increases after
            every 250 points.
            5. There should be fire on the bottom of the screen and cactus on
            the top. The fire should rise by some height at every level,and the
            cactus should move down.
            6. If the user fails to dodge the flame or hits the fire or cactus,
            he will lose and the game will end.
            7. There should be a start screen, an end screen, and an option to
            escape the game.
            8. Current Score, Level and Top Score should be displayed on the
            screen. Score is incremented whenever user presses any key.

"""

# Import Modules

import pygame, random, sys
from pygame.locals import *
pygame.init()

# Intializing Global variables.

window_height=600 
window_width=1200

blue = (0,0,255)
black = (0,0,0)
white = (255, 255, 255)

fps = 25
level = 0
addnewflamerate = 20


# Defining the required function.

class dragon:
    """
    This class will contain the  required variables, __init__ function, a
    function to make the dragon move in vertical direction between the cactus
    and the flames and also a function to return the height of the function.

    """

    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 15
    
    def __init__(self):
        self.image = load_image('dragon.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.right = window_width
        self.imagerect.top = window_height/2

    def update(self):
        
        if self.imagerect.top < cactusrect.bottom:
            self.up = False
            self.down = True

        if self.imagerect.bottom > firerect.top:
            self.up = True
            self.down = False
            
        if self.down:
            self.imagerect.bottom += self.velocity

        if self.up:
            self.imagerect.top -= self.velocity

        Canvas.blit(self.image, self.imagerect)

    def return_height(self):

        h = self.imagerect.top
        return h


class flames:
    """
    This class will contain a variable to determine the speed of the flames in
    fps, and three functions i.e, __init__ function, one function will be to
    generate the flames from a height same as that of the dragon, and one to
    detect whether the flame has reached the end of the screen.

    """

    flamespeed = 20

    def __init__(self):
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 20, 20)

    def update(self):
            self.imagerect.left -= self.flamespeed

    def collision(self):
        if self.imagerect.left == 0:
            return True
        else:
            return False


class maryo:
    """
    This class will contain variables that will determine the movement of the
    player, player speed and the gravity speed. This class contains 2 functions,
    __init__ function and the one to update the position of the player. The
    position of the player should be updated if it is within the range of the
    movement i.e below the cactus and above the fire.

    """
    global moveup, movedown, gravity, cactusrect, firerect
    speed = 10
    downspeed = 20

    def __init__(self):
        self.image = load_image('maryo.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50,window_height/2)
        self.score = 0

    def update(self):
        
        if moveup and self.imagerect.top > cactusrect.bottom:
            self.imagerect.top -= self.speed
            self.score += 1
            
        if  movedown and self.imagerect.bottom < firerect.top :
            self.imagerect.bottom += self.downspeed
            self.score += 1
            
        if gravity and self.imagerect.bottom < firerect.top:
            self.imagerect.bottom += self.speed


def terminate():
    """
    Function to end the program
    """

    pygame.quit()
    sys.exit()


def waitforkey():
    """
    This function has a loop which waits for the user to start and terminates
    when the user exits the game.
    :return: returns if the program exits the game
    """
    # To wait for user to start.
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # To terminate if the user presses the escape key.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return


def flamehitsmario(playerrect, flames):
    """
    Function to check if flame has hit mario or not
    :param playerrect
    :param flames
    :return: boolean value
    """
    for f in flame_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False


def drawtext(text, font, surface, x, y):
    """
    Function to display text on the screen.
    """
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def check_level(score):
    """
    Function that returns the current level.
    :param score
    """
    global window_height, level, cactusrect, firerect
    if score in range(0,250):
        firerect.top = window_height - 50
        cactusrect.bottom = 50
        level = 1
    elif score in range(250, 500):
        firerect.top = window_height - 100
        cactusrect.bottom = 100
        level = 2
    elif score in range(500,750):
        level = 3
        firerect.top = window_height-150
        cactusrect.bottom = 150
    elif score in range(750,1000):
        level = 4
        firerect.top = window_height - 200
        cactusrect.bottom = 200


def load_image(imagename):
    """
    Function to load the images.
    :param imagename:
    """
    return pygame.image.load(imagename)

# End of functions, begin to start the main code.
mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('MARYO')

# Setting up font and sounds and images.
font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks.png')
firerect = fireimage.get_rect()

cactusimage = load_image('cactus_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('start.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('end.png')
endimagerect = startimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')

# Getting to the start screen.
drawtext('Mario', font, Canvas,(window_width/3), (window_height/3))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()

# Start for the main code.
topscore = 0
Dragon = dragon()

while True:

    flame_list = []
    player = maryo()
    moveup = movedown = gravity = False
    flameaddcounter = 0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)

    # The main game loop.
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                
                if event.key == K_UP:
                    movedown = False
                    moveup = True
                    gravity = False

                if event.key == K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False

            if event.type == KEYUP:

                if event.key == K_UP:
                    moveup = False
                    gravity = True
                if event.key == K_DOWN:
                    movedown = False
                    gravity = True
                    
                if event.key == K_ESCAPE:
                    terminate()

        flameaddcounter += 1
        check_level(player.score)
        
        if flameaddcounter == addnewflamerate:

            flameaddcounter = 0
            newflame = flames()
            flame_list.append(newflame)

        for f in flame_list:
            flames.update(f)

        for f in flame_list:
            if f.imagerect.left <= 0:
                flame_list.remove(f)

        player.update()
        Dragon.update()
        Canvas.fill(black)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)

        drawtext('Score : %s | Top score : %s | Level : %s'
                 %(player.score, topscore, level), scorefont, Canvas,
                 350, cactusrect.bottom + 10)
        
        for f in flame_list:
            Canvas.blit(f.surface, f.imagerect)

        if flamehitsmario(player.imagerect, flame_list):
            if player.score > topscore:
                topscore = player.score
            break
        
        if ((player.imagerect.top <= cactusrect.bottom) or
                (player.imagerect.bottom >= firerect.top)):
            if player.score > topscore:
                topscore = player.score
            break

        pygame.display.update()

        mainClock.tick(fps)
    
    pygame.mixer.music.stop()
    gameover.play()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()
