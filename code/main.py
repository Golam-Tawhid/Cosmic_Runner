import pygame
from sys import exit
from random import randint

def display_score():
    # Calculate the current time in seconds
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    # Render and display the current score
    score_surf = font2.render(f'Score: {current_time}', True, "#3E001F")
    score_rect = score_surf.get_rect(topleft=(350, 10))
    pygame.draw.rect(screen, "#C147E9", score_rect) # Draw a colored rectangle behind the score
    pygame.draw.rect(screen, '#645CBB', score_rect, 3) # Draw a border around the score rectangle
    screen.blit(score_surf, score_rect)

    # Render and display the highest score
    hscore_surf = font2.render(f'Highest Score: {hi_score}', True, "#3E001F")
    hscore_rect = hscore_surf.get_rect(topleft=(15,10))
    pygame.draw.rect(screen, "#57C5B6", hscore_rect)
    pygame.draw.rect(screen, '#159895', hscore_rect, 3)
    screen.blit(hscore_surf, hscore_rect)

    return current_time

def obstacle_movement(obstacle_list):
    # Move obstacles and update the list of obstacles
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 587:
                screen.blit(enemy_surf, obstacle_rect) # Display ground enemy obstacle
            else:
                screen.blit(fly_surface, obstacle_rect) # Display flying enemy obstacle
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    # Check for collisions between the player and obstacles
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True     

def player_animation():
    global player_surf, player_index

    # Perform player animation based on the player's position
    if player_rect.bottom<580:
        player_surf= player_jump # Player is jumping
    else:
        player_index += 0.12
        if player_index >= len(player_run):
            player_index = 0
        player_surf = player_run[int(player_index)] # Player is running

pygame.init()
screen = pygame.display.set_mode((1024, 680))
screen.fill('White')
pygame.display.set_caption("2D Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font("font/Comica Boom.otf", 70)
font2 = pygame.font.Font("font/Comica Boom.otf", 30)

game_active = False
start_time = 0
score = 0
hi_score=0

# Load and play background music
bg_music1 = pygame.mixer.Sound("audio/space_line.mp3")
bg_music2 = pygame.mixer.Sound("audio/gamemusic.mp3")
jump_music = pygame.mixer.Sound("audio/jump.mp3")
jump_music.set_volume(0.5)
bg_music2.play(loops=-1)

# Load game assets
back_surface = pygame.image.load('image/backG.jpg').convert()
ground_surface = pygame.image.load('image/gro.png').convert_alpha()

fly_surface = pygame.image.load("image/fly_en1.png").convert_alpha()

# Load enemy frames for animation
enemy_frame1 = pygame.image.load("image/enm1.png").convert_alpha()
enemy_frame2 = pygame.image.load("image/enm2.png").convert_alpha()
enemy_frame3 = pygame.image.load("image/enm3.png").convert_alpha()
enemy_frame4 = pygame.image.load("image/enm4.png").convert_alpha()
enemy_frame5 = pygame.image.load("image/enm5.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2, enemy_frame3, enemy_frame4, enemy_frame5, enemy_frame4, enemy_frame3, enemy_frame2]
enemy_frame_index = 0
enemy_surf = enemy_frames[enemy_frame_index]

# Initialize obstacle list
obstacle_rect_list = []

player_walk1 = pygame.image.load("image/rn1.png").convert_alpha()
player_walk2 = pygame.image.load("image/rn2.png").convert_alpha() 
player_walk3 = pygame.image.load("image/rn3.png").convert_alpha()
player_walk4 = pygame.image.load("image/rn4.png").convert_alpha()
player_run = [player_walk2, player_walk3, player_walk4, player_walk1]
player_index = 0
player_jump = pygame.image.load("image/jp.png").convert_alpha()

player_surf = player_run[player_index]
player_rect = player_surf.get_rect(bottomleft=(200, 580))
player_gravity = 0

intro = pygame.image.load("image/gm.png").convert_alpha()
intro = pygame.transform.rotozoom(intro, 0, 1)
intro_rect = intro.get_rect(center=(512, 300))

game_name = test_font.render('Cosmic Runner', True, "#FFD93D")
game_name_rect = game_name.get_rect(center=(512, 80))

game_msg = test_font.render("Press space to run", True, "#8BE8E5")
game_msg_rect = game_msg.get_rect(center=(512, 530))

# Set up obstacle and enemy animation timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

enemy_animation_timer= pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 480:
                    player_gravity = -23
                    jump_music.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(enemy_surf.get_rect(bottomright=(randint(1000, 1200), 587)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(1000, 1200), 330)))

            # Animate enemy frames on enemy animation timer
            if event.type == enemy_animation_timer:
                if enemy_frame_index>7:
                    enemy_frame_index=0
                enemy_surf= enemy_frames[enemy_frame_index]
                enemy_frame_index+=1

    if game_active:
        screen.blit(back_surface, (0, 0))
        screen.blit(ground_surface, (0, 520))

        score = display_score()

        if score>=hi_score:
            hi_score=score

        # Update player position and animation
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 580:
            player_rect.bottom = 580
        player_animation()
        screen.blit(player_surf, player_rect)

        # Update obstacles and check for collisions
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        # Render the game-over screen when the game is not active
        screen.fill("#071952")
        screen.blit(intro, intro_rect)
        obstacle_rect_list.clear()
        player_rect.bottomleft = (200, 580)
        player_gravity = 0

        # Render the score and game messages
        score_msg = test_font.render(f'Your Score: {score}', True, '#8696FE')
        score_msg_rect = score_msg.get_rect(center=(512, 530))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)
            
    pygame.display.update()
    clock.tick(60)