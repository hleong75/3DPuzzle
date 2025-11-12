"""
Command-line interface for 3D Puzzle Generator.
"""

import argparse
import sys
from .puzzle_generator import PuzzleGenerator
from .config import PuzzleConfig


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Generate interlocking 3D puzzles from 3D models for wood manufacturing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a puzzle with default settings
  puzzle3d input.stl -o output/
  
  # Generate with custom number of pieces
  puzzle3d input.obj -o output/ --slices 15
  
  # Adjust for thicker material
  puzzle3d input.stl -o output/ --material-thickness 5.0
  
  # Change slice direction
  puzzle3d input.stl -o output/ --slice-direction y
  
  # Export as single file
  puzzle3d input.stl -o output/ --combined
        """
    )
    
    # Required arguments
    parser.add_argument('input', help='Input 3D model file (STL, OBJ, etc.)')
    parser.add_argument('-o', '--output', required=True, 
                       help='Output directory for puzzle pieces')
    
    # Slicing options
    parser.add_argument('--slices', type=int, default=10,
                       help='Number of slices/pieces to generate (default: 10)')
    parser.add_argument('--slice-direction', choices=['x', 'y', 'z'], default='z',
                       help='Direction to slice the model (default: z)')
    
    # Material options
    parser.add_argument('--material-thickness', type=float, default=3.0,
                       help='Material thickness in mm (default: 3.0)')
    parser.add_argument('--tolerance', type=float, default=0.2,
                       help='Tolerance for interlocking parts in mm (default: 0.2)')
    parser.add_argument('--kerf-width', type=float, default=0.1,
                       help='Laser/saw blade width in mm (default: 0.1)')
    
    # Interlocking options
    parser.add_argument('--tab-width', type=float, default=5.0,
                       help='Width of interlocking tabs in mm (default: 5.0)')
    parser.add_argument('--tab-depth', type=float, default=1.5,
                       help='Depth of interlocking tabs in mm (default: 1.5)')
    parser.add_argument('--tab-spacing', type=float, default=15.0,
                       help='Spacing between tabs in mm (default: 15.0)')
    
    # Output options
    parser.add_argument('--format', choices=['stl', 'dxf'], default='stl',
                       help='Output file format (default: stl)')
    parser.add_argument('--combined', action='store_true',
                       help='Export all pieces in a single file')
    
    args = parser.parse_args()
    
    # Create configuration
    config = PuzzleConfig()
    config.num_slices = args.slices
    config.slice_direction = args.slice_direction
    config.material_thickness = args.material_thickness
    config.tolerance = args.tolerance
    config.kerf_width = args.kerf_width
    config.tab_width = args.tab_width
    config.tab_depth = args.tab_depth
    config.tab_spacing = args.tab_spacing
    config.export_format = args.format
    config.separate_pieces = not args.combined
    
    # Validate configuration
    errors = config.validate()
    if errors:
        print("Error: Invalid configuration:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    try:
        # Create generator and process
        generator = PuzzleGenerator(config)
        generator.generate_from_file(args.input, args.output)
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
