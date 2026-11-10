# Flappy Birb AI

Flappy Birb AI is a Pygame implementation of Flappy Bird that can be played
manually or controlled by a population of neural networks evolved with
[NEAT](https://neat-python.readthedocs.io/).

## Features

- Human-playable Flappy Bird mode.
- NEAT-based AI training mode.
- Configurable target fitness and generation limit.
- Sprite-based bird animation, pipes, background, and scrolling ground.
- Fitness rewards for survival and passing pipes.

## Requirements

- Python 3.9 or newer
- The packages listed in [`requirements.txt`](requirements.txt)

## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/Usman-Shah-Rashdi/Flappy_BIrd_Ai.git
   cd Flappy_BIrd_Ai
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

### Human-playable mode

Run the game with keyboard controls:

```bash
python Flappy_birb_AI.py --human
```

Press **Space** to make the bird jump. Close the game window to exit.

### NEAT training mode

Run the default training session:

```bash
python Flappy_birb_AI.py
```

The default configuration uses a population of 20 genomes and runs for 50
generations when no target score is supplied.

Stop after reaching a target fitness:

```bash
python Flappy_birb_AI.py --target-score 100
```

Limit the number of generations while pursuing a target:

```bash
python Flappy_birb_AI.py --target-score 100 --max-gens 200
```

`--max-gens 0` means no generation limit when `--target-score` is used.

## Project structure

```text
.
├── Flappy_birb_AI.py       # Game, physics, and NEAT training logic
├── config_feedforward.txt  # NEAT population and genome configuration
├── requirements.txt        # Python dependencies
├── imgs/                   # Game sprites and background assets
└── docs/
    └── PROJECT_DOCUMENTATION.md
```

## How the AI works

Each genome controls one bird through a feed-forward neural network with three
inputs:

1. Normalized bird Y position.
2. Normalized distance to the top pipe.
3. Normalized distance to the bottom pipe.

If the network output is greater than `0.5`, the bird jumps. A genome receives
small rewards for staying alive and larger rewards for passing pipes, while
collisions and leaving the play area reduce fitness.

The NEAT configuration can be adjusted in
[`config_feedforward.txt`](config_feedforward.txt), including population size,
mutation rates, fitness threshold, and network topology.

## Troubleshooting

- Run commands from the repository root so the `imgs/` directory can be found.
- If a module is missing, activate the virtual environment and rerun
  `python -m pip install -r requirements.txt`.
- If the display does not open on a headless machine, use a local desktop
  environment or configure an appropriate SDL video driver.

## License

No license file is currently included. Add a license before distributing the
project or its assets.
