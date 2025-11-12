"""
Main puzzle generator that orchestrates the entire process.
"""

import os
import trimesh
import numpy as np
from .config import PuzzleConfig
from .slicer import PuzzleSlicer
from .interlocking import InterlockingGenerator


class PuzzleGenerator:
    """Main class for generating 3D interlocking puzzles from 3D models."""
    
    def __init__(self, config=None):
        """
        Initialize the puzzle generator.
        
        Args:
            config: PuzzleConfig object, or None to use defaults
        """
        self.config = config if config else PuzzleConfig()
        
    def load_model(self, filepath):
        """
        Load a 3D model from file.
        
        Args:
            filepath: Path to 3D model file (STL, OBJ, etc.)
            
        Returns:
            trimesh.Trimesh object
        """
        try:
            mesh = trimesh.load(filepath)
            
            # If it's a Scene, get the combined mesh
            if isinstance(mesh, trimesh.Scene):
                mesh = mesh.dump(concatenate=True)
            
            # Ensure it's a valid volume
            if not mesh.is_volume:
                print("Warning: Mesh is not a closed volume. Attempting to fix...")
                mesh.fill_holes()
                mesh.fix_normals()
            
            print(f"Loaded model: {filepath}")
            print(f"  Vertices: {len(mesh.vertices)}")
            print(f"  Faces: {len(mesh.faces)}")
            print(f"  Bounds: {mesh.bounds}")
            print(f"  Is watertight: {mesh.is_watertight}")
            
            return mesh
            
        except Exception as e:
            raise ValueError(f"Could not load model from {filepath}: {e}")
    
    def generate_puzzle(self, mesh):
        """
        Generate puzzle pieces from a 3D mesh.
        
        Args:
            mesh: trimesh.Trimesh object
            
        Returns:
            List of trimesh.Trimesh objects representing puzzle pieces
        """
        # Validate configuration
        errors = self.config.validate()
        if errors:
            raise ValueError(f"Invalid configuration: {', '.join(errors)}")
        
        print(f"\nGenerating puzzle with {self.config.num_slices} pieces...")
        print(f"  Slice direction: {self.config.slice_direction}")
        print(f"  Material thickness: {self.config.material_thickness}mm")
        print(f"  Tolerance: {self.config.tolerance}mm")
        print(f"  Tab width: {self.config.tab_width}mm")
        
        # Step 1: Slice the model
        print("\n[1/3] Slicing model...")
        slicer = PuzzleSlicer(mesh, self.config)
        pieces = slicer.create_slice_meshes()
        print(f"  Created {len(pieces)} pieces")
        
        # Step 2: Add interlocking features
        print("\n[2/3] Adding interlocking features...")
        interlocker = InterlockingGenerator(self.config)
        pieces = interlocker.add_interlocking_features(pieces)
        print(f"  Added tabs and slots to {len(pieces)} pieces")
        
        # Step 3: Validate pieces
        print("\n[3/3] Validating pieces...")
        valid_pieces = []
        for i, piece in enumerate(pieces):
            if piece is not None and hasattr(piece, 'vertices') and len(piece.vertices) > 0:
                valid_pieces.append(piece)
                print(f"  Piece {i+1}: {len(piece.vertices)} vertices, {len(piece.faces)} faces")
            else:
                print(f"  Warning: Piece {i+1} is invalid, skipping")
        
        print(f"\nGenerated {len(valid_pieces)} valid puzzle pieces")
        return valid_pieces
    
    def export_pieces(self, pieces, output_dir, base_name="puzzle_piece"):
        """
        Export puzzle pieces to files.
        
        Args:
            pieces: List of trimesh.Trimesh objects
            output_dir: Directory to save files
            base_name: Base name for output files
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nExporting {len(pieces)} pieces to {output_dir}...")
        
        if self.config.separate_pieces:
            # Export each piece separately
            for i, piece in enumerate(pieces):
                filename = f"{base_name}_{i+1:03d}.{self.config.export_format}"
                filepath = os.path.join(output_dir, filename)
                piece.export(filepath)
                print(f"  Exported: {filename}")
        else:
            # Export all pieces in one file
            combined = trimesh.util.concatenate(pieces)
            filename = f"{base_name}_all.{self.config.export_format}"
            filepath = os.path.join(output_dir, filename)
            combined.export(filepath)
            print(f"  Exported: {filename}")
        
        # Also export an assembly view (all pieces together)
        assembly_filename = f"{base_name}_assembly.{self.config.export_format}"
        assembly_path = os.path.join(output_dir, assembly_filename)
        assembly = trimesh.util.concatenate(pieces)
        assembly.export(assembly_path)
        print(f"  Exported assembly: {assembly_filename}")
        
        print(f"\nExport complete!")
    
    def generate_from_file(self, input_file, output_dir):
        """
        Complete pipeline: load model, generate puzzle, and export.
        
        Args:
            input_file: Path to input 3D model
            output_dir: Directory to save puzzle pieces
            
        Returns:
            List of generated puzzle pieces
        """
        print("=" * 60)
        print("3D PUZZLE GENERATOR")
        print("=" * 60)
        
        # Load model
        mesh = self.load_model(input_file)
        
        # Generate puzzle
        pieces = self.generate_puzzle(mesh)
        
        # Export pieces
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        self.export_pieces(pieces, output_dir, base_name)
        
        print("\n" + "=" * 60)
        print("PUZZLE GENERATION COMPLETE")
        print("=" * 60)
        
        return pieces
