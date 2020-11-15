import pygame

running = True
pygame.display.set_caption('Ball game')
(width, height) = (300, 300)
background_color = (120, 160, 250)

screen = pygame.display.set_mode((width, height))
screen.fill(background_color)

pygame.draw.circle(screen, (0, 0, 255), (150, 50), 15, 1)
pygame.display.flip()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
