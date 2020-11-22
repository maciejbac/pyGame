#!/usr/bin/python

# importing required packages
import pygame
import random
import math

# setting initial variables for the window
BLUE = (0, 0, 255)
RED = (255, 0, 0)
running = True
(window_width, window_height) = (800, 600)
(game_width, game_height) = (window_width - 100, window_height - 100)

background_color = (120, 160, 250)
pygame.display.set_caption('Ball game')
particle_count = 25
gravity_on = False
gravity = (math.pi, 0.02)
mass_of_air = 0.1
elasticity = 0.95
particle_max_size = 20

# Initialize the screen object
screen = pygame.display.set_mode((window_width, window_height))

# Initialize empty particle array
my_particles = []


class Particle:
    # Constructor function that assigns parameters to internal values of the Particle object
    def __init__(self, x, y, size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass

        # TEMPORARY: set random colour and thickness
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.thickness = 40

        # set default speed and angle, can be changed when creating Particle object
        self.speed = 0.01
        self.angle = math.pi / 2

        self.drag = (self.mass / (self.mass + mass_of_air)) ** self.size

    # Call pygame package to draw circle, pass values stored in the current (self) Particle object as parameters
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    # Update the x and y position based on the angle and speed of the Particle object
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

        if gravity_on:
            # Gravity function that adds a pre-defined gravity vector to the existing movement vector of the particle
            (self.angle, self.speed) = add_vectors(self.angle, self.speed, *gravity)

        # Multiply particle's speed by the drag to introduce air drag
        self.speed *= self.drag

    # if statements that detect and respond to collisions. Each if statement handles 1 out of 4 sides of the window.
    def bounce(self):
        if self.x > game_width - self.size:
            self.x = 2 * (game_width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > game_height - self.size:
            self.y = 2 * (game_height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


# Function that adds two vectors together - used to handle gravity and collisions
def add_vectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length


def find_particle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None


# Collision detection function
def collide(p1, p2):
    col_dx = p1.x - p2.x
    col_dy = p1.y - p2.y
    distance = math.hypot(col_dx, col_dy)

    if distance < p1.size + p2.size:
        tangent = math.atan2(col_dy, col_dx)
        angle = math.atan2(col_dy, col_dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass
        (p1.angle, p1.speed) = add_vectors(*(p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass),
                                           *(angle, 2 * p2.speed * p2.mass / total_mass))
        (p2.angle, p2.speed) = add_vectors(*(p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass),
                                           *(angle + math.pi, 2 * p1.speed * p1.mass / total_mass))
        p1.speed *= elasticity
        p2.speed *= elasticity

        angle = 0.5 * math.pi + tangent
        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap


# Create a number of Particle objects using random values to populate the screen
for n in range(particle_count):
    particle_size = random.randint(10, particle_max_size)
    particle_density = 1.00

    particle_x = random.randint(particle_size, game_width - particle_size)
    particle_y = random.randint(particle_size, game_height - particle_size)

    particle = Particle(particle_x, particle_y, particle_size, particle_density * particle_size ** 2)
    # particle.colour = (200 - particle_density * 10, 200 - particle_density * 10, 255)

    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)
    my_particles.append(particle)

selected_particle = None
# Main loop of the program
while running:
    # Listen for Quit message from the X button on the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Detect mouse click, if the user clicked on a particle
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = find_particle(my_particles, mouseX, mouseY)

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    # Reset the scene
    screen.fill(background_color)

    # Iterate through all particle objects
    for i, particle in enumerate(my_particles):
        if particle != selected_particle:
            particle.move()
            particle.bounce()

        if selected_particle:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - selected_particle.x
            dy = mouseY - selected_particle.y
            selected_particle.angle = math.atan2(dy, dx) - 0.5 * math.pi
            selected_particle.speed = math.hypot(dx, dy) * 0.1
            # Draw dot when a particle is selected
            pygame.draw.line(screen, (0, 0, 0), (mouseX, mouseY), (selected_particle.x, selected_particle.y))
            pygame.draw.circle(screen, (0, 0, 0), (mouseX, mouseY), 5, 5)

        particle.display()

        for particle2 in my_particles[i + 1:]:
            collide(particle, particle2)

    # Swap the frame buffer
    pygame.display.flip()
