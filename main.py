import pygame  # importing pygame
from sys import exit
from pygame.time import Clock

pygame.init()  # initializing pygame

screen = pygame.display.set_mode((752, 600))  # creating a display surface
screen.fill('White')
pygame.display.set_caption("Runner")  # changing the display name
clock = pygame.time.Clock()  # this helps us to control the frame rate
# creating font
test_font = pygame.font.Font("font/Comica Boom.otf", 50)  # font type, font size

# color surface
# test_surface = pygame.Surface((100, 200))  # for plain color
# test_surface.fill('Red')  # fill the surface with the given color

# image surface
back_surface = pygame.image.load('image/xBJPpY.gif').convert()
ground_surface = pygame.image.load('image/ground1.png').convert_alpha()  # convert used to make the game run faster

# text surface
text_surface = test_font.render('Welcome', True, 'Black')  # text, AA(Anti-aliasing, color

# image surface
bug_surface = pygame.image.load("image/bug100.png").convert_alpha()
bug_x = 800
bug_rect = bug_surface.get_rect(topleft=(800, 410))

player_surf = pygame.image.load('image/pRun180.png').convert_alpha()

# creating rectangle
# player_rect = pygame.Rect()  # left,top,width,height
player_rect = player_surf.get_rect(bottomleft=(10, 500))  # create rectangle around the surface
# changing the rectangle position will change the player position
while True:
    # draw all elements here
    # update everything in the loop
    # event loop
    for event in pygame.event.get():  # this loop is used for closing the display surface
        if event.type == pygame.QUIT:  # Quit is the "X" button on the surface
            pygame.quit()  # this is the opposite of init()
            exit()  # this will stop the while loop

    screen.blit(back_surface, (0, 0))  # adding the surface to the display surface with given position
    screen.blit(ground_surface, (0, 450))
    screen.blit(text_surface, (300, 150))

    bug_rect.x -= 3

    if bug_rect.right <= 0:
        bug_rect.left = 800

    # bug_x -= 3
    # if bug_x == -100:
    #     bug_x = 800

    screen.blit(bug_surface, bug_rect)
    # player_rect.left += 1
    screen.blit(player_surf, player_rect)

    # collision check
    if player_rect.colliderect(bug_rect):
        print('collision')

    pygame.display.update()
    clock.tick(60)  # the loop will not run faster than 60
