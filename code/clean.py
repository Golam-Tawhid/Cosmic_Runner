import pygame
from sys import exit
from random import randint

# global hscore

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    score_surf = test_font2.render(f'Score: {current_time}', True, "#3E001F")
    score_rect = score_surf.get_rect(topleft=(350, 10))
    pygame.draw.rect(screen, "#C147E9", score_rect)
    pygame.draw.rect(screen, '#645CBB', score_rect, 3)
    screen.blit(score_surf, score_rect)

    cur_score=score

    # if cur_score>hscore:
    #     hscore=cur_score
    hscore_surf = test_font2.render(f'Highest Score: {cur_score}', True, "#3E001F")
    hscore_rect = hscore_surf.get_rect(topleft=(15,10))
    pygame.draw.rect(screen, "#57C5B6", hscore_rect)
    pygame.draw.rect(screen, '#159895', hscore_rect, 3)
    screen.blit(hscore_surf, hscore_rect)

    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 587:
                screen.blit(bug_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True     

def player_animation():
    global player_surf, player_index

    if player_rect.bottom<580:
        player_surf= player_jump
    else:
        player_index += 0.12
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((1024, 680))
screen.fill('White')
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font("font/Comica Boom.otf", 50)
test_font2 = pygame.font.Font("font/Comica Boom.otf", 30)

game_active = False
start_time = 0
score = 0

back_surface = pygame.image.load('image/backG.jpg').convert()
ground_surface = pygame.image.load('image/gro.png').convert_alpha()

bug_surface = pygame.image.load("image/en1.png").convert_alpha()
fly_surface = pygame.image.load("image/fly_en1.png").convert_alpha()

obstacle_rect_list = []

player_walk1 = pygame.image.load("image/rn1.png").convert_alpha()
player_walk2 = pygame.image.load("image/rn2.png").convert_alpha() 
player_walk3 = pygame.image.load("image/rn3.png").convert_alpha()
player_walk4 = pygame.image.load("image/rn4.png").convert_alpha()
player_walk=[player_walk2, player_walk3, player_walk4, player_walk1]
player_index=0
player_jump= pygame.image.load("image/jp.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(200, 580))
player_gravity = 0

player_stand = pygame.image.load("image/gm.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center=(450, 300))

game_name = test_font.render('Vaag Bug', True, "#4E4FEB")
game_name_rect = game_name.get_rect(center=(450, 80))

game_msg = test_font.render("Press space to run", True, "#8BE8E5")
game_msg_rect = game_msg.get_rect(center=(450, 530))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 480:
                    player_gravity = -21
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(bug_surface.get_rect(bottomright=(randint(1000, 1200), 587)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(1000, 1200), 330)))

    if game_active:
        screen.blit(back_surface, (0, 0))
        screen.blit(ground_surface, (0, 520))

        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 580:
            player_rect.bottom = 580
        player_animation()
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        

        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill("#071952")
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.bottomleft = (200, 580)
        player_gravity = 0

        score_msg = test_font.render(f'Your Score: {score}', True, '#8696FE')
        score_msg_rect = score_msg.get_rect(center=(450, 530))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)
            
    pygame.display.update()
    clock.tick(60)
