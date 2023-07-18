import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', True, "#DB005B")
    score_rect = score_surf.get_rect(center=(376, 100))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 500:
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

pygame.init()
screen = pygame.display.set_mode((752, 600))
screen.fill('White')
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font("font/Comica Boom.otf", 50)

game_active = False
start_time = 0
score = 0

back_surface = pygame.image.load('image/xBJPpY.gif').convert()
ground_surface = pygame.image.load('image/ground1.png').convert_alpha()

text_surface = test_font.render('Vaag Bug', True, '#080202')
text_rect = text_surface.get_rect(center=(376, 40))

bug_surface = pygame.image.load("image/bug50.png").convert_alpha()
fly_surface = pygame.image.load("image/fly50.png").convert_alpha()

obstacle_rect_list = []

player_surf = pygame.image.load("image/pooh2.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(100, 500))
player_gravity = 0

player_stand = pygame.image.load("image/pooh2.gif").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center=(376, 300))

game_name = test_font.render('Vaag Bug', True, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(376, 80))

game_msg = test_font.render("Press space to run", True, (111, 196, 169))
game_msg_rect = game_msg.get_rect(center=(376, 530))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 500:
                    player_gravity = -25
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(bug_surface.get_rect(bottomright=(randint(1000, 1200), 500)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(1000, 1200), 200)))

    if game_active:
        screen.blit(back_surface, (0, 0))
        screen.blit(ground_surface, (0, 450))
        # pygame.draw.rect(screen, "#99DBF5", text_rect)
        # pygame.draw.rect(screen, 'Green', text_rect, 10)
        
        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 500:
            player_rect.bottom = 500
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.bottomleft = (100, 500)
        player_gravity = 0

        score_msg = test_font.render(f'Your Score: {score}', True, '#0C134F')
        score_msg_rect = score_msg.get_rect(center=(376, 530))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)
            
    pygame.display.update()
    clock.tick(60)
