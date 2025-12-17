# Genetic Algorithm Evolution Simulation

A visual simulation demonstrating evolution through genetic algorithms, where creatures learn to navigate obstacles and reach a target through natural selection over multiple generations.

**Demo:** [YouTube Video](https://www.youtube.com/watch?v=deebMTNorQU&t=21s)

## Overview

Simulates a population of 5,000 creatures evolving movement strategies to reach a goal while avoiding obstacles. Uses genetic algorithm principles including fitness-based selection, crossover, and mutation to achieve 95%+ success rate over generations.

## How It Works

### Genetic Algorithm Components

- **Genes:** Each creature has a sequence of movement vectors (direction and magnitude)
- **Fitness Function:** Distance to target (closer = higher fitness), with bonus for reaching goal
- **Selection:** Fitness-proportionate selection creates mating pool
- **Crossover:** Two parent creatures combine genes to create offspring
- **Mutation:** Random gene alterations introduce variation
- **Elitism:** Best creature from each generation is preserved

### Simulation Details

- **Population:** 5,000 creatures per generation
- **Environment:** 3 obstacles between start and target
- **Success Criteria:** Creatures must navigate obstacles to reach yellow target zone
- **Visualization:** Real-time display of evolution progress with generation count and success rate

## Features

- Real-time visualization using Pygame
- Adjustable parameters (population size, mutation rate, gene length)
- Obstacle collision detection
- Fitness-based color coding (successful creatures appear different)
- Press **SPACE** to show only the best-performing creature
- Generation statistics display

## Controls

- **SPACE (hold):** Show only the best creature from current generation
- **Close window:** Exit simulation

## Installation & Usage

```bash
# Clone the repository
git clone https://github.com/yourusername/genetic-algorithm-simulation.git
cd genetic-algorithm-simulation

# Install dependencies
pip install pygame

# Run simulation
python main.py
```

## Results

The simulation demonstrates emergent intelligent behavior through evolution:
- Early generations show random, chaotic movement
- Fitness pressure gradually favors creatures moving toward target
- Later generations efficiently navigate obstacles
- Achieves 95%+ success rate after sufficient generations

## Technical Implementation

**Python** | **Pygame** | **Genetic Algorithms**

### Key Classes

- `Creature` - Individual agent with genes (movement vectors), position, and fitness calculation
- `Obstacle` - Rectangular barriers with collision detection
- Main loop handles generation cycling, mating pool creation, and visualization

### Genetic Operations

```python
# Fitness-proportionate selection
mating_pool = creatures × (fitness / total_fitness)

# Crossover: combine parent genes
child.genes = parentA.genes[:split] + parentB.genes[split:]

# Mutation: random gene modification
if random() < mutation_rate:
    gene = random_vector()
```

## Parameters

Adjustable in `main.py`:
- `populationSize = 5000` - Number of creatures per generation
- `GENE_SIZE` - Length of gene sequence (defined in creature.py)
- `dt` - Time step for gene activation
- `FPS = 30` - Simulation frame rate
- Mutation rate (in `creature.py`)

## Future Improvements

- Dynamic obstacle generation
- Variable target positions
- Performance metrics visualization (fitness over time)
- Configurable mutation and crossover rates via UI
- Save/load best creature genomes
