# Social Attraction & Clustering Simulation

A Python-based physics simulation that demonstrates how social networks naturally form clusters based on attraction and repulsion forces. This project visualizes how individuals in a social network are drawn together by their connections while being pushed apart from unconnected individuals.

## 🎯 Core Concept

The simulation models a social network where:
- **Connected individuals** (friends, colleagues, family) are attracted to each other
- **Unconnected individuals** repel each other when they get too close
- This creates natural clustering behavior where social groups form and maintain their cohesion

## 🛠️ Technologies Used

- **Python 3.7+**: Core programming language
- **Pymunk**: 2D physics engine (Pythonic wrapper around Chipmunk2D)
- **Pygame**: Graphics and window management
- **Math/Physics**: Custom force calculations for social dynamics

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install pygame pymunk
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

## 🚀 Running the Simulation

### Basic Usage
```bash
python main.py
```

### Controls
- **Mouse Drag**: Click and drag nodes to move them around
- **R Key**: Reset the simulation with new random positions
- **ESC Key**: Quit the simulation

## 🎮 Features

### Physics Simulation
- **Attraction Forces**: Connected nodes pull each other together
- **Repulsion Forces**: Unconnected nodes push each other apart
- **Realistic Physics**: Collision detection, friction, and damping
- **Interactive Nodes**: Drag nodes with mouse to see how forces respond

### Network Visualization
- **Nodes**: Represent individuals in the social network
- **Connections**: Lines showing social relationships
- **Node Labels**: ID numbers displayed above each node
- **Real-time Updates**: Forces and positions update continuously

### Social Network Models
The simulation includes several pre-built network structures:

1. **Basic Social Network** (default): 15 individuals in 3 groups with cross-group connections
2. **Large Random Network**: Configurable size with group-based connection probabilities
3. **Clique Network**: Distinct social cliques with bridge connections

## 📊 Understanding the Simulation

### Force Dynamics
- **Attraction**: `F = attraction_force * (distance - min_distance) / scale_factor`
- **Repulsion**: `F = repulsion_force * (max_distance - distance) / max_distance`
- **Damping**: Velocity gradually decreases to prevent infinite oscillation

### Clustering Behavior
1. **Initial State**: Nodes start in random positions
2. **Force Application**: Attraction and repulsion forces are calculated each frame
3. **Natural Clustering**: Connected groups gradually move together
4. **Stable Formation**: Groups reach equilibrium positions

### Parameters
You can adjust these parameters in `main.py`:
- `attraction_force`: Strength of attraction between connected nodes
- `repulsion_force`: Strength of repulsion between unconnected nodes
- `repulsion_distance`: Maximum distance for repulsion effects
- `damping`: Velocity damping factor (0.98 = 2% loss per frame)

## 🔧 Customization

### Adding New Networks
Edit `social_network_data.py` to create custom network structures:

```python
def create_custom_network():
    nodes = [
        {'id': 1, 'name': 'Person1', 'group': 'A'},
        # ... more nodes
    ]
    
    connections = [
        {'from': 1, 'to': 2, 'strength': 'strong'},
        # ... more connections
    ]
    
    return {'nodes': nodes, 'connections': connections}
```

### Modifying Physics
Adjust force calculations in `main.py`:

```python
# In apply_social_forces method
if is_connected:
    # Custom attraction formula
    force_magnitude = self.attraction_force * math.log(distance)
else:
    # Custom repulsion formula
    force_magnitude = self.repulsion_force / (distance ** 2)
```

## 🎨 Visual Customization

### Colors and Styling
- Background: Dark gray `(30, 30, 30)`
- Connection lines: Light gray `(100, 100, 100)`
- Node labels: White `(255, 255, 255)`
- UI text: Light gray `(200, 200, 200)`

### Window Settings
- Default size: 1200x800 pixels
- Frame rate: 60 FPS
- Fullscreen: Not supported (but easily modifiable)

## 🔬 Educational Applications

This simulation is useful for:
- **Social Network Analysis**: Understanding clustering in real networks
- **Physics Education**: Learning about force-based systems
- **Computer Science**: Algorithm visualization and optimization
- **Psychology/Sociology**: Modeling social behavior patterns

## 🐛 Troubleshooting

### Common Issues

**"pygame module not found"**
```bash
pip install pygame
```

**"pymunk module not found"**
```bash
pip install pymunk
```

**Performance Issues**
- Reduce the number of nodes in the network
- Increase the damping factor
- Lower the frame rate

**Visual Glitches**
- Ensure your graphics drivers are up to date
- Try running in a different resolution

## 📈 Future Enhancements

Potential improvements and extensions:
- [ ] Multiple network layouts (circular, grid, etc.)
- [ ] Dynamic network changes (add/remove connections)
- [ ] Color-coded nodes by group
- [ ] Force strength visualization
- [ ] Network metrics display (clustering coefficient, etc.)
- [ ] Export functionality (screenshots, data)
- [ ] Web-based version using Pygame-web

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Performance optimization
- Additional network models
- Enhanced visualization features
- Educational documentation
- Bug fixes and testing

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Pymunk**: Excellent Python physics library
- **Pygame**: Great graphics library for Python
- **Chipmunk2D**: The underlying physics engine

---

**Enjoy exploring social dynamics through physics simulation!** 🎮✨ 