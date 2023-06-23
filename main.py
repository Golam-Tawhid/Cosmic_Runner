import pygame  # importing pygame
from sys import exit
from random import randint

from pyscreeze import center
# from pygame.time import Clock

def display_score():
    # global current_time
    current_time = int(pygame.time.get_ticks() / 1000) - star_time #converting it to readable value
    score_surf = test_font.render(f'Score:{current_time}', True, "#DB005B")
    score_rect = score_surf.get_rect(center = (376,100))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5

            screen.blit(bug_surface, obstacle_rect) # rectangle and surface on the same position
        return obstacle_list
    else:
        return []

pygame.init()  # initializing pygame

screen = pygame.display.set_mode((752, 600))  # creating a display surface
screen.fill('White')
pygame.display.set_caption("Runner")  # changing the display name
clock = pygame.time.Clock()  # this helps us to control the frame rate
# creating font
test_font = pygame.font.Font("font/Comica Boom.otf", 50)  # font type, font size

game_active = False

star_time = 0
score = 0
# color surface
# test_surface = pygame.Surface((100, 200))  # for plain color
# test_surface.fill('Red')  # fill the surface with the given color

# image surface
back_surface = pygame.image.load('image/xBJPpY.gif').convert()
ground_surface = pygame.image.load('image/ground1.png').convert_alpha()  # convert used to make the game run faster

# text surface
text_surface = test_font.render('Vaag Bug', True, '#080202')  # text, AA(Anti-aliasing), color
text_rect = text_surface.get_rect(center = (376, 40)) 
# image surface
# obstacles
bug_surface = pygame.image.load("image/bug100.png").convert_alpha()
bug_rect = bug_surface.get_rect(topleft=(800, 430))

obstacle_rect_list = []

player_surf = pygame.image.load("image/pooh.png").convert_alpha()
# creating rectangle
# player_rect = pygame.Rect()  # left,top,width,height
player_rect = player_surf.get_rect(bottomleft=(100, 500))  # create rectangle around the surface
# changing the rectangle position will change the player position
player_gravity = 0
#intro screen
player_stand= pygame.image.load("image/pooh2.gif").convert_alpha() #importing image
#scale 
# player_stand = pygame.transform.scale2x(player_stand) #updating the image. Returns new surface (overwrites the previous one)
#You can also use rotozoom instead of scale. But its more complex. Takes 3 args
player_stand = pygame.transform.rotozoom(player_stand,0,1)
#or
#player_stand = pygame.transform.scale(pygame.image.load("image/pooh2.gif").convert_alpha(), (200,400))
player_stand_rect = player_stand.get_rect(center=(376,300))

game_name= test_font.render('Vaag Bug', True, (111,196,169))
game_name_rect = game_name.get_rect(center=(376,80))

game_msg= test_font.render("Press space to run", True, (111,196,169))
game_msg_rect = game_msg.get_rect(center=(376, 530))

#Timer
obstacle_timer = pygame.USEREVENT + 1 #custom user event
pygame.time.set_timer(obstacle_timer, 1500) #trigger the event


while True:
    # draw all elements here
    # update everything in the loop
    # event loop
    
    for event in pygame.event.get():  # this loop is used for closing the display surface
        
        if event.type == pygame.QUIT:  # Quit is the "X" button on the surface
            pygame.quit()  # this is the opposite of init()
            exit()  # this will stop the while loop

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >=500:
                    player_gravity = -25

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >=500:
                    player_gravity = -25

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                bug_rect.left = 800
                star_time = int(pygame.time.get_ticks() / 1000)

        # if event.type == pygame.MOUSEMOTION: #to get mouse position
        #     if player_rect.collidepoint(event.pos):
        #         print('Collision')
        # pygame.MOUSEBUTTONUP / MOUSEBUTTONDOWN to check if mouse button pressed or released
        #triggering the timer
        if event.type== obstacle_timer and game_active:
            obstacle_rect_list.append(bug_surface.get_rect(topleft= (randint(1000,1200), 430)))



    if game_active:
        screen.blit(back_surface, (0, 0))  # adding the surface to the display surface with given position
        screen.blit(ground_surface, (0, 450))
        pygame.draw.rect(screen, "#99DBF5", text_rect)
        pygame.draw.rect(screen, 'Green', text_rect, 10)
        
        #drawing a line that follow mouse
        # pygame.draw.line(screen, 'Gold', (0,0), pygame.mouse.get_pos(),10)
        #drawing a circle
        # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100))  # left,top,width,eight
        screen.blit(text_surface, text_rect)

        score= display_score()

        # bug_rect.x -= 8 #we won't need this bc we created a user define event using timer.

        # if bug_rect.right <= 0:
        #     bug_rect.left = 800

        # # bug_x -= 3
        # # if bug_x == -100:
        # #     bug_x = 800
        # screen.blit(bug_surface, bug_rect)


        # player_rect.left += 1
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 500:
            player_rect.bottom = 500
        screen.blit(player_surf, player_rect)

        #obstacle movement
        obstacle_rect_list= obstacle_movement(obstacle_rect_list)
        """
        we first run the function (take rect list) and move every rect -5 left. then we get new list and overwrite previous one
        continuesly update list
        """

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('Jump')

        # collision check
        # if player_rect.colliderect(bug_rect):
        #     print('collision')

        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())

        if bug_rect.colliderect(player_rect):
            game_active=False
    else:
        screen.fill((94,129,162))
        # screen.blit(player_stand,player_stand_rect)
        screen.blit(player_stand,player_stand_rect)
        score_msg= test_font.render(f'Your Score: {score}', True, '#0C134F')
        score_msg_rect= score_msg.get_rect(center=(376,530))
        screen.blit(game_name, game_name_rect)

        if score==0: #if score is zero it will show intro
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)
    

    pygame.display.update()
    clock.tick(60)  # the loop will not run faster than 60
       