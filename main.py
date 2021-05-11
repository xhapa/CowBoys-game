import pygame
import os
import random
from obstacles_class import Obstacles
from player_class import Player

pygame.font.init()
pygame.display.set_caption("CowBoys")
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER_LIMIT = pygame.Rect(WIDTH//2-5, 0, 5, HEIGHT)
LEFT_OBSTACLES_LIMIT, RIGHT_OBSTACLES_LIMIT = HEIGHT/2 + 25, WIDTH/2 + 75
FPS = 60

HEALTH_FONT = pygame.font.SysFont('Corbel',40)
WINNER_FONT = pygame.font.SysFont('Corbel',100)

VEL = 4
OBSTACLES_VEL = 2
BULLET_VEL = 7
LIMIT_BULLETS = 2 
LIMIT_OBSTACLES = 5

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
OBSTACLE_TIME_EVENT = pygame.USEREVENT + 3

COWBOY_WIDTH = 60
COWBOY_HEIGHT = 50
OBSTACLE_WIDTH = 25
OBSTACLE_HEIGHT = 35

RED_COWBOY_IMAGE = pygame.image.load(os.path.join('Assets','red_cowboy.png'))
BLUE_COWBOY_IMAGE = pygame.image.load(os.path.join('Assets','blue_cowboy.png'))
CACTUS_IMAGE=pygame.image.load(os.path.join('Assets','cactus.png'))
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets','background.jpg'))
CACTUS=pygame.transform.scale(CACTUS_IMAGE,(OBSTACLE_WIDTH,OBSTACLE_HEIGHT))
RED_COWBOY = pygame.transform.scale(RED_COWBOY_IMAGE,(COWBOY_WIDTH,COWBOY_HEIGHT))
BLUE_COWBOY = pygame.transform.scale(BLUE_COWBOY_IMAGE,(COWBOY_WIDTH,COWBOY_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(WIDTH,HEIGHT)) 


def draw_screen(red, blue, obstacles):
    SCREEN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(SCREEN, (160,100,30), BORDER_LIMIT)
    SCREEN.blit(RED_COWBOY, (red.hit_box.x,red.hit_box.y))
    SCREEN.blit(BLUE_COWBOY, (blue.hit_box.x, blue.hit_box.y))

    red_health_text = HEALTH_FONT.render("Health: " + str(red.health), 1, (255,255,255))
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue.health), 1, (255,255,255))
    SCREEN.blit(blue_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    SCREEN.blit(red_health_text, (10, 10))

    for bullet in red.bullets:
        pygame.draw.rect(SCREEN, (255,0,0), bullet)

    for bullet in blue.bullets:
        pygame.draw.rect(SCREEN, (0,0,255), bullet)

    for obstacle in obstacles.obstacles:
        SCREEN.blit(CACTUS,(obstacle.x, obstacle.y))

    pygame.display.update()

def red_handle_movement(keys_pressed, red_player):
    if keys_pressed[pygame.K_w] and red_player.hit_box.y- VEL > 0: # UP
        red_player.hit_box.y-=VEL
    if keys_pressed[pygame.K_a] and red_player.hit_box.x - VEL > 0 : # LEFT
        red_player.hit_box.x-=VEL
    if keys_pressed[pygame.K_d] and red_player.hit_box.x + VEL + red_player.hit_box.width < LEFT_OBSTACLES_LIMIT: # RIGHT
        red_player.hit_box.x+=VEL
    if keys_pressed[pygame.K_s] and red_player.hit_box.y + VEL + red_player.hit_box.height < HEIGHT: # DOWN
        red_player.hit_box.y+=VEL

def blue_handle_movement(keys_pressed, blue_player):
    if keys_pressed[pygame.K_UP] and blue_player.hit_box.y- VEL > 0: # UP
        blue_player.hit_box.y-=VEL
    if keys_pressed[pygame.K_LEFT] and blue_player.hit_box.x - VEL > RIGHT_OBSTACLES_LIMIT: # LEFT
        blue_player.hit_box.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and blue_player.hit_box.x + VEL + blue_player.hit_box.width < WIDTH: # RIGHT
        blue_player.hit_box.x+=VEL
    if keys_pressed[pygame.K_DOWN] and blue_player.hit_box.y + VEL + blue_player.hit_box.height < HEIGHT: # DOWN
        blue_player.hit_box.y+=VEL

def draw_win(text):
    draw_winner_text = WINNER_FONT.render(text, 1,(255,255,255))
    SCREEN.blit(draw_winner_text, (WIDTH/2 -draw_winner_text.get_width()/2, HEIGHT/2 -draw_winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(6000)

def main():

    pygame.init()

    winner=""

    blue_player = Player(530, 200, COWBOY_WIDTH, COWBOY_HEIGHT,LIMIT_BULLETS, BULLET_VEL)
    red_player = Player(130, 200, COWBOY_WIDTH, COWBOY_HEIGHT, LIMIT_BULLETS, BULLET_VEL)
    
    obsta = Obstacles(LIMIT_OBSTACLES, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLES_VEL, LEFT_OBSTACLES_LIMIT, RIGHT_OBSTACLES_LIMIT,HEIGHT)

    clock = pygame.time.Clock()
    pygame.time.set_timer(OBSTACLE_TIME_EVENT, 800)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()        
        
            if event.type == pygame.KEYDOWN and pygame.time.get_ticks()>6000:
                red_player.create_bullets(event, pygame.K_q)
                blue_player.create_bullets(event, pygame.K_RCTRL,COWBOY_WIDTH)

            red_player.handle_health(event,RED_HIT)
            blue_player.handle_health(event,BLUE_HIT)

            obsta.create_obstacles(event,OBSTACLE_TIME_EVENT)

        if red_player.health <=0:
            winner = "Blue Wins!!"
        if blue_player.health <=0:
            winner = "Red Wins!!"
        if winner!="":
            draw_win(winner)
            break

        keys_pressed = pygame.key.get_pressed()            
        red_handle_movement(keys_pressed, red_player)
        blue_handle_movement(keys_pressed, blue_player)
        obsta.handle_obstacles_movement()

        red_player.handle_bullets_impact(blue_player,obsta,RED_HIT,BLUE_HIT,WIDTH)

        draw_screen(red_player, blue_player, obsta)
    
    main()           


if __name__=="__main__":
    main()