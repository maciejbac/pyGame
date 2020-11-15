import pygame

running = True
pygame.display.set_caption('Ball game')
(width, height) = (300, 300)
background_color = (120, 160, 250)


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 255, 255)
        self.thickness = 1

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)


screen = pygame.display.set_mode((width, height))
screen.fill(background_color)

particle = Particle(150, 50, 15)
particle.display()

pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
