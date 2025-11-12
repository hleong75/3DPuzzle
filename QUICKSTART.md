# Quick Start Guide

Get started with 3D Puzzle Generator in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/hleong75/3DPuzzle.git
cd 3DPuzzle

# Install the package
pip install -e .
```

## Your First Puzzle

### Step 1: Verify Installation

```bash
puzzle3d --help
```

You should see the help text with all available options.

### Step 2: Generate a Simple Puzzle

Try it with one of the included examples:

```bash
puzzle3d examples/cube.stl -o my_first_puzzle/
```

This creates a 10-piece puzzle in the `my_first_puzzle/` directory.

### Step 3: View Your Puzzle

Open the generated STL files in any 3D viewer:
- **Windows**: 3D Builder, MeshLab, Blender
- **Mac**: Preview (for STL), MeshLab, Blender
- **Linux**: MeshLab, Blender
- **Online**: [ViewSTL.com](https://www.viewstl.com)

Check out:
- Individual pieces: `cube_001.stl`, `cube_002.stl`, etc.
- Assembly view: `cube_assembly.stl`

## Customize Your Puzzle

### More Pieces

```bash
puzzle3d examples/sphere.stl -o sphere_puzzle/ --slices 15
```

### Different Slice Direction

```bash
puzzle3d examples/cylinder.stl -o cylinder_puzzle/ --slice-direction y
```

### Adjust for Your Material

For 5mm plywood:
```bash
puzzle3d examples/torus.stl -o torus_puzzle/ \
  --material-thickness 5.0 \
  --tolerance 0.3 \
  --tab-depth 2.0
```

## Use Your Own 3D Model

```bash
puzzle3d your_model.stl -o output/
```

**Requirements for your model:**
- Format: STL or OBJ
- Should be a closed, manifold mesh
- Reasonable size (10-200mm recommended)

## Run the Demo

See all features in action:

```bash
python demo.py
```

This generates 5 different example puzzles with various configurations.

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--slices N` | Number of pieces | `--slices 12` |
| `--slice-direction` | Slice axis | `--slice-direction y` |
| `--material-thickness` | Material in mm | `--material-thickness 3.0` |
| `--tolerance` | Fit tolerance in mm | `--tolerance 0.2` |
| `--tab-width` | Tab width in mm | `--tab-width 5.0` |
| `--combined` | Export as single file | `--combined` |

## Next Steps

1. **Read the full documentation**: [README.md](README.md)
2. **See more examples**: [EXAMPLES.md](EXAMPLES.md)
3. **Adjust tolerances** for your cutting method
4. **Test with scrap material** before final cuts
5. **Share your creations**!

## Troubleshooting

**"No module named 'puzzle3d'"**
- Run `pip install -e .` from the project directory

**Pieces don't fit**
- Increase `--tolerance` by 0.05mm increments
- Check your cutting method's kerf width

**Model doesn't slice**
- Ensure your model is a closed mesh
- Try a different `--slice-direction`

## Get Help

- Full documentation: [README.md](README.md)
- Detailed examples: [EXAMPLES.md](EXAMPLES.md)
- Project summary: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

Happy puzzling! 🧩
