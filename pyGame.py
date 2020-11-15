import pygame
import random

BLUE = (0, 0, 255)
RED = (255, 0, 0)
running = True
pygame.display.set_caption('Ball game')
(width, height) = (300, 300)
background_color = (120, 160, 250)


class Particle:
    def __init__(self, x, y, size, colour):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.thickness = 1

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)


screen = pygame.display.set_mode((width, height))
screen.fill(background_color)

particle_count = 10
my_particles = []

for n in range(particle_count):
    size = random.randint(10, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    my_particles.append(Particle(x, y, size, BLUE))

for particle in my_particles:
    particle.display()

pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
