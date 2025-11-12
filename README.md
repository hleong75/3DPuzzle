# 3D Puzzle Generator

A tool to transform complete 3D objects into interlocking 3D puzzles ready for wood manufacturing. Creates UGEARS-style mechanical wooden puzzles with proper tolerances and interlocking mechanisms.

## Features

- 🧩 **3D Puzzle Generation**: Converts any 3D model (STL, OBJ) into interlocking puzzle pieces
- 🔧 **Manufacturing Ready**: Includes proper tolerances for laser cutting or CNC machining
- 🪵 **Wood Optimized**: Configurable for different wood thicknesses and material properties
- 🔗 **Interlocking Mechanism**: Automatic generation of tabs and slots for piece assembly
- 📦 **Multiple Export Formats**: Supports STL and DXF export formats
- ⚙️ **Highly Configurable**: Adjust number of pieces, slice direction, tolerances, and more

## Installation

### From Source

```bash
git clone https://github.com/hleong75/3DPuzzle.git
cd 3DPuzzle
pip install -e .
```

### Requirements

- Python 3.8 or higher
- numpy
- trimesh
- numpy-stl
- scipy

## Quick Start

### Basic Usage

```bash
# Generate a 10-piece puzzle from a 3D model
puzzle3d input.stl -o output/

# Generate with custom number of pieces
puzzle3d input.obj -o output/ --slices 15

# Adjust for thicker material (5mm plywood)
puzzle3d input.stl -o output/ --material-thickness 5.0 --tolerance 0.3
```

### Python API

```python
from puzzle3d import PuzzleGenerator, PuzzleConfig

# Create configuration
config = PuzzleConfig()
config.num_slices = 12
config.material_thickness = 3.0
config.tolerance = 0.2

# Generate puzzle
generator = PuzzleGenerator(config)
pieces = generator.generate_from_file('model.stl', 'output/')
```

## Configuration Options

### Slicing Options

- `--slices`: Number of pieces to generate (default: 10)
- `--slice-direction`: Direction to slice (x, y, or z) (default: z)

### Material Options

- `--material-thickness`: Material thickness in mm (default: 3.0)
- `--tolerance`: Tolerance for interlocking parts in mm (default: 0.2)
- `--kerf-width`: Laser/saw blade width in mm (default: 0.1)

### Interlocking Options

- `--tab-width`: Width of interlocking tabs in mm (default: 5.0)
- `--tab-depth`: Depth of interlocking tabs in mm (default: 1.5)
- `--tab-spacing`: Spacing between tabs in mm (default: 15.0)

### Output Options

- `--format`: Output format (stl or dxf) (default: stl)
- `--combined`: Export all pieces in a single file

## How It Works

1. **Load 3D Model**: Imports STL, OBJ, or other 3D model formats
2. **Slice Model**: Divides the model into sections along specified axis
3. **Generate Interlocking**: Adds tabs to one face and matching slots to adjacent faces
4. **Apply Tolerances**: Accounts for material thickness and manufacturing tolerances
5. **Export**: Saves individual pieces or combined assembly

## Examples

### Example 1: Simple Cube Puzzle

```bash
puzzle3d examples/cube.stl -o output/cube/ --slices 6
```

This creates a 6-piece interlocking cube puzzle.

### Example 2: Complex Model with Custom Settings

```bash
puzzle3d model.stl -o output/ \
  --slices 20 \
  --material-thickness 4.0 \
  --tolerance 0.25 \
  --tab-width 6.0 \
  --slice-direction y
```

### Example 3: For Thin Plywood

```bash
puzzle3d model.obj -o output/ \
  --material-thickness 2.0 \
  --tolerance 0.15 \
  --tab-depth 1.0
```

## Manufacturing Tips

1. **Material Selection**: Use hardwood plywood (birch, maple) for best results
2. **Laser Cutting**: Account for kerf width in your tolerance settings
3. **Test Fit**: Always test with a small piece first to verify tolerances
4. **Finishing**: Sand lightly and apply wood finish for smoother assembly
5. **Assembly**: Pieces should fit snugly but not require excessive force

## Recommended Settings by Material

### 3mm Baltic Birch Plywood
```bash
--material-thickness 3.0 --tolerance 0.2 --tab-depth 1.5
```

### 5mm MDF
```bash
--material-thickness 5.0 --tolerance 0.3 --tab-depth 2.0
```

### 2mm Basswood
```bash
--material-thickness 2.0 --tolerance 0.15 --tab-depth 1.0
```

## Troubleshooting

**Pieces don't fit together**
- Increase tolerance value (try +0.1mm increments)
- Check if kerf-width is properly set for your cutting method

**Tabs break easily**
- Increase tab-width
- Reduce tab-depth
- Use harder wood material

**Model doesn't slice properly**
- Ensure input model is a closed, manifold mesh
- Try a different slice-direction
- Check that model is properly scaled (in mm)

## Project Structure

```
3DPuzzle/
├── puzzle3d/           # Main package
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── config.py       # Configuration settings
│   ├── puzzle_generator.py  # Main generator
│   ├── slicer.py       # 3D slicing logic
│   └── interlocking.py # Tab/slot generation
├── tests/              # Unit tests
├── examples/           # Example models
├── setup.py            # Package setup
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Inspired by UGEARS mechanical wooden puzzles and other wooden construction kits.