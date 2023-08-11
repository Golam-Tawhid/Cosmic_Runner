import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("image/rn1.png").convert_alpha()
        player_walk2 = pygame.image.load("image/rn2.png").convert_alpha() 
        player_walk3 = pygame.image.load("image/rn3.png").convert_alpha()
        player_walk4 = pygame.image.load("image/rn4.png").convert_alpha()
        self.player_walk=[player_walk2, player_walk3, player_walk4, player_walk1]
        self.player_index=0
        self.player_jump= pygame.image.load("image/jp.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,587))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys= pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=587:
            self.gravity =- 20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity+=1
        self.rect.y += self.gravity
        if self.rect.bottom >=587:
            self.rect.bottom = 587

    def animation_state(self):
        if self.rect.bottom <587:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index=0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

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
            self.frames = [enemy_frame1, enemy_frame2, enemy_frame3, enemy_frame4, enemy_frame5]
            y_pos = 587 # Vertical position of the obstacle

        self.animation_index=0 # Current frame index
        self.image=self.frames[self.animation_index] # Current frame image
        self.rect = self.image.get_rect(midbottom = (randint(1000,1200),y_pos)) # Obstacle's position
    def animation_state(self):
        self.animation_index += 0.1 # Increment the animation index
        if self.animation_index >= len(self.frames):
            self.animation_index=0 # Reset animation index if it exceeds the frame count
        self.image = self.frames[int(self.animation_index)] # Update the current frame image

    def update(self):
        self.animation_state()
        self.rect.x -=6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: # If the obstacle is off the left edge of the screen
            self.kill() # Remove the obstacle from the sprite group

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    score_surf = test_font2.render(f'Score: {current_time}', True, "#3E001F")
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
        obstacle_group.empty()
        return False
    else:
        return True

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
hi_score=0

bg_music1 = pygame.mixer.Sound("audio/space_line.mp3")
bg_music2 = pygame.mixer.Sound("audio/gamemusic.mp3")
bg_music1.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

back_surface = pygame.image.load('image/backG.jpg').convert()
ground_surface = pygame.image.load('image/gro.png').convert_alpha()

player_stand = pygame.image.load("image/gm.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rect = player_stand.get_rect(center=(450, 300))

game_name = test_font.render('Vaag Bug', True, "#4E4FEB")
game_name_rect = game_name.get_rect(center=(450, 80))

game_msg = test_font.render("Press space to run", True, "#8BE8E5")
game_msg_rect = game_msg.get_rect(center=(450, 530))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

enemy_animation_timer= pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly","enemy","enemy","enemy"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(back_surface, (0, 0))
        screen.blit(ground_surface, (0, 520)) 

        score = display_score()

        if score>=hi_score:
            hi_score=score

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill("#071952")
        screen.blit(player_stand, player_stand_rect)

        score_msg = test_font.render(f'Your Score: {score}', True, '#8696FE')
        score_msg_rect = score_msg.get_rect(center=(450, 530))

        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)
            
    pygame.display.update()
    clock.tick(60)