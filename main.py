#!/usr/bin/python

# importing required packages
from os import lseek
import pygame
import pygame.freetype
import pygame.font
import random
import math


# setting initial variables for the window
RED = (255, 0, 0)
running = True
(window_width, window_height) = (900, 600)
(game_width, game_height) = (window_width - 200, window_height)
selected_particle = None
background_color = (120, 160, 250)
pygame.display.set_caption('Ball game')
particle_count = 35
random_momentum = True
gravity_on = False
gravity = (math.pi, 0.02)
mass_of_air = 0.01
elasticity = 0.5
particle_max_size = 30
margin = 5

# Initialize the screen object
screen = pygame.display.set_mode((window_width, window_height))

# Initialize pygame.font library
pygame.font.init()
font = pygame.font.Font(None, 20)


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
        self.thickness = 50

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


class Player(Particle):
    pass 

    def playerTestFunction():
        return 0


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

    # Collision handling requires refactoring as it doesn't currently take into consideration the angle at which both
    # particles collide
    if distance < p1.size + p2.size:
        angle = math.atan2(col_dy, col_dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = add_vectors(*(p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass),
                                           *(angle, 2 * p2.speed * p2.mass / total_mass))

        (p2.angle, p2.speed) = add_vectors(*(p1.angle, p2.speed * (p2.mass - p1.mass) / total_mass),
                                           *(angle + math.pi, 2 * p1.speed * p1.mass / total_mass))

        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - distance + 1)

        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap

        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap


def init_random_particles():
    # Create a number of Particle objects using random values to populate the screen
    for n in range(particle_count):
        particle_size = random.randint(10, particle_max_size)
        particle_density = 1.00

        particle_x = random.randint(particle_size, game_width - particle_size)
        particle_y = random.randint(particle_size, game_height - particle_size)

        new_particle = Particle(particle_x, particle_y, particle_size, particle_density * particle_size ** 2)
        # particle.colour = (200 - particle_density * 10, 200 - particle_density * 10, 255)

        new_particle.speed = random.random()

        if random_momentum == True:
            new_particle.speed = random.randint(1, 3)                                                                                                                                                   
            new_particle.angle = random.uniform(0, math.pi * 2)
        else:
            new_particle.speed = 0
            new_particle.angle = random.uniform(0, math.pi * 2)

        my_particles.append(new_particle)
    #append player particle
    my_particles.append(Player(0,0, 50, 1 * 20 ** 2))


def init_test_particles():
    test_particle1 = Particle(game_width / 2, 100, 30, 1.00 * 50 ** 2)
    test_particle2 = Particle(game_width / 2, 200, 30, 1.00 * 10 ** 2)

    test_particle1.speed = 0.0
    test_particle1.angle = random.uniform(0, math.pi * 2)

    test_particle2.speed = 0.0
    test_particle2.angle = random.uniform(0, math.pi * 2)

    my_particles.append(test_particle1)
    my_particles.append(test_particle2)


def write(text, location, color=(0, 0, 0)):
    screen.blit(font.render(text, True, color), location)


def draw_game():
    # Reset the scene
    screen.fill(background_color)
    pygame.draw.line(screen, (0, 0, 0), (game_width, 0), (game_width, game_height))

    state = ''
    moving_particles_count = 0

    # Iterate through all particle objects
    for i, particle in enumerate(my_particles):
        if particle != selected_particle:
            particle.move()
            particle.bounce()

        for particle2 in my_particles[i + 1:]:
            collide(particle, particle2)

        particle.display()

        if selected_particle:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - selected_particle.x
            dy = mouseY - selected_particle.y
            selected_particle.angle = math.atan2(dy, dx) - 0.5 * math.pi
            selected_particle.speed = math.hypot(dx, dy) * 0.1
            # Draw line between mouse pointer and the particle when selected
            pygame.draw.line(screen, (0, 0, 0), (mouseX, mouseY), (selected_particle.x, selected_particle.y))

            pygame.draw.line(screen, (255, 255, 255), (selected_particle.x, selected_particle.y),
                             (selected_particle.x + (selected_particle.x - mouseX), selected_particle.y +
                              (selected_particle.y - mouseY)))

            pygame.draw.circle(screen, (0, 0, 0), (mouseX, mouseY), 5, 5)

            write('V = ' + str(round(math.hypot(dx, dy), 2)), (mouseX + 20, mouseY + 10))

        if particle.speed > 0.01:
            moving_particles_count += 1
        else:
            particle.speed = 0

        if moving_particles_count == 0:
            state = 'Still'
        else:
            state = 'Moving'

    # Draw text
    ball_count = len(my_particles)
    write('Ball count: ' + str(ball_count), (game_width + margin, margin))
    write('Current state: ' + state, (game_width + margin, margin * 4))
    write('Balls moving: ' + str(moving_particles_count), (game_width + margin, margin * 7))

    # Swap the frame buffer
    pygame.display.flip()


init_random_particles()
# init_test_particles()


# Main loop of the program
while running:
    # Listen for Quit message from the X button on the window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Detect mouse click, if the user clicked on a particle
        if event.type == pygame.MOUSEBUTTONDOWN:
            (sel_mouseX, sel_mouseY) = pygame.mouse.get_pos()
            selected_particle = find_particle(my_particles, sel_mouseX, sel_mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    draw_game()
