#Game: Color chase

#description:in this game the player controls a character that must catch falling color blocks.
#each block has its own colors.
#charcter color changes periodically with quite reflex and strategic movement

#featues of game
#1.simple controls
#2.Dynamic gameplay.
#3.increasing difficulty and scoring system

import pygame #module for game building
import random #for generating random positions
import time #for game timing and color timing

#Initialixe pygame

pygame.init()

#screen dimensions

WIDTH,HEIGHT=800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("COLOR CHASE")

#colors for blocks

WHITE=(255,255,255) #default structure of color parameter
BLACK=(0,0,0)
COLORS=[(255,0,0),(0,255,0),(0,0,255),(255,0,0)]

#Game variables

player_size=50
player_pos=[WIDTH//2,HEIGHT-2*player_size]
block_size=50
block_pos=[random.randint(0,WIDTH-block_size),0] #cordinates for starting from top of screen
block_list=[block_pos]
speed=5
score=0

#timing and color change

start_time=time.time()
color_change_interval=3 #seconds
current_color=random.choice(COLORS)

#font for displaying score

font=pygame.font.SysFont("monospace",35) #ensured size of score and its capacity to fill the screen

#main game loop
game_over=False
clock=pygame.time.Clock()

def drop_blocks(block_list):
    delay=random.random()
    if len(block_list)<10 and delay<0.1:
        x_pos=random.randint(0,WIDTH-block_size)
        y_pos=0
        block_list.append([x_pos,y_pos])

def draw_blocks(block_list):
    for block_pos in block_list:
        pygame.draw.rect(screen,current_color,(block_pos[0],block_pos[1],block_size, block_size))

def update_block_position(block_list,score):
    for idx,block_pos in enumerate(block_list):
        if block_pos[1]>=0 and block_pos[1]<HEIGHT:
            block_pos[1]+=speed
        else:
            block_list.pop(idx)
            score+=1
    return score

def collision_chcek(block_list,player_pos):
    for block_pos in block_list:
        if detect_collision(block_pos,player_pos):
            return True
    return False

def detect_collision(player_pos,block_pos):
    p_x=player_pos[0]
    p_y=player_pos[1]

    b_x=block_pos[0]
    b_y=block_pos[1]

    if (b_x>=p_x and b_x<(p_x + player_size)) or (p_x>=b_x and p_x<(b_x + block_size)):
        if (b_y>=p_y and b_y<(p_y + player_size)) or (p_y>=b_y and p_y<(b_y + block_size)):
            return True
    return False

#game loop

while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0]>0:
        player_pos[0]-= player_size
    if keys[pygame.K_RIGHT] and player_pos[0]<WIDTH-player_size:
        player_pos[0]+=player_size

    screen.fill(BLACK)

    #drop new balls and update position

    drop_blocks(block_list)
    score=update_block_position(block_list,score)

    #draw blocks and player

    draw_blocks(block_list)
    pygame.draw.rect(screen,current_color,(player_pos[0],player_pos[1],player_size,player_size))

    #check for collisons

    if collision_chcek(block_list,player_pos):
        if block_pos[0]!=current_color:
            game_over=True

    #display scores

    text=font.render(f"Score:{score}",True,WHITE)
    screen.blit(text,(10,10))

    #change player and color periodically

    if time.time()-start_time>color_change_interval:
        start_time=time.time()
        current_color=random.choice(COLORS)

    pygame.display.update()

    clock.tick(30)

pygame.quit()


