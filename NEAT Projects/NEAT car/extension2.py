import pygame
import os
import math
import sys
import neat
import time

pygame.init()

SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TIME_LIMIT = 10

TRACK = pygame.image.load(os.path.join("Assets", "track.png"))
FONT = pygame.font.Font('freesansbold.ttf', 20)

# Global config placeholder
config = None

# Pure-Pygame network visualizer
def draw_net(screen, genome, config, rect):
    x, y, w, h = rect
    # 1) Group node IDs by layer
    layers = {}
    for nid, node in genome.nodes.items():
        layer = config.genome_config.node_evaluator.get_node_activation(nid).layer
        layers.setdefault(layer, []).append(nid)

    num_layers = len(layers)
    pos = {}
    # 2) Assign positions
    for i, layer in enumerate(sorted(layers)):
        nodes = layers[layer]
        for j, nid in enumerate(nodes):
            px = x + (i / (num_layers - 1)) * w
            py = y + ((j + 1) / (len(nodes) + 1)) * h
            pos[nid] = (int(px), int(py))

    # 3) Draw connections
    for conn in genome.connections.values():
        if not conn.enabled:
            continue
        inp, out = conn.key
        wgt = conn.weight
        color = (0, 200, 0) if wgt > 0 else (200, 0, 0)
        thickness = max(1, min(5, int(abs(wgt) * 5)))
        pygame.draw.line(screen, color, pos[inp], pos[out], thickness)

    # 4) Draw nodes
    for nid, (px, py) in pos.items():
        radius = 8 if nid in config.genome_config.output_keys else 5
        is_output = nid in config.genome_config.output_keys
        node_color = (50, 50, 200) if is_output else (200, 200, 200)
        pygame.draw.circle(screen, node_color, (px, py), radius)
        pygame.draw.circle(screen, (0, 0, 0), (px, py), radius, 1)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(490, 820))
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []

    def update(self):
        self.radars.clear()
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
        self.data()

    def drive(self):
        self.rect.center += self.vel_vector * 6

    def collision(self):
        length = 40
        right = [
            int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
            int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)
        ]
        left = [
            int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
            int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)
        ]
        # Die on collision with grass
        if SCREEN.get_at(tuple(right)) == pygame.Color(2, 105, 31, 255) or \
           SCREEN.get_at(tuple(left)) == pygame.Color(2, 105, 31, 255):
            self.alive = False
        # Draw collision points
        pygame.draw.circle(SCREEN, (0, 255, 255), right, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255), left, 4)

    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        elif self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self, radar_angle):
        length, x, y = 0, int(self.rect.center[0]), int(self.rect.center[1])
        # Cast ray until grass or max length
        while SCREEN.get_at((x, y)) != pygame.Color(2, 105, 31, 255) and length < 200:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
        # Draw radar line & endpoint
        pygame.draw.line(SCREEN, (255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), 3)
        dist = int(math.hypot(self.rect.center[0] - x, self.rect.center[1] - y))
        self.radars.append((radar_angle, dist))

    def data(self):
        return [d for (_, d) in self.radars]

# Helpers to remove a dead car
def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)

# Genome evaluation
def eval_genomes(genomes, cfg):
    global cars, ge, nets
    # Setup cars, genomes, nets
    cars, ge, nets = [], [], []
    for gid, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, cfg))
        genome.fitness = 0

    run = True
    start_time = time.time()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0, 0))

        # Draw NN graph for the first alive genome
        if ge:
            draw_net(SCREEN, ge[0], config, (SCREEN_WIDTH - 550, 20, 530, 300))

        # Break if no cars or out of time
        if not cars or time.time() - start_time > TIME_LIMIT:
            break

        # Step: increment fitness, remove dead
        for i, car_grp in enumerate(cars):
            genome = ge[i]
            genome.fitness += 1
            if not car_grp.sprite.alive:
                remove(i)

        # Activate nets and set directions
        for i, car_grp in enumerate(cars):
            output = nets[i].activate(car_grp.sprite.data())
            car_grp.sprite.direction = 1 if output[0] > 0.7 else (-1 if output[1] > 0.7 else 0)

        # Update & draw cars
        for car_grp in cars:
            car_grp.draw(SCREEN)
            car_grp.update()

        # Draw stats
        elapsed = time.time() - start_time
        stats_text = [
            FONT.render(f'Cars: {len(cars)}', True, (0,0,0)),
            FONT.render(f'Generation: {pop.generation + 1}', True, (0,0,0)),
            FONT.render(f'Time Left: {round(TIME_LIMIT - elapsed, 2)}s', True, (0,0,0)),
        ]
        for idx, txt in enumerate(stats_text):
            SCREEN.blit(txt, (50, 50 + idx*30))

        pygame.display.set_caption(f"Time Left: {round(TIME_LIMIT - elapsed, 2)}s")
        pygame.display.update()

# NEAT run setup
def run(config_path):
    global pop, config
    # Load configuration
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    cfg_path = os.path.join(local_dir, 'config.txt')
    run(cfg_path)
