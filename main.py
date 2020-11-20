#!/usr/bin/python

# importing required packages
import pygame
import random
import math

# setting initial variables for the window
BLUE = (0, 0, 255)
RED = (255, 0, 0)
running = True
(width, height) = (600, 600)
background_color = (120, 160, 250)
pygame.display.set_caption('Ball game')
particle_count = 100
gravity = (math.pi, 0.01)

# Initialize the screen object
screen = pygame.display.set_mode((width, height))

# Initialize empty particle array
my_particles = []


class Particle:
    # Constructor function that assigns parameters to internal values of the Particle object
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        # TEMPORARY: set random colour and thickness, TODO: add support for manual colour selection
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.thickness = 1

        # set default speed and angle, can be changed when creating Particle object
        self.speed = 0.01
        self.angle = math.pi / 2

    # Call pygame package to draw circle, pass values stored in the current (self) Particle object as parameters
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    # Update the x and y position based on the angle and speed of the Particle object
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

        # Gravity function that adds a pre-defined gravity vector to the existing movement vector of the particle
        (self.angle, self.speed) = add_vectors(self.angle, self.speed, *gravity)

    # if statements that detect and respond to collisions. Each if statement handles 1 out of 4 sides of the window.
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


def add_vectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length


# Create a number of Particle objects using random values to populate the screen
for n in range(particle_count):
    particle_size = random.randint(10, 20)
    particle_x = random.randint(particle_size, width - particle_size)
    particle_y = random.randint(particle_size, height - particle_size)

    particle = Particle(particle_x, particle_y, particle_size)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)
    my_particles.append(particle)

# Main loop of the program
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Reset the scene
    screen.fill(background_color)

    # Iterate through all particle objects
    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()

    # Swap the frame buffer
    pygame.display.flip()

