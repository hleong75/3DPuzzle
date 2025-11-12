# Usage Examples for 3D Puzzle Generator

This document provides detailed examples of using the 3D Puzzle Generator tool.

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Advanced Examples](#advanced-examples)
3. [Python API Examples](#python-api-examples)
4. [Tips and Best Practices](#tips-and-best-practices)

## Basic Usage

### Example 1: Simple Cube Puzzle

Generate a basic 5-piece puzzle from a cube:

```bash
puzzle3d examples/cube.stl -o output/cube/
```

This creates:
- 5 interlocking pieces
- Default 3mm material thickness
- 0.2mm tolerance
- Slicing along Z-axis

### Example 2: Custom Number of Pieces

Create a 12-piece puzzle:

```bash
puzzle3d examples/sphere.stl -o output/sphere/ --slices 12
```

### Example 3: Different Slice Direction

Slice along Y-axis instead of Z:

```bash
puzzle3d examples/cylinder.stl -o output/cylinder/ --slice-direction y
```

## Advanced Examples

### Example 4: Thick Material (5mm Plywood)

For thicker materials, adjust material thickness and tolerances:

```bash
puzzle3d model.stl -o output/ \
  --material-thickness 5.0 \
  --tolerance 0.3 \
  --tab-depth 2.0
```

### Example 5: Fine Precision (Thin Wood)

For thin materials requiring precise fit:

```bash
puzzle3d model.stl -o output/ \
  --material-thickness 2.0 \
  --tolerance 0.15 \
  --tab-depth 1.0 \
  --tab-width 4.0
```

### Example 6: Laser Cutting Optimization

Account for laser kerf (material removed by laser):

```bash
puzzle3d model.stl -o output/ \
  --kerf-width 0.15 \
  --tolerance 0.25
```

### Example 7: Large Puzzle with Many Pieces

Create a complex 20-piece puzzle:

```bash
puzzle3d model.obj -o output/ \
  --slices 20 \
  --tab-spacing 12.0 \
  --slice-direction x
```

### Example 8: Export as Single File

Export all pieces in one file for easy loading:

```bash
puzzle3d model.stl -o output/ --combined
```

## Python API Examples

### Example 9: Basic API Usage

```python
from puzzle3d import PuzzleGenerator

# Create generator with defaults
generator = PuzzleGenerator()

# Generate puzzle
pieces = generator.generate_from_file('model.stl', 'output/')
```

### Example 10: Custom Configuration

```python
from puzzle3d import PuzzleGenerator, PuzzleConfig

# Create custom configuration
config = PuzzleConfig()
config.num_slices = 8
config.material_thickness = 4.0
config.tolerance = 0.25
config.tab_width = 6.0
config.slice_direction = 'y'

# Generate puzzle with custom config
generator = PuzzleGenerator(config)
pieces = generator.generate_from_file('model.stl', 'output/')
```

### Example 11: Load and Process Separately

```python
from puzzle3d import PuzzleGenerator, PuzzleConfig

config = PuzzleConfig()
config.num_slices = 10

generator = PuzzleGenerator(config)

# Load model
mesh = generator.load_model('input.stl')

# Generate puzzle pieces
pieces = generator.generate_puzzle(mesh)

# Export pieces
generator.export_pieces(pieces, 'output/', 'my_puzzle')
```

### Example 12: Batch Processing

```python
from puzzle3d import PuzzleGenerator, PuzzleConfig
import os

# Configuration for all puzzles
config = PuzzleConfig()
config.num_slices = 6
config.material_thickness = 3.0

generator = PuzzleGenerator(config)

# Process multiple files
input_files = ['model1.stl', 'model2.stl', 'model3.stl']

for input_file in input_files:
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = f'output/{base_name}/'
    
    print(f"Processing {input_file}...")
    generator.generate_from_file(input_file, output_dir)
```

## Tips and Best Practices

### Choosing Number of Slices

- **Small models (< 50mm)**: 3-5 pieces
- **Medium models (50-150mm)**: 6-12 pieces
- **Large models (> 150mm)**: 12-20+ pieces

### Material Selection

**Recommended woods:**
- Baltic Birch Plywood (3mm, 5mm)
- Maple veneer plywood
- Basswood sheets
- MDF (for prototyping)

**Avoid:**
- Very soft woods (pieces may break)
- Wood with large grain (can split along grain)

### Tolerance Guidelines

| Cutting Method | Recommended Tolerance |
|----------------|----------------------|
| Laser cutting  | 0.15 - 0.25mm       |
| CNC milling    | 0.2 - 0.3mm         |
| Manual sawing  | 0.3 - 0.5mm         |

### Tab Sizing

- **Tab width**: Should be 2-3x material thickness
- **Tab depth**: Should be 40-60% of material thickness
- **Tab spacing**: 10-20mm depending on piece size

### Testing Your Settings

1. Start with default settings
2. Generate a simple test puzzle (cube with 3-5 pieces)
3. Cut and test fit
4. Adjust tolerance based on results:
   - Too tight? Increase tolerance by 0.05mm
   - Too loose? Decrease tolerance by 0.05mm
5. Once happy, apply settings to your actual project

### Slice Direction Tips

- **Z-axis (default)**: Best for models that are wider than tall
- **Y-axis**: Good for models with front-to-back detail
- **X-axis**: Use for side-to-side assembly

Choose the direction that:
1. Creates roughly equal-sized pieces
2. Respects the model's natural structure
3. Results in interesting piece shapes

### Export Format Selection

- **STL**: Best for 3D viewing and general use
- **DXF**: Better for laser cutters and CNC machines (coming soon)

### Common Issues and Solutions

**Issue**: Pieces don't fit together
- **Solution**: Increase `--tolerance` value

**Issue**: Tabs break easily
- **Solution**: Increase `--tab-width` or decrease `--tab-depth`

**Issue**: Model doesn't slice properly
- **Solution**: Ensure input is a manifold (closed) mesh, try different `--slice-direction`

**Issue**: Too many/few tabs per piece
- **Solution**: Adjust `--tab-spacing` value

## Real-World Example: UGEARS-Style Mechanical Puzzle

```bash
# Create a professional-quality wooden puzzle
puzzle3d mechanical_owl.stl -o output/owl_puzzle/ \
  --slices 15 \
  --material-thickness 3.0 \
  --tolerance 0.2 \
  --tab-width 5.0 \
  --tab-depth 1.5 \
  --tab-spacing 12.0 \
  --slice-direction z
```

This creates a 15-piece interlocking puzzle optimized for:
- 3mm Baltic Birch plywood
- Laser cutting with standard kerf
- UGEARS-style fit and finish
- Professional appearance

## Next Steps

After generating your puzzle:

1. **Inspect the pieces**: Open the STL files in a 3D viewer
2. **Optimize layout**: Arrange pieces efficiently for cutting
3. **Add labels**: Consider numbering pieces for assembly
4. **Create instructions**: Document assembly order
5. **Test cut**: Always do a test run on scrap material
6. **Finish pieces**: Sand, stain, or seal as desired

For more information, see the main [README.md](README.md) file.
