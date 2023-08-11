import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 680

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Scroll")

back_surface = pygame.image.load('image/backG.jpg').convert_alpha()
bg = pygame.image.load("image/gro.png").convert_alpha()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

scroll = 0
tiles = math.ceil(SCREEN_WIDTH  / bg_width) + 1

run = True
while run:

  clock.tick(FPS)
  screen.blit(back_surface, (0, 0))
  for i in range(0, tiles):
    screen.blit(bg, (i * bg_width + scroll, 520))
    bg_rect.x = i * bg_width + scroll

  scroll -= 5

  if abs(scroll) > bg_width:
    scroll = 0
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()