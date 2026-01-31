# Neural Evolution Simulation

A visual simulation demonstrating evolution through genetic algorithms and neural networks, where creatures learn to navigate obstacles and reach a target through natural selection over multiple generations.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0+-green.svg)
![NumPy](https://img.shields.io/badge/NumPy-Latest-orange.svg)

## 🎯 Overview

This project simulates a population of AI-controlled creatures that evolve navigation strategies using neural networks and genetic algorithms. Each creature has a "brain" (neural network) that processes visual input from raycasting sensors and outputs movement commands. Through evolutionary pressure, creatures develop increasingly sophisticated behaviors to reach targets while avoiding obstacles.

### Key Features

- **Neural Network Brains**: Each creature has a feedforward neural network with configurable architecture
- **Vision System**: Raycasting-based vision with adjustable field of view and range
- **Genetic Evolution**: Fitness-based selection, crossover, and mutation
- **Real-time Visualization**: Watch evolution happen in real-time with Pygame
- **Checkpointing**: Save and load the best-performing neural networks
- **Customizable Parameters**: Easily adjust population size, mutation rates, network architecture, and more

## 🧬 How It Works

### Neural Network Architecture

Each creature's brain is a feedforward neural network:

**Input Layer** (NUM_RAYS + 4 neurons):
- Vision rays (default: 4) - distance readings from raycasting
- Relative position to target (x, y)
- Current velocity (x, y)

**Hidden Layer**: 
- Configurable size (default: 10 neurons)
- tanh activation

**Output Layer** (2 neurons):
- Acceleration commands (x, y)
- tanh activation

### Genetic Algorithm

1. **Initialization**: Population starts with random neural network weights
2. **Simulation**: Each creature uses its neural network to navigate
3. **Fitness Evaluation**: Based on distance to target, with bonuses for success
4. **Selection**: Fitness-proportionate selection creates mating pool
5. **Crossover**: Parent networks combine to create offspring
6. **Mutation**: Random weight perturbations introduce variation
7. **Elitism**: Best performer automatically advances to next generation

### Vision System

Creatures perceive their environment through raycasting:
- Multiple rays cast within field of view (default: 60°, 4 rays)
- Each ray detects distance to nearest obstacle
- Closer obstacles = stronger signal (1.0 = very close, 0.0 = far)
- Vision data feeds directly into neural network

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/neural-evolution-sim.git
cd neural-evolution-sim

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# Run the simulation
python main.py
```

The simulation will start with a random population. Watch as creatures evolve better navigation strategies over generations!

## 🎮 Controls

| Key | Action |
|-----|--------|
| **SPACE** (hold) | Show only the best creature from current generation |
| **S** | Save the current best brain to `best_brain.npy` |
| **Close Window** | Exit simulation |

## ⚙️ Configuration

All parameters can be adjusted in `settings.py`:

### Display Settings
```python
WIDTH = 800          # Screen width
HEIGHT = 600         # Screen height
FPS = 90            # Frames per second
```

### Genetic Algorithm
```python
POPULATION_SIZE = 100           # Creatures per generation
MUTATION_RATE = 0.001          # Probability of weight mutation
GENERATION_FRAMES = 500        # Frames before next generation
ELITISM = True                 # Preserve best creature
```

### Creature Intelligence
```python
NUM_RAYS = 4                   # Number of vision rays
FOV = 60                       # Field of view (degrees)
VIEW_RANGE = 60                # Maximum vision distance
HIDDEN_SIZE = 10               # Hidden layer neurons
ACC_LIMIT = 5                  # Maximum acceleration
MAX_SPEED = 2                  # Maximum velocity
```

### Visual Style
```python
COLOR_BG = (15, 15, 20)               # Background
COLOR_CREATURE = (100, 100, 255)      # Normal creature
COLOR_CREATURE_BEST = (255, 255, 0)   # Best creature
COLOR_OBSTACLE = (40, 40, 45)         # Obstacles
COLOR_TARGET = (255, 200, 0)          # Target
```

## 📊 Evolution Dynamics

### Fitness Function

```python
distance_to_target = norm(creature.position - target.position)
base_fitness = interpolate(distance, [0, WIDTH], [1, 0])

if target_reached:
    fitness = 1.5                    # 50% bonus
elif out_of_bounds:
    fitness = base_fitness * 0.1     # 90% penalty
else:
    fitness = base_fitness²          # Squared for selection pressure
```

### Typical Evolution Timeline

- **Generations 1-10**: Random wandering, rare successes
- **Generations 10-30**: Movement toward target emerges
- **Generations 30-100**: Obstacle avoidance develops
- **Generations 100+**: Optimized pathfinding, high success rates

## 🏗️ Project Structure

```
neural-evolution-sim/
├── main.py              # Main simulation loop and rendering
├── creature.py          # Creature class with neural network
├── population.py        # Population management and evolution
├── obstacle.py          # Obstacle class with collision detection
├── target.py            # Target class with optional movement
├── helpers.py           # Utility functions (raycasting, etc.)
├── settings.py          # Configuration parameters
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔬 Advanced Usage

### Loading a Saved Brain

Place a saved neural network in `saved_brains/best_brain.npy`:

```python
# The simulation will automatically detect and load it
python main.py
# Console: "Loaded saved brain! Evolution will resume from this checkpoint."
```

### Saving During Runtime

Press **S** while the simulation is running to save the current best brain:

```python
# Saves to: best_brain.npy in the current directory
```

### Customizing the Environment

Modify `main.py` to change obstacle count or target behavior:

```python
# More obstacles
obstacles = [Obstacle(random=True) for _ in range(25)]

# Moving target
target = Target(move=True, random=False)

# Random target position each generation
target = Target(move=False, random=True)
```

## 🎨 Visual Indicators

| Color | Meaning |
|-------|---------|
| Blue | Active creature |
| Green | Reached target |
| Red | Collided with obstacle or boundary |
| Yellow | Best creature in current generation |

## 🧪 Experiments to Try

1. **Increase Vision Rays**: Set `NUM_RAYS = 8` for more detailed perception
2. **Larger Networks**: Increase `HIDDEN_SIZE = 20` for more complex behaviors
3. **Higher Mutation**: Try `MUTATION_RATE = 0.01` for faster but less stable evolution
4. **Sparse Population**: Reduce `POPULATION_SIZE = 50` to see individual strategies
5. **Moving Target**: Set `Target(move=True)` to evolve dynamic tracking
6. **Obstacle Maze**: Increase obstacle count to 30+ for complex navigation

## 🐛 Troubleshooting

**Issue**: Creatures don't improve over generations
- **Solution**: Increase `GENERATION_FRAMES` to give more time for fitness evaluation
- **Solution**: Decrease `MUTATION_RATE` if evolution is too chaotic

**Issue**: All creatures die immediately
- **Solution**: Check that `ACC_LIMIT` and `MAX_SPEED` are reasonable
- **Solution**: Reduce obstacle count or size

**Issue**: Simulation runs slowly
- **Solution**: Decrease `POPULATION_SIZE`
- **Solution**: Reduce `NUM_RAYS` or `VIEW_RANGE`
- **Solution**: Lower `FPS` in settings

## 📚 Technical Details

### Dependencies

- **pygame**: Graphics and simulation loop
- **numpy**: Numerical operations and neural network computations
- **numba**: JIT compilation for raycasting performance

### Neural Network Implementation

The brain is encoded as a flat array of genes (weights and biases):

```
genes = [Wih (input→hidden weights), 
         Bih (hidden biases),
         Who (hidden→output weights),
         Bho (output biases)]
```

This encoding allows for efficient genetic operations (crossover and mutation) on the entire network as a single genome.

### Raycasting Algorithm

Uses line-segment intersection to detect obstacles:
1. Cast rays from creature's "eye" position
2. For each ray, check intersection with all obstacle edges
3. Return fraction of ray length to closest intersection
4. Numba JIT compilation for real-time performance

## 🤝 Contributing

Contributions are welcome! Some ideas:

- Different neural network architectures (recurrent, attention-based)
- Alternative selection methods (tournament, rank-based)
- Visualization improvements (fitness graphs, genealogy trees)
- Performance optimizations
- Additional creature behaviors or sensors

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Inspired by evolutionary computation research and genetic algorithm visualizations. Built with Python, Pygame, NumPy, and Numba.

---

**Made with 🧬 and 🤖**