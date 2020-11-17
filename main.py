#!/usr/bin/python
import pygame
import random
import math

BLUE = (0, 0, 255)
RED = (255, 0, 0)
running = True
pygame.display.set_caption('Ball game')
(width, height) = (300, 300)
background_color = (120, 160, 250)


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.thickness = 50

        self.speed = 0.01
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed


screen = pygame.display.set_mode((width, height))

particle_count = 10
my_particles = []

for n in range(particle_count):
    size = random.randint(10, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    my_particles.append(Particle(x, y, size))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    for particle in my_particles:
        particle.move()
        particle.display()

    pygame.display.flip()

