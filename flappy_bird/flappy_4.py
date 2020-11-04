
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from random import randint

green = (35, 232, 61)
blue = (37,241,245)
black = (0,0,0)
grey = (9,105,16)
grey2 = (24,168,33)
grey3 = (220,220,220)
green2 = (161,255,167)
green3 = (87,255,98)
yellow = (246,255,0)
white = (255,255,255)
orange = (255,187,0)
brown = (143,71,0)
pygame.init()
pygame.font.init()

# initialize sounds
pygame.mixer.pre_init()
pygame.mixer.set_num_channels(1)
pygame.mixer.init()

font = pygame.font.SysFont(None, 75)
size = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

done = False

clock = pygame.time.Clock()

def obstacle(x_obstacle, obstacle_widht, y_obstacle, obstacle_hight):
    pygame.draw.rect(screen, green, [x_obstacle, y_obstacle, obstacle_widht, obstacle_hight])
    pygame.draw.rect(screen, green, [x_obstacle, y_obstacle+obstacle_hight+space_obst, obstacle_widht, obstacle_hight+500])
    pygame.draw.rect(screen, black, [x_obstacle+63, y_obstacle, 7, obstacle_hight])
    pygame.draw.rect(screen, grey, [x_obstacle+56, y_obstacle, 7, obstacle_hight])
    pygame.draw.rect(screen, grey2, [x_obstacle+49, y_obstacle, 7, obstacle_hight])
    pygame.draw.rect(screen, green2, [x_obstacle, y_obstacle, 7, obstacle_hight])
    pygame.draw.rect(screen, green3, [x_obstacle+7, y_obstacle, 7, obstacle_hight])

    pygame.draw.rect(screen, black, [x_obstacle+63, y_obstacle+obstacle_hight+space_obst, 7, obstacle_hight+500])
    pygame.draw.rect(screen, grey, [x_obstacle+56, y_obstacle+obstacle_hight+space_obst, 7, obstacle_hight+500])
    pygame.draw.rect(screen, grey2, [x_obstacle+49, y_obstacle+obstacle_hight+space_obst, 7, obstacle_hight+500])
    pygame.draw.rect(screen, green2, [x_obstacle, y_obstacle+obstacle_hight+space_obst, 7, obstacle_hight+500])
    pygame.draw.rect(screen, green3, [x_obstacle+7, y_obstacle+obstacle_hight+space_obst, 7, obstacle_hight+500])
    

def ball(x_bird, y_bird):
    pygame.draw.circle(screen, yellow, [x_bird, int(y_bird)], 20)
    pygame.draw.circle(screen, white, [int(x_bird+12), int(y_bird-12)], 10)
    pygame.draw.polygon(screen, orange, [(x_bird+12,y_bird+5),(x_bird+12,y_bird-5), (x_bird+25, y_bird)])
    pygame.draw.circle(screen, black, [int(x_bird+12), int(y_bird-12)], 1)
    pygame.draw.circle(screen,black,[int(x_bird-12), int(y_bird+10)], 11)
    pygame.draw.circle(screen, yellow,[int(x_bird-12), int(y_bird+10)], 10)

def gameover():
    font = pygame.font.SysFont(None, 75)
    text = font.render("Game over", True, black)
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

def Score(score):
    font = pygame.font.Font(None ,50)
    text = font.render(("Score: "+str(score)), True, black)
    screen.blit(text, [0, 0])


def cloud(clx, cly):
    pygame.draw.circle(screen, grey3, [int(clx),int(cly)],20)
    pygame.draw.circle(screen, grey3, [int(clx+15),int(cly-10)],20)
    pygame.draw.circle(screen, grey3, [int(clx+30),int(cly)],20)
    pygame.draw.circle(screen, grey3, [int(clx+15),int(cly+10)],20)


# draw all background clounds
def all_cloud():
    cloud(45,40)
    cloud(83, 482)
    cloud(383, 39)
    cloud(524, 23)
    cloud(467, 63)
    cloud(623, 424)
    cloud(330, 260)
    cloud(600, 150)
    cloud(150, 150)
    cloud(450, 400)


def Ground(ground):
    pygame.draw.rect(screen, brown, [0, ground, 700, 60])


x_bird = 350 # bird x location # it's location never changes - The screen that "moves"
y_bird = 250 # bird y location
size_ball = 20
x_speed = 0 # how fast it moves on x direction
y_speed = 0 # how fast it moves on y direction

flying_speed_up = -10 # to go up, y_bird goes towards 0
flying_speed_down = 5


ground = size[1] -5.5 # position of ground

x_obstacle = size[0] # where obstacle will start - edge of right 
y_obstacle = 0 # object ylocation start - top of screen
obstacle_widht = 70 # width of rectangle on x's
obstacle_hight = (randint(10,350) //10 ) *10 # height of rectangle on y_bird's # from top to a random position up to 350 - multiple of 10
space_obst = 150 # space between rectangle
obspeed = 10 # obstace moving on screen speed
score = 0
of_limit_obst = -80 # maximum that it can go over the screen

# load and play sound
jump_sound = pygame.mixer.Sound('jump_sound/jump_01.wav')

while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            quit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_speed = flying_speed_up
                
                # play the background game music
                vol = jump_sound.get_volume()
                jump_sound.set_volume(min(vol*1,0.25))
                jump_sound.play()
            
        else:
            y_speed = flying_speed_down
            

    screen.fill(blue)

    all_cloud()
    obstacle(x_obstacle, obstacle_widht, y_obstacle, obstacle_hight)
    ball(x_bird, y_bird)
    Score(score)
    
    x_obstacle -= obspeed
    y_bird += y_speed

    if y_bird+5 > ground:
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

pygame.quit()
