import pygame as py
import neat
import time
import argparse
import os
import random


WIN_WIDTH = 570
WIN_HEIGHT = 720

BIRD_IMG = [py.transform.scale2x(py.image.load(os.path.join("imgs", "bird1.png"))),
            py.transform.scale2x(py.image.load(os.path.join("imgs", "bird2.png"))),
            py.transform.scale2x(py.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "base.png")))
BG_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "bg.png")))

# Font initialized later when pygame is ready
STAT_FONT = None
GEN = 0

class Bird:
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2
        
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if   self.img_count < self.ANIMATION_TIME:
             self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]       
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = py.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return py.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = py.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = py.mask.from_surface(self.PIPE_TOP)
        bottom_mask = py.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, birds, pipes, base, score=0, gen=0):
    global STAT_FONT
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    # draw all birds (or a single bird)
    if isinstance(birds, list):
        for bird in birds:
            bird.draw(win)
    else:
        birds.draw(win)

    # init font lazily
    if STAT_FONT is None:
        py.font.init()
        STAT_FONT = py.font.SysFont("comicsans", 50)

    # score and generation
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))

    gen_label = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(gen_label, (10, 10))

    py.display.update()

def main():
    # simple human-playable version (kept for convenience)
    py.init()
    global STAT_FONT
    py.font.init()
    STAT_FONT = py.font.SysFont("comicsans", 50)

    bird = Bird(200, 200)
    base = Base(700)
    pipes = [Pipe(700)]
    win = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = py.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(45)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    bird.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 700:
            pass

        base.move()
        bird.move()
        draw_window(win, bird, pipes, base, score)

    py.quit()
    quit()


def eval_genomes(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200, 200))
        g.fitness = 0
        ge.append(g)

    win = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = py.time.Clock()

    base = Base(700)
    pipes = [Pipe(700)]
    score = 0

    run = True
    while run and len(birds) > 0:
        clock.tick(45)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        rem = []
        add_pipe = False

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            # inputs: bird y, distance to top pipe, distance to bottom pipe
            top_dist = abs(bird.y - pipes[pipe_ind].height)
            bottom_dist = abs(bird.y - pipes[pipe_ind].bottom)
            output = nets[x].activate((bird.y / WIN_HEIGHT, top_dist / WIN_HEIGHT, bottom_dist / WIN_HEIGHT))
            if output[0] > 0.5:
                bird.jump()

        for pipe in pipes:
            pipe.move()
            to_remove = []
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    to_remove.append(i)
            # remove collided birds in reverse order to keep indices valid
            for i in sorted(to_remove, reverse=True):
                nets.pop(i)
                ge.pop(i)
                birds.pop(i)
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if len(birds) > 0 and not pipe.passed and pipe.x < birds[0].x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        # check ground / ceiling collisions
        to_remove = []
        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 700 or bird.y < 0:
                ge[i].fitness -= 1
                to_remove.append(i)
        for i in sorted(to_remove, reverse=True):
            nets.pop(i)
            ge.pop(i)
            birds.pop(i)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path, target_score=None, max_generations=0):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # If no target_score specified, fall back to fixed 50 generations
    if target_score is None:
        p.run(eval_genomes, 50)
        return p, stats

    gen = 0
    best_fitness = float("-inf")
    # run one generation at a time until target reached or max_generations hit
    while True:
        gen += 1
        p.run(eval_genomes, 1)
        # compute best fitness among current population
        best_fitness = max((g.fitness if g.fitness is not None else float("-inf") for g in p.population.values()), default=float("-inf"))
        print(f"After generation {gen}: best fitness = {best_fitness}")
        if best_fitness >= target_score:
            print(f"Target score {target_score} reached at generation {gen}!")
            break
        if max_generations and gen >= max_generations:
            print(f"Reached max generations ({max_generations}) without hitting target.")
            break

    return p, stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flappy Birb NEAT runner")
    parser.add_argument("--human", action="store_true", help="Run human-playable main() instead of NEAT")
    parser.add_argument("--target-score", type=float, default=None, help="Target score to run generations until reached")
    parser.add_argument("--max-gens", type=int, default=0, help="Maximum generations to run when using --target-score (0 = unlimited)")
    args = parser.parse_args()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")

    if args.human:
        main()
    else:
        run(config_path, target_score=args.target_score, max_generations=args.max_gens)