GRASS_COLOR = pygame.Color(2, 105, 31, 255)
START_POS = (490, 820)
HALFWAY_POS = (490, 190)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=START_POS)
        self.drive_state = False
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0

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

    def check_collision(self):
        x, y = int(self.rect.centerx), int(self.rect.centery)
        if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
            color_at_car = SCREEN.get_at((x, y))
            if color_at_car == GRASS_COLOR:
                print("Car hit the grass! Respawning...")
                self.respawn()

    def respawn(self):
        self.rect.center = START_POS
        self.angle = 0
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.direction = 0
        self.drive_state = False
        self.reached_halfway = False  # ✅ Reset halfway point when respawning

    def check_finish_line(self, start_time):
        x, y = self.rect.center

        # ✅ Halfway point check
        if not self.reached_halfway and 470 <= x <= 510 and 170 <= y <= 210:
            print("Reached halfway point!")
            self.reached_halfway = True

        # ✅ Finish line check (only if halfway point is reached)
        if self.reached_halfway and 470 <= x <= 510 and 800 <= y <= 880:
            if not self.crossed_finish_line:
                self.crossed_finish_line = True
                if self.last_lap_time is not None:
                    lap_time = (pygame.time.get_ticks() - self.last_lap_time) // 1000
                    print(f"Lap Time: {lap_time}s")
                    if lap_time < self.best_lap_time:
                        self.best_lap_time = lap_time
                        print(f"New Best Lap Time: {self.best_lap_time}s")

                self.last_lap_time = pygame.time.get_ticks()
                self.reached_halfway = False  # ✅ Reset halfway point after completing a lap

        # ✅ Reset flag when car leaves finish line
        elif not (470 <= x <= 510 and 800 <= y <= 880):
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

        # Draw background box
        info_box = pygame.Rect(SCREEN_WIDTH - 220, 10, 210, 70)
        pygame.draw.rect(SCREEN, (0, 0, 0), info_box, border_radius=5)
        pygame.draw.rect(SCREEN, (255, 255, 255), info_box, 2, border_radius=5)

        # Blit text onto the screen
        timer_surface = font.render(timer_text, True, (255, 255, 255))
        best_lap_surface = font.render(best_lap_text, True, (255, 255, 255))
        SCREEN.blit(timer_surface, (SCREEN_WIDTH - 210, 20))
        SCREEN.blit(best_lap_surface, (SCREEN_WIDTH - 210, 50))
