import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from random import randint

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

pygame.init()
pygame.font.init()

size = 700,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

done = False
clock = pygame.time.Clock()

def ball(x_bird,y_bird, size): # bird
    pygame.draw.circle(screen,black,[x_bird,y_bird], size)

def gameover(): # if game is over, then print and ask to play again
    font = pygame.font.SysFont(None, 75)
    text = font.render("Game over", True, red)
    screen.blit(text, [150, 100])

    font = pygame.font.SysFont(None, 25)
    text = font.render("Press Enter to start again", True, black)
    screen.blit(text, [150, 200])

    wait = 1 # to start a new game
    pygame.display.flip()
    while wait: # start a new game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    wait = 0 # to start a new game

# draw obstcle
def obstacle(x_obstacle, y_obstacle, obstacle_widht, obstacle_hight,space_obst):
                                   # left  top   width  height(up to 350)
    pygame.draw.rect(screen, green, [x_obstacle, y_obstacle, obstacle_widht, obstacle_hight]) # from top to middle

    # space + rect to bottom
    pygame.draw.rect(screen, green, [x_obstacle, int(y_obstacle+obstacle_hight+space_obst), obstacle_widht, obstacle_hight+500])


# print score on top left screen
def Score(score):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Score: "+str(score), True, black)
    screen.blit(text, [0,0])

x_bird = 350 # bird x location # it's location never changes - The screen that "moves"
y_bird = 250 # bird y location
size_ball = 20
x_speed = 0 # how fast it moves on x direction
y_speed = 0 # how fast it moves on y direction

flying_speed_up = -10 # to go up, y_bird goes towards 0
flying_speed_down = 5


ground = size[1] # position of ground

x_obstacle = size[0] # where obstacle will start - edge of right 
y_obstacle = 0 # object y_bird location start - top of screen
obstacle_widht = 70 # width of rectangle on x's
obstacle_hight = (randint(10,350) //10 ) *10 # height of rectangle on y_bird's # from top to a random position up to 350 - multiple of 10
space_obst = 150 # space between rectangle
obspeed = 10 # obstace moving on screen speed
score = 0
of_limit_obst = -80 # maximum that it can go over the screen

while not done: # loop over and over and print/display everyting every time
    for event in pygame.event.get(): #
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_speed = flying_speed_up
        else:
            y_speed = flying_speed_down
                

    screen.fill(white) # fill screen with a color
    obstacle(x_obstacle, y_obstacle, obstacle_widht, obstacle_hight,space_obst) # draw obstace
    ball(x_bird,y_bird, size_ball) # draw our bird
    Score(score) # draw our score
    
    y_bird += y_speed
    x_obstacle -= obspeed
    
    if y_bird > ground: # if touch the ground
        gameover()
        x_bird = 350
        y_bird = 250
        x_speed = 0
        y_speed = 0
        x_obstacle = 700
        y_obstacle = 0
        obstacle_widht = 70
        obstacle_hight = (randint(10,350) //10 ) *10 
        space_obst = 150
        obspeed = 10
        score = 0


        # if bird x_bird position is inside of rectangle range(in the space_obst between both rect)
        # and if bird y_bird is inside of y_bird's top obstacle
    if x_bird+size_ball > x_obstacle and x_bird-15 < obstacle_widht+x_obstacle and y_bird-size_ball//2 < obstacle_hight : # if touch top part of obstacle
        gameover()
        x_bird = 350
        y_bird = 250
        x_speed = 0
        y_speed = 0
        x_obstacle = 700
        y_obstacle = 0
        obstacle_widht = 70
        obstacle_hight = (randint(10,350) //10 ) *10 
        space_obst = 150
        obspeed = 10
        score = 0

         # if bird x_bird position is inside of rectangle range(in the space_obst between both rect)
         # and if bird y_bird is inside of y_bird's botton obstacle
    if x_bird+size_ball > x_obstacle and y_bird+size_ball > obstacle_hight+space_obst and x_bird-15 < obstacle_widht+x_obstacle: # if touch bottom part of obstacle
        gameover()
        x_bird = 350
        y_bird = 250
        x_speed = 0
        y_speed = 0
        x_obstacle = 700
        y_obstacle = 0
        obstacle_widht = 70
        obstacle_hight = (randint(10,350) //10 ) *10 
        space_obst = 150
        obspeed = 10
        score = 0

    if x_obstacle < of_limit_obst: # if obstance is gone(passed screen), then create a new one
        x_obstacle = 700
        obstacle_hight = (randint(10,350) //10 ) *10 

    if x_bird > x_obstacle and x_bird <= x_obstacle+obspeed:
        score = (score + 1)

    pygame.display.flip()
    clock.tick(60)


