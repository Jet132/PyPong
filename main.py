# Created by Jet
# Original Git Repo: https://github.com/Jet132/PyPong
# Do not remove this Credit
#=====================================================

import PyPong
import pygame
import keyboard


###Controls###
# Player 0: W, S
# Player 1: O, L

#Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

#Display settings
scaling = 2

#Game settings
(width, height) = (300,200)
player_size = 40
player_width = 5
ball_size = 10

#pygame init
screen = pygame.display.set_mode((width*scaling, height*scaling))
pygame.display.set_caption('PyPong')

#init PyPong
env = PyPong.PyPong(field_size=(width, height), player_size=player_size, ball_size=ball_size, player_speed=8, start_velocity=4)
states = env.reset()

clock = pygame.time.Clock()
terminal = False
while not terminal:
    #24 fps
    clock.tick(24)
    #window exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminal = True
    if terminal:
        break

    #get input
    action0 = PyPong.ACTION_NOTHING
    if keyboard.is_pressed('w'):
        action0 = PyPong.ACTION_UP
    elif keyboard.is_pressed('s'):
        action0 = PyPong.ACTION_DOWN

    action1 = PyPong.ACTION_NOTHING
    if keyboard.is_pressed('o'):
        action1 = PyPong.ACTION_UP
    elif keyboard.is_pressed('l'):
        action1 = PyPong.ACTION_DOWN

    #execute game
    states, rewards, terminal = env.execute(action0,action1)
    print(rewards)
    #get game state
    (player0,player1), ball, ball_v = env.getRawState()
    #print(env.getScores())

    ####DRAW GAME####
    screen.fill(WHITE)

    #ball
    pygame.draw.rect(screen, BLACK, [ball[0]*scaling, ball[1]*scaling, ball_size*scaling, ball_size*scaling])
    #players
    pygame.draw.rect(screen, BLACK, [0, player0*scaling, player_width, player_size*scaling])
    pygame.draw.rect(screen, BLACK, [width*scaling-player_width, player1*scaling, player_width, player_size*scaling])

    pygame.display.flip()

pygame.quit()