# Project Documentation

## 1. Overview

Flappy Birb AI is a desktop game built with Python and Pygame. It supports
traditional keyboard play and an evolutionary AI mode. The AI uses the
NEAT-Python library to evolve feed-forward neural networks that decide when a
bird should jump.

The application is intentionally self-contained: game code is in
`Flappy_birb_AI.py`, neural-network settings are in
`config_feedforward.txt`, and visual resources are stored in `imgs/`.

## 2. Runtime architecture

### Entry point

`Flappy_birb_AI.py` is the application entry point. It parses command-line
arguments and selects one of two modes:

- `--human` calls `main()`.
- Without `--human`, the program calls `run()` and starts NEAT training.

The configuration path is built relative to the script location, so the NEAT
configuration is found regardless of the caller's current directory. The image
paths are relative to the current working directory; running from the project
root is therefore recommended.

### Game entities

#### `Bird`

`Bird` stores position, velocity, tilt, animation state, and the current sprite.
Its `jump()` method applies upward velocity. Its `move()` method applies
gravity-like movement and updates rotation. Collision masks are generated from
the current sprite.

#### `Pipe`

`Pipe` creates a top and bottom obstacle separated by a fixed gap. It moves
horizontally at a constant velocity and uses pixel masks to detect collisions
with birds. A pipe is marked as passed once it moves beyond the bird.

#### `Base`

`Base` draws two copies of the ground image and loops them horizontally to
create a scrolling effect.

#### `draw_window()`

This function renders the background, pipes, base, birds, score, and generation
number, then updates the Pygame display.

## 3. Human mode

Human mode creates one bird, one initial pipe, and a Pygame event loop running
at 45 frames per second. The player presses Space to call `Bird.jump()`.
Pipes are removed after leaving the screen, and a new pipe is added after the
bird passes the current pipe.

The current loop preserves the original game's behavior for collisions and
ground contact. Those conditions are detected, but the human mode does not
currently terminate or reset the run automatically.

## 4. NEAT mode

`run()` creates a `neat.Population` from `config_feedforward.txt`, attaches
standard output and statistics reporters, and evaluates genomes through
`eval_genomes()`.

Each generation:

1. Creates one `Bird` and one neural network for each genome.
2. Resets each genome's fitness.
3. Advances the simulation at 45 frames per second.
4. Activates each network with three normalized inputs.
5. Makes the bird jump when the network output exceeds `0.5`.
6. Removes birds that collide with pipes or leave the play area.
7. Rewards survival and successfully passing pipes.
8. Evolves the population through NEAT.

When `--target-score` is omitted, training runs for 50 generations. When it is
provided, training runs one generation at a time until the target is reached or
`--max-gens` is reached. A maximum generation value of `0` means unlimited
generations in target-score mode.

## 5. Neural-network inputs and fitness

The network has three inputs and one output, as defined in the NEAT
configuration:

| Input | Meaning |
| --- | --- |
| `bird.y / WIN_HEIGHT` | Normalized vertical position |
| `top_dist / WIN_HEIGHT` | Normalized distance to the top pipe |
| `bottom_dist / WIN_HEIGHT` | Normalized distance to the bottom pipe |

The output is interpreted as a jump decision:

```text
output[0] > 0.5  ->  jump
output[0] <= 0.5 ->  do not jump
```

Fitness changes are:

- `+0.1` each simulation frame survived.
- `+5` for each pipe passed.
- `-1` for a pipe collision.
- `-1` for hitting the ceiling or ground.

## 6. Configuration reference

`config_feedforward.txt` controls population and genome behavior. Important
settings include:

- `pop_size`: number of genomes per generation.
- `fitness_threshold`: fitness at which NEAT may stop.
- `num_inputs`: must remain `3` unless the input code changes.
- `num_outputs`: must remain `1` unless the decision logic changes.
- `activation_default`: activation function for network nodes.
- `conn_add_prob` and `conn_delete_prob`: connection mutation rates.
- `node_add_prob` and `node_delete_prob`: node mutation rates.
- `max_stagnation`: generations a species may remain stagnant.

If the number of inputs or outputs is changed, `eval_genomes()` must be updated
at the same time so the network input tuple and output handling remain
consistent.

## 7. Asset requirements

The `imgs/` directory must contain:

- `bg.png`: background.
- `base.png`: scrolling ground.
- `pipe.png`: pipe sprite.
- `bird1.png`, `bird2.png`, `bird3.png`: animation frames.

Sprites are loaded when the module starts and scaled with
`pygame.transform.scale2x`. Missing or unreadable assets prevent the program
from starting.

## 8. Development and validation

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

Run the human mode as a smoke test:

```bash
python Flappy_birb_AI.py --human
```

Run a short AI smoke test:

```bash
python Flappy_birb_AI.py --target-score 100 --max-gens 1
```

The game opens a graphical window in both modes, so validation requires a
desktop session or a configured SDL display environment.

## 9. Extension ideas

- Add automatic reset and game-over behavior to human mode.
- Add a headless training option for faster evolution.
- Save and load winning genomes.
- Add command-line controls for population size and frame rate.
- Add automated tests for physics, pipe generation, and collision handling.
- Add a project license and contribution guidelines.
