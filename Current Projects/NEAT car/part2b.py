# Driving car but you die when you hit the grass
# There is also a timer
# Made checkpoints so you can drive laps properly now

import pygame
import os
import math
import sys
import neat

SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("Assets", "track.png"))

GRASS_COLOR = pygame.Color(2, 105, 31, 255) # +
START_POS = (490, 820) # +

pygame.init()

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(490, 820))
        self.drive_state = False
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 3
        self.direction = 0
        self.time_since_death = 0

        # Lap timing
        self.last_lap_time = None
        self.best_lap_time = float('inf')
        self.crossed_finish_line = False
        self.reached_halfway = False

    def update(self):
        self.drive()
        self.rotate()
        self.check_collision()

    def drive(self):
        if self.drive_state:
            self.rect.center += self.vel_vector * 6

    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    # +
    def check_collision(self):
        # Get color of the pixel under the car's center position
        x, y = int(self.rect.centerx), int(self.rect.centery)
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:  # Ensure within bounds
            color_at_car = SCREEN.get_at((x, y))
            if color_at_car == GRASS_COLOR:
                print("Car hit the grass! Respawning...")
                self.respawn()

    def respawn(self):
        global time_since_death
        self.time_since_death = pygame.time.get_ticks()
        self.rect.center = START_POS
        self.angle = 0
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.direction = 0
        self.drive_state = False
        self.crossed_finish_line = False
        self.reached_halfway = False


    def check_finish_line(self, start_time):
        global time_since_death
        x, y = self.rect.center

        # Check if car is at the finish line (vertical strip at start position)
        # Halfway point check
        if not self.reached_halfway and 470 <= x <= 510 and 140 <= y <= 240:
            print("Reached halfway point!")
            self.reached_halfway = True

        # Finish line check (only if halfway point is reached)
        if self.reached_halfway and 480 <= x <= 500 and 760 <= y <= 900:
            if not self.crossed_finish_line:
                self.crossed_finish_line = True
                if self.last_lap_time is not None:
                    if self.last_lap_time > self.time_since_death:
                        lap_time = (pygame.time.get_ticks() - self.last_lap_time) // 1000
                        print(f"Lap Time: {lap_time}s")
                    else:
                        lap_time = (pygame.time.get_ticks() - self.time_since_death) // 1000
                        print(f"Lap Time: {lap_time}s")
                else:
                    lap_time = pygame.time.get_ticks() // 1000
                if lap_time < self.best_lap_time:
                    self.best_lap_time = lap_time
                    print(f"New Best Lap Time: {self.best_lap_time}s")

                self.last_lap_time = pygame.time.get_ticks()
                self.reached_halfway = False  # Reset halfway point after completing a lap

        # Reset flag when car leaves finish line
        elif not (530 <= x <= 560 and 780 <= y <= 880):
            self.crossed_finish_line = False

    def draw_info(self, start_time):
        font = pygame.font.Font(None, 36)

        # Current time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f'Time: {minutes:02}:{seconds:02}'

        # Best lap time
        best_lap_text = f'Best Lap: {"--:--" if self.best_lap_time == float("inf") else f"{self.best_lap_time // 60:02}:{self.best_lap_time % 60:02}"}'

        halfway_status = "Halfway: Active" if self.reached_halfway else "Halfway: Inactive"
        finish_status = "Finish: Active" if self.crossed_finish_line else "Finish: Inactive"

        # Draw background box
        info_box = pygame.Rect(SCREEN_WIDTH - 220, 10, 210, 70)
        pygame.draw.rect(SCREEN, (0, 0, 0), info_box, border_radius=5)
        pygame.draw.rect(SCREEN, (255, 255, 255), info_box, 2, border_radius=5)

        # Blit text onto the screen
        timer_surface = font.render(timer_text, True, (255, 255, 255))
        best_lap_surface = font.render(best_lap_text, True, (255, 255, 255))
        halfway_surface = font.render(halfway_status, True, (255, 255, 255))
        finish_surface = font.render(finish_status, True, (255, 255, 255))
        # death_time = font.render(str(self.time_since_death), True, (255, 255, 255))
        # lap_time = font.render(str(self.last_lap_time), True, (255, 255, 255))
        finish_surface = font.render(finish_status, True, (255, 255, 255))
        SCREEN.blit(timer_surface, (SCREEN_WIDTH - 210, 20))
        SCREEN.blit(best_lap_surface, (SCREEN_WIDTH - 210, 50))
        SCREEN.blit(halfway_surface, (SCREEN_WIDTH - 210, 80))
        SCREEN.blit(finish_surface, (SCREEN_WIDTH - 210, 110))
        # SCREEN.blit(death_time, (SCREEN_WIDTH - 210, 130))
        # SCREEN.blit(lap_time, (SCREEN_WIDTH - 210, 150))
        

    # +

car = pygame.sprite.GroupSingle(Car())

def eval_genomes():
    start_time = pygame.time.get_ticks() # +
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0, 0))

        # Draw the finish line
        pygame.draw.line(SCREEN, (255, 0, 0), (490, 760), (490, 900), 5)

        # Draw the halfway line
        pygame.draw.line(SCREEN, (0, 0, 255), (490, 140), (490, 240), 5)

        # User Input
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = False
            car.sprite.direction = 0 # +
        
        # Drive 
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = True
        
        # Steer
        if user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1

        # Update
        # Check for collisions after update but before drawing on screen
        car.update()
        car.sprite.check_collision()

        # Check finish line
        car.sprite.check_finish_line(start_time)

        car.draw(SCREEN)
        car.sprite.draw_info(start_time)
        pygame.display.update()

eval_genomes()