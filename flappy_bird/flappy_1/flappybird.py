import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


import pygame,random
pygame.init()
pygame.mixer.pre_init()
pygame.mixer.set_num_channels(2)
pygame.font.init() # initialize font class in pygame
pygame.mixer.init()

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
orange = (255,187,0)

screen_width=600
screen_hight=476

screen=pygame.display.set_mode([screen_width,screen_hight])
pygame.display.set_caption('Flappy Bird')
folder_bird_images = "grumpy/"

bird_images=[pygame.image.load(folder_bird_images + str(i)+'.png') for i in range(1,5)]

clock=pygame.time.Clock()
vec=pygame.math.Vector2

background=pygame.image.load('background.png')

backroung_widht=background.get_width()

# a list of random blocks - [0] is the height of top and [1] the height of bottom - How long is the obstacle
# blist=[[40, 300], [50, 290], [60, 280], [70, 270], [80, 260], [90, 250], [100, 240], [110, 230], 
#       [120, 220], [130, 210], [140, 200], [150, 190], [160, 180], [170, 170], [180, 160], [190, 150],
#       [200, 140], [210, 130], [220, 120], [230, 110], [240, 100], [250, 90], [260, 80], [270, 70], 
#       [280, 60], [290, 50], [300, 40]]

blist = [[20, 280], [30, 270], [40, 260], [50, 250], [60, 240], [70, 230], [80, 220], [90, 210], [100, 200], 
         [110, 190], [120, 180], [130, 170], [140, 160], [150, 150], [160, 140], [170, 130], [180, 120],
         [190, 110], [200, 100], [210, 90], [220, 80], [230, 70], [240, 60], [250, 50], [260, 40], [270, 30], 
         [280, 20]]


