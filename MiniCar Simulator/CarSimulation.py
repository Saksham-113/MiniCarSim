import pygame
import math
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

class Vehicle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.theta = 0.0  
        self.v_l = 0.0  
        self.v_r = 0.0  
        self.L = 40.0  
        self.max_velocity = 200.0  
        self.acceleration = 150.0 
        self.friction = 0.98 
        self.original_image = pygame.image.load('Graphics/car.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def handle_input(self, keys, dt):
        if keys[pygame.K_UP]:
            self.v_l += self.acceleration * dt
            self.v_r += self.acceleration * dt
        if keys[pygame.K_DOWN]:
            self.v_l -= self.acceleration * dt
            self.v_r -= self.acceleration * dt
        if keys[pygame.K_LEFT]:
            self.v_l += self.acceleration * dt
            self.v_r -= self.acceleration * dt
        if keys[pygame.K_RIGHT]:
            self.v_l -= self.acceleration * dt
            self.v_r += self.acceleration * dt

    def update(self, dt, keys):
        self.v_l *= self.friction
        self.v_r *= self.friction
        if abs(self.v_l) < 2: self.v_l = 0
        if abs(self.v_r) < 2: self.v_r = 0
        self.v_l = max(-self.max_velocity, min(self.v_l, self.max_velocity))
        self.v_r = max(-self.max_velocity, min(self.v_r, self.max_velocity))
        v = (self.v_r + self.v_l) / 2.0
        omega = (self.v_r - self.v_l) / self.L
        self.theta += math.degrees(omega * dt)
        move_theta_rad = math.radians(90 - self.theta)
        self.x += v * math.cos(move_theta_rad) * dt
        self.y -= v * math.sin(move_theta_rad) * dt
        self.image = pygame.transform.rotate(self.original_image, -self.theta)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Differential Drive Vehicle Simulation")
    clock = pygame.time.Clock()
    world_surface = pygame.image.load("Graphics/world.png")
    vehicle = Vehicle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        vehicle.handle_input(keys, dt)
        vehicle.update(dt, keys)
        screen.blit(world_surface, (0, 0))
        vehicle.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
