import pygame
from sys import exit
from random import randint,choice
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_run1 = pygame.image.load("image/rn1.png").convert_alpha()
        player_run2 = pygame.image.load("image/rn2.png").convert_alpha() 
        player_run3 = pygame.image.load("image/rn3.png").convert_alpha()
        player_run4 = pygame.image.load("image/rn4.png").convert_alpha()
        self.player_run=[player_run2, player_run3, player_run4, player_run1]
        self.player_index=0
        self.player_jump= pygame.image.load("image/jp.png").convert_alpha()

        self.current_health = 1000
        self.target_health = 1000
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(midbottom = (250,580))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys= pygame.key.get_pressed()
        if score!=0 and keys[pygame.K_SPACE] and self.rect.bottom >=580:
            self.gravity =- 23
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y += self.gravity
        if self.rect.bottom >=580:
            self.rect.bottom = 580

    def animation_state(self):
        if self.rect.bottom <580:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_run):
                self.player_index=0
            self.image = self.player_run[int(self.player_index)]

    def get_damage(self):
        if self.target_health > 0:
            self.target_health -= 5
        if self.target_health < 0:
            self.target_health = 0

    def advanced_health(self):
        transition_width = 0
        transition_color = (255,0,0)
        
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0,255,0)
        
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed 
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)

        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(10,90,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,45,transition_width,25)
		
        pygame.draw.rect(screen,("Yellow"),(10,90,self.health_bar_length,25))
        pygame.draw.rect(screen,(255,0,0),health_bar)
        pygame.draw.rect(screen,transition_color,transition_bar)	
        pygame.draw.rect(screen,(255,255,255),(10,90,self.health_bar_length,25),4)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.advanced_health()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        # Initialize the obstacle based on its type (fly or enemy)
        if type == "fly":
            fly_1 = pygame.image.load("image/fly_en1.png").convert_alpha()
            self.frames = [fly_1] 
            y_pos = 330 # Vertical position of the obstacle
        else:
            enemy_frame1 = pygame.image.load("image/enm1.png").convert_alpha()
            enemy_frame2 = pygame.image.load("image/enm2.png").convert_alpha()
            enemy_frame3 = pygame.image.load("image/enm3.png").convert_alpha()
            enemy_frame4 = pygame.image.load("image/enm4.png").convert_alpha()
            enemy_frame5 = pygame.image.load("image/enm5.png").convert_alpha()
            self.frames = [enemy_frame1, enemy_frame2, enemy_frame3, enemy_frame4, enemy_frame5, enemy_frame4, enemy_frame3, enemy_frame2]
            y_pos = 587 # Vertical position of the obstacle

        self.animation_index = 0 # Current frame index
        self.image = self.frames[self.animation_index] # Current frame image
        self.rect = self.image.get_rect(midbottom = (randint(1000,1200),y_pos)) # Obstacle's position
    def animation_state(self):
        self.animation_index += 0.08 # Increment the animation index
        if self.animation_index >= len(self.frames):
            self.animation_index = 0 # Reset animation index if it exceeds the frame count
        self.image = self.frames[int(self.animation_index)] # Update the current frame image

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: # If the obstacle is off the left edge of the screen
            self.kill() # Remove the obstacle from the sprite group

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    score_surf = test_font2.render(f'Score: {current_time}', True, "Black")
    score_rect = score_surf.get_rect(topleft=(350, 10))
    pygame.draw.rect(screen, "#C147E9", score_rect)
    pygame.draw.rect(screen, '#645CBB', score_rect, 3)
    screen.blit(score_surf, score_rect)

    hscore_surf = test_font2.render(f'Highest Score: {hi_score}', True, "#3E001F")
    hscore_rect = hscore_surf.get_rect(topleft=(15,10))
    pygame.draw.rect(screen, "#57C5B6", hscore_rect)
    pygame.draw.rect(screen, '#159895', hscore_rect, 3)
    screen.blit(hscore_surf, hscore_rect)

    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        player.sprite.get_damage()
        if player.sprite.target_health<=0:
            return False
        else:
            return True
    else:
        return True   

pygame.init()
screen = pygame.display.set_mode((1024, 680))
screen.fill('White')
pygame.display.set_caption("2D Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font("font/Comica Boom.otf", 70)
test_font2 = pygame.font.Font("font/Comica Boom.otf", 30)

game_active = False
start_time = 0
score = 0
hi_score=0
 
bg_music1 = pygame.mixer.Sound("audio/space_line.mp3")
bg_music2 = pygame.mixer.Sound("audio/gamemusic.mp3")
bg_music2.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

back_surface = pygame.image.load('image/backG.jpg').convert_alpha()
bg = pygame.image.load("image/gro.png").convert_alpha()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

scroll = 0
tiles = math.ceil(1024  / bg_width) + 1

intro = pygame.image.load("image/gm.png").convert_alpha()
intro = pygame.transform.rotozoom(intro, 0, 1)
intro_rect = intro.get_rect(center=(512, 300))

game_name = test_font.render('Cosmic Runner', True, "#FFD93D")
game_name_rect = game_name.get_rect(center=(512, 80))

game_msg = test_font.render("Press space to run", True, "#8BE8E5")
game_msg_rect = game_msg.get_rect(center=(512, 530))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["enemy","enemy","fly","enemy"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(back_surface, (0, 0))
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 520))
            bg_rect.x = i * bg_width + scroll

        #scroll background
        scroll -= 3

        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0 

        score = display_score()

        if score>=hi_score:
            hi_score=score

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill("#27374D")
        screen.blit(intro, intro_rect)

        score_msg = test_font.render(f'Your Score: {score}', True, '#FF78C4')
        score_msg_rect = score_msg.get_rect(center=(512, 530))

        game_over = test_font.render("GAME OVER", True, '#B31312')
        game_over_rect = game_over.get_rect(center=(512, 80))

        

        if score == 0:
            screen.blit(game_name, game_name_rect)
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(game_over, game_over_rect)
            screen.blit(score_msg, score_msg_rect)
            
    pygame.display.update()
    clock.tick(60)