class Bird(pygame.sprite.Sprite):
   def __init__(self):
      super().__init__()
      self.image=bird_images[0]
      self.image=pygame.transform.scale(self.image,(100,85))
      self.rect=self.image.get_rect()
      self.vel=vec(0,0)
      self.rect.center=(screen_width/2,screen_hight/2) # player starts in the middle of screen
      self.acc=vec(0,0)
      self.pos=vec(self.rect.center)
      self.frame_count = 0 # how many frames has passed - Use this to change img slow and fast enough for flying emotion 
      self.jump_sound = pygame.mixer.Sound('../jump_sound/flying.wav')

      self.speed = 4 # how fast the bird fly up/down

   def play_flying_sound(self):
      vol = self.jump_sound.get_volume()
      self.jump_sound.set_volume(min(vol*1,0.7))
      self.jump_sound.play()

   def update(self):
      self.acc=vec(0,self.speed)
      self.vel=vec(0,0)
      keys=pygame.key.get_pressed()
      # count frames to update image flying
      if keys[pygame.K_SPACE]:
         
         self.acc.y = self.speed * -1
         if self.frame_count+1<28:
            self.frame_count+=1
            self.image=bird_images[self.frame_count//7]
            self.image=pygame.transform.scale(self.image,(100,85))
            if self.frame_count//7 ==0:
               self.play_flying_sound()

         else:
            self.frame_count=0
      else:
         self.image=bird_images[0]
         self.image=pygame.transform.scale(self.image,(100,85))

      self.vel+=self.acc
      self.pos+=self.vel+0.5*self.acc # smoth new position

      # make sure it doesn't pass the borders
      if self.pos.y<=0+self.rect.width/2:
         self.pos.y=0+self.rect.width/2
      if self.pos.y>=screen_hight-self.rect.width/2:
         self.pos.y=screen_hight-self.rect.width/2

      self.rect.center=self.pos # update rect center for detection
      self.mask=pygame.mask.from_surface(self.image)


# super class for all walls - Top and bottom part(yes, they're different)
class WallsBasic(pygame.sprite.Sprite):
   def __init__(self,x,y,height, image_path):
      super().__init__()
      width = 80
      self.image=pygame.image.load(image_path)
      self.image=pygame.transform.scale(self.image,(width,height)) # transform image to sixe we want to
      self.rect=self.image.get_rect() # get it as rectangle
      if y>=0:
         self.rect.x,self.rect.y=x,y # x and y position of wall
      else:
         self.rect.x,self.rect.y=x,screen_hight-self.rect.height

      self.obst_speed = 6 # how fast the screen/obstacles moves

   def update(self):
      self.rect.x -= self.obst_speed
      self.mask=pygame.mask.from_surface(self.image) # this is used for perfect collision detection

class TopBlock(WallsBasic):
   def __init__(self,x,height):
      image_path =  'top_block.png'
      y = 0 # starts at top
      WallsBasic.__init__(self,x,y,height,image_path)
   
class BottomBlock(WallsBasic):
   def __init__(self,x,height):
      image_path =  'bottom_block.png'
      y = -1
      WallsBasic.__init__(self,x,y,height,image_path)



class Game:
   def __init__(self):
      self.bgx=0
      self.x=650
      self.height_top=170
      self.height_bottom=170
      self.score=0
      self.gover=0
      self.last=pygame.time.get_ticks()

   def blockgenerator(self): # from a list, choose randomly a block to insert on screen
      x=random.randint(620,650)
      height=random.choice(blist)
      height_top=height[0]
      height_bottom=height[1]
      self.topblock=TopBlock(x,height_top)
      self.tblocks=pygame.sprite.Group()
      self.tblocks.add(self.topblock)
      self.all_sprites.add(self.topblock)
      self.bottomblock=BottomBlock(x,height_bottom)
      self.bblocks=pygame.sprite.Group()
      self.bblocks.add(self.bottomblock)
      self.all_sprites.add(self.bottomblock)

   def new(self): # create a new game
      self.bird=Bird()

      self.all_sprites=pygame.sprite.Group() # this can make it easy for collision
      self.all_sprites.add(self.bird)

      self.topblock=TopBlock(self.x,self.height_top)

      self.tblocks=pygame.sprite.Group() # sprite for all top blocks
      self.tblocks.add(self.topblock)

      self.all_sprites.add(self.topblock) # also add to all sprites

      # do the same for bottom
      self.bottomblock=BottomBlock(self.x,self.height_bottom)
      self.bblocks=pygame.sprite.Group()
      self.bblocks.add(self.bottomblock)
      self.all_sprites.add(self.bottomblock)


      self.score=0
      self.gover=0

   def msg(self,text,x,y,color,size):
      self.font=pygame.font.SysFont('georgia',size,bold=1)
      msgtxt=self.font.render(text,1,color)
      msgrect=msgtxt.get_rect()
      msgrect.center=x/2,y/2
      screen.blit(msgtxt,(msgrect.center))

   def pause(self):
      wait=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
         self.msg("Paused",screen_width-100,screen_hight-100,blue,40)
         pygame.display.flip()

   def over(self):
      wait=1
      self.gover=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
         self.msg("Gameover",screen_width-150,screen_hight-100,red,40)
         self.msg("Press Enter to Play Again",screen_width-545,screen_hight+200,red,40)
         pygame.display.flip()
      self.new()

   def scores(self):
         self.msg("Score:"+str(self.score),screen_width-130,50,orange,50)
      
   def update(self):
     self.all_sprites.update()
     now=pygame.time.get_ticks()
     hits1=pygame.sprite.spritecollide(self.bird,self.bblocks,False,pygame.sprite.collide_mask)
     hits2=pygame.sprite.spritecollide(self.bird,self.tblocks,False,pygame.sprite.collide_mask)
     if hits1 or hits2:
        self.over()    

     relx=self.bgx%backroung_widht+5
     screen.blit(background,(relx-backroung_widht+3,0))
     if relx<screen_width:
        screen.blit(background,(relx,0))
     self.bgx-=2

     # if got block, add score
     if self.bottomblock.rect.x<screen_width/2 and self.topblock.rect.x<screen_width/2:
        self.blockgenerator() # add new one everytime you pass by a block
        self.score+=1

     else:
        self.score+=0
         
   def draw(self):
      self.all_sprites.draw(screen)
      self.scores()

   def event(self):
      for event in pygame.event.get():
         clock.tick(60)
         if event.type==pygame.QUIT:
            pygame.quit()
            quit()
         if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  self.pause()

   def run(self):
      while 1:
         self.event()
         self.update()
         self.draw()
         pygame.display.flip()


g=Game()
while g.run:
   back_sound = pygame.mixer.Sound('../background/background.wav')
   vol = back_sound.get_volume()
   back_sound.set_volume(min(vol*1,0.25))
   back_sound.play(-1)
   g.new()
   g.run()
