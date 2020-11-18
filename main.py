#!/usr/bin/python
import pygame
import random
import math

BLUE = (0, 0, 255)
RED = (255, 0, 0)
running = True
pygame.display.set_caption('Ball game')
(width, height) = (600, 600)
background_color = (120, 160, 250)


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.thickness = 1

        self.speed = 0.01
        self.angle = math.pi / 2

    def display(self):

        # pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)

        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle


screen = pygame.display.set_mode((width, height))

particle_count = 10
my_particles = []

for n in range(particle_count):
    particle_size = random.randint(10, 20)
    particle_x = random.randint(particle_size, width - particle_size)
    particle_y = random.randint(particle_size, height - particle_size)

    particle = Particle(particle_x, particle_y, particle_size)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)
    my_particles.append(particle)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()

    pygame.display.flip()

