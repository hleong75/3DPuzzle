#!/usr/bin/env python3
"""
Demo script to showcase the 3D Puzzle Generator capabilities.
"""

import os
import sys
from puzzle3d import PuzzleGenerator, PuzzleConfig

def demo_basic():
    """Demo 1: Basic puzzle generation with defaults."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Puzzle Generation")
    print("="*70)
    
    generator = PuzzleGenerator()
    pieces = generator.generate_from_file('examples/cube.stl', 'output/demo1_basic/')
    
    print(f"\n✓ Generated {len(pieces)} pieces with default settings")
    print("  Check output/demo1_basic/ for results")


def demo_custom_slices():
    """Demo 2: Custom number of slices."""
    print("\n" + "="*70)
    print("DEMO 2: Custom Number of Slices (15 pieces)")
    print("="*70)
    
    config = PuzzleConfig()
    config.num_slices = 15
    
    generator = PuzzleGenerator(config)
    pieces = generator.generate_from_file('examples/sphere.stl', 'output/demo2_slices/')
    
    print(f"\n✓ Generated {len(pieces)} pieces from sphere")
    print("  Check output/demo2_slices/ for results")


def demo_different_directions():
    """Demo 3: Slicing in different directions."""
    print("\n" + "="*70)
    print("DEMO 3: Different Slice Directions")
    print("="*70)
    
    for direction in ['x', 'y', 'z']:
        config = PuzzleConfig()
        config.num_slices = 6
        config.slice_direction = direction
        
        generator = PuzzleGenerator(config)
        output_dir = f'output/demo3_{direction}_direction/'
        pieces = generator.generate_from_file('examples/cylinder.stl', output_dir)
        
        print(f"\n✓ {direction.upper()}-axis: Generated {len(pieces)} pieces")


def demo_material_variations():
    """Demo 4: Different material thicknesses."""
    print("\n" + "="*70)
    print("DEMO 4: Material Thickness Variations")
    print("="*70)
    
    materials = [
        ("2mm Basswood", 2.0, 0.15, 1.0),
        ("3mm Baltic Birch", 3.0, 0.2, 1.5),
        ("5mm MDF", 5.0, 0.3, 2.0),
    ]
    
    for name, thickness, tolerance, tab_depth in materials:
        config = PuzzleConfig()
        config.num_slices = 5
        config.material_thickness = thickness
        config.tolerance = tolerance
        config.tab_depth = tab_depth
        
        generator = PuzzleGenerator(config)
        output_dir = f'output/demo4_{thickness}mm/'
        pieces = generator.generate_from_file('examples/torus.stl', output_dir)
        
        print(f"\n✓ {name}: {len(pieces)} pieces")
        print(f"  Thickness: {thickness}mm, Tolerance: {tolerance}mm")


def demo_complex_model():
    """Demo 5: Complex model with fine-tuned settings."""
    print("\n" + "="*70)
    print("DEMO 5: Complex Model - Professional Settings")
    print("="*70)
    
    config = PuzzleConfig()
    config.num_slices = 12
    config.material_thickness = 3.0
    config.tolerance = 0.2
    config.tab_width = 5.0
    config.tab_depth = 1.5
    config.tab_spacing = 12.0
    config.slice_direction = 'z'
    
    generator = PuzzleGenerator(config)
    pieces = generator.generate_from_file('examples/sphere.stl', 'output/demo5_professional/')
    
    print(f"\n✓ Professional puzzle: {len(pieces)} pieces")
    print("  Settings optimized for laser-cut Baltic Birch")
    print("  UGEARS-style interlocking mechanism")


def print_summary():
    """Print summary of all demos."""
    print("\n" + "="*70)
    print("DEMO COMPLETE - SUMMARY")
    print("="*70)
    print("\nAll demo outputs have been generated in the 'output/' directory:")
    print("\n  1. output/demo1_basic/         - Basic puzzle with defaults")
    print("  2. output/demo2_slices/        - 15-piece sphere puzzle")
    print("  3. output/demo3_*_direction/   - Puzzles sliced in X, Y, Z directions")
    print("  4. output/demo4_*mm/           - Puzzles for different materials")
    print("  5. output/demo5_professional/  - Professional UGEARS-style puzzle")
    
    print("\n" + "="*70)
    print("To view the results:")
    print("  - Open .stl files in any 3D viewer (MeshLab, Blender, etc.)")
    print("  - Each directory contains individual pieces and an assembly view")
    print("  - Try different settings to find what works best for your project!")
    print("="*70 + "\n")


def main():
    """Run all demos."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                    3D PUZZLE GENERATOR - DEMO                      ║")
    print("║                                                                    ║")
    print("║  This demo showcases various features and configurations          ║")
    print("║  of the 3D Puzzle Generator tool.                                 ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    try:
        demo_basic()
        demo_custom_slices()
        demo_different_directions()
        demo_material_variations()
        demo_complex_model()
        print_summary()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